# Fetch Rewards Take-Home SRE Challenge

## Overview
This project is a Python-based service monitor (availability_monitor.py) that checks the health of specified HTTP endpoints every 15 seconds. It tracks status codes, response times, and calculates the availability percentage of each unique domain. The script uses `requests`, `PyYAML`, and `defaultdict`, and includes robust error handling and logging.

The original code had issues with YAML loading, request defaults, port handling, and lacked clear visibility into request timing and behavior. This updated version fixes those problems and introduces improved structure and logging.

---

## Files to include: requirements.in, availability_monitor.py, env_setup.sh + your own sample.yaml file

## Requirements
- Python 3.7+
- Virtual environment (optional but recommended)
- `pyyaml`
- `requests`

Install dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Clone the repository and navigate into it
```bash
git clone <repo_url>
cd <repo_folder>
```

### 2. Start environment (QUICK START)
```bash
sh env_setup.sh
./venv/bin/python availability_monitor.py

```


### 2. (Optional) Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.  (Optional) Install dependencies
```bash
pip install -r requirements.txt
```

Alternatively, you can generate the `requirements.txt` from a `requirements.in` (if included):
```bash
pip install pip-tools
pip-compile requirements.in > requirements.txt
pip install -r requirements.txt
```

You can also use the provided setup script:
```bash
source env_setup.sh
```

---

## Running the Monitor
```bash
python availability_monitor.py <path_to_config_yaml>
```

Example:
```bash
sh env_setup.sh
./venv/bin/python availability_monitor.py <path_to_config_yaml>


```

---

## Fixes and Improvements

### 1. YAML Parsing Fix
**Problem:** The YAML file wasn't being parsed correctly due to incorrect usage of `yaml.safe_load()`.
**Fix:** Used `file.read()` to load contents before passing to `yaml.safe_load()`.

### 2. `pyyaml` Missing
**Problem:** Code failed due to missing `pyyaml` dependency.
**Fix:** Added `pyyaml` to `requirements.txt` and imported it properly.

### 3. Port Handling
**Problem:** Port numbers in URLs caused domains to be treated as separate entries in availability stats.
**Fix:** Used `urllib.parse` to extract and strip port from URLs using `.hostname`.

### 4. No Defaults for Requests
**Problem:** Missing method, headers, or body fields caused crashes.
**Fix:** Added default values: method defaults to `GET`, headers/body default to empty dictionaries.

### 5. Logging Improvements
**Problem:** Request logs lacked timestamps and structure.
**Fix:**
```python
print(f"[HTTP REQUEST START] {time.strftime('%Y-%m-%d %H:%M:%S')} | Method: {method} | URL: {url} | Headers: {headers or '{}'} | Body: {body or '{}'}")
...
print(f"[HTTP REQUEST END] {time.strftime('%Y-%m-%d %H:%M:%S')} | Elapsed: {elapsed}s | Status: {response.status_code}")
```

### 6. Availability Logic
**Problem:** Ports in URLs led to duplicate domains being counted separately.
**Fix:** Replaced manual domain parsing with `urlparse().hostname` to normalize.

### 7. Response Time Threshold
**Problem:** 500ms SLA for availability was not enforced.
**Fix:** Availability requires both a 2xx response and elapsed time <= 0.5s.

### 8. Async Http and Sleep
**Problem:** As it scales to handling more urls inconsistent timing can occur and also the requests in general are blocking taking up time and limiting how many requests would be able to be made.
**Fix:** To allow consistency of timing window and to improve efficiency. 

## 9. Added structured logging
**Problem** Hard to review process especially wiht async if there arent structured logs to check. Also allows for error catches without letting the script fail completely.
**Fix** 

---

## Potential Next Steps
- Use a hash map or dictionary to track endpoint check history
- Log results to JSONL or use persistent storage (e.g., SQLite)
- Improve testability with unit tests and assertions
- Add log rotation
- Implement prioritization or dynamic endpoint scheduling??
- Implement smart rate limiting a separate file to utilize it as a rate limit class with custom features 

---

## Example Output
```
[HTTP REQUEST START] 2025-04-15 21:12:03 | Method: GET | URL: https://example.com | Headers: {} | Body: {}
[HTTP REQUEST END] 2025-04-15 21:12:03 | Elapsed: 0.327s | Status: 200
example.com has 100% availability percentage
```

---

## Author
Jared Godfrey Amen

---


