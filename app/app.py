from flask import Flask, Response
from datetime import datetime
import threading
import logging
import random
import time

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename="/var/log/app.log", level=logging.INFO)

# Shared in-memory metric storage
metrics = {"200": 0, "500": 0}

# Background simulation thread
def simulate_requests():
    while True:
        status = random.choices(["200", "500"], weights=[0.9, 0.1])[0]
        metrics[status] += 1
        msg = f"[{datetime.utcnow().isoformat()}] Simulated {status} response"
        if status == "500":
            logging.error(msg)
        else:
            logging.info(msg)
        time.sleep(1)  # simulate 1 req/sec

# Route for Prometheus to scrape
@app.route("/metrics")
def prom_metrics():
    return Response(
        f"""
# HELP myapp_http_requests_total Total HTTP requests
# TYPE myapp_http_requests_total counter
myapp_http_requests_total{{status="200"}} {metrics["200"]}
myapp_http_requests_total{{status="500"}} {metrics["500"]}
""",
        mimetype="text/plain"
    )

# Optional endpoint to hit manually
@app.route("/")
def index():
    return "Mock service running.\n"

# Start background traffic simulation
@app.before_first_request
def launch_simulation():
    t = threading.Thread(target=simulate_requests)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

