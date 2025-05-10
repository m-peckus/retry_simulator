import requests
import time

# Retry decorator 
def retry_on_rate_limit(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                response = func(*args, **kwargs)
                if response.status_code != 429:
                    return response
                print(f"Rate limit (429). Retrying in {delay * (attempt + 1)}s...")
                time.sleep(delay * (attempt + 1))
            raise Exception("Max retries reached.")
        return wrapper
    return decorator

# Simulated rate limit request
@retry_on_rate_limit(max_retries=4, delay=1)
def call_httpbin():
    return requests.get("https://httpbin.org/status/429")

# Test
call_httpbin()
