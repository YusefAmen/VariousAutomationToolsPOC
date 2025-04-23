import yaml
import logging
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse, urlunparse, ParseResult
import asyncio
import aiohttp
from aiohttp import ClientSession
import builtins

# ----------------- LOGGING SETUP -----------------

logging.basicConfig(
    level=logging.INFO,  # Use DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("availability_monitor.log"),
        logging.StreamHandler()
    ]
)

# Redirect all print() calls to logger
def print(*args, **kwargs):
    logging.info(' '.join(map(str, args)))
builtins.print = print

logger = logging.getLogger(__name__)

# ----------------- HELPERS -----------------

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.hostname
    except Exception as e:
        logger.error(f"Error extracting domain: {e}")
        return None

def get_safe_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https'] or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        cleaned = ParseResult(
            scheme=parsed.scheme,
            netloc=parsed.hostname,
            path=parsed.path,
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment
        )
        return urlunparse(cleaned)
    except Exception as e:
        logger.warning(f"Exception cleaning URL: {e}")
        return None

# ----------------- REQUESTS -----------------

async def make_request(session, url, method, headers=None, body=None):
    if not url or not url.strip():
        logger.warning(f"Skipping request: Invalid URL -> {url!r}")
        return {"error": "invalid_url", "url": url}

    method = method.upper() if method else 'GET'

    logger.info(f"[HTTP REQUEST START] {time.strftime('%Y-%m-%d %H:%M:%S')} | Method: {method} | URL: {url}")

    try:
        start = time.time()
        async with session.request(method, url, headers=headers, json=body) as response:
            status = response.status
        end = time.time()

        elapsed = round(end - start, 3)
        logger.info(f"[HTTP REQUEST END] {time.strftime('%Y-%m-%d %H:%M:%S')} | Elapsed: {elapsed}s | Status: {status}")
        return status, elapsed
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return {"error": "request_failed", "url": url}

async def check_health(session, endpoint):
    url = get_safe_url(endpoint['url'])
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        result = await make_request(session, url, method, headers, body)

        if isinstance(result, dict) and "error" in result:
            return "DOWN"

        status, elapsed = result
        if 200 <= status < 300 and elapsed <= 0.5:
            return "UP"
        else:
            return "DOWN"
    except Exception as e:
        logger.error(f"Health check error for {endpoint['url']}: {e}")
        return "DOWN"

# ----------------- MONITOR -----------------

async def monitor_endpoints(file_path):
    endpoints = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        async with ClientSession() as session:
            tasks = [check_health(session, endpoint) for endpoint in endpoints]
            results = await asyncio.gather(*tasks)

            for endpoint, result in zip(endpoints, results):
                domain = extract_domain(endpoint["url"])
                if domain:
                    domain_stats[domain]["total"] += 1
                    if result == "UP":
                        domain_stats[domain]["up"] += 1

        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            logger.info(f"{domain} has {availability}% availability percentage")

        logger.info("-------------------------")
        await asyncio.sleep(15)

# ----------------- ENTRY POINT -----------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        asyncio.run(monitor_endpoints(config_file))
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")

