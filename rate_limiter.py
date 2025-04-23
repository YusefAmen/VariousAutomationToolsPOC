import requests
import time
from collections import deque

def fetch_all_users_with_org_emails():
    base_url = "https://reqres.in/api/users"
    rate_limit = 5
    time_window = 10  # seconds
    timestamps = deque()

    page = 1
    all_users = []

    while True:
        # RATE LIMIT CHECK
        current_time = time.time()

        # Remove timestamps older than 10 seconds
        while timestamps and current_time - timestamps[0] > time_window:
            timestamps.popleft()

        # Wait if we're at the rate limit
        if len(timestamps) >= rate_limit:
            wait_time = time_window - (current_time - timestamps[0])
            print(f"Rate limit hit. Sleeping for {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            continue  # Re-check after sleep

        # Send request
        print(f"Requesting page {page}...")
        response = requests.get(f"{base_url}?page={page}")
        timestamps.append(time.time())  # Log timestamp *after* sending

        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}")
            break

        data = response.json()
        users = data.get("data", [])

        # Filter users with `.org` emails
        filtered_users = [
            user for user in users if user.get("email", "").endswith(".org")
        ]
        all_users.extend(filtered_users)

        if page >= data.get("total_pages", 1):
            break

        page += 1

    return all_users

