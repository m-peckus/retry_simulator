import os
import time
import stripe
from dotenv import load_dotenv
import requests
from stripe.error import RateLimitError

# Load environment and set api key
load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

# Retry decorator 
def retry_on_rate_limit(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                response = func(*args, **kwargs)
                #if response.status_code != 429:
                # Stripe's Python SDK raises exceptions on 429
                if not isinstance(response, stripe.error.RateLimitError):
                    return response
                print(f"Rate limit (429). Retrying in {delay * (attempt + 1)}s...")
                time.sleep(delay * (attempt + 1))
            raise Exception("Max retries reached.")
        return wrapper
    return decorator

# Simulated rate limit request
@retry_on_rate_limit(max_retries=4, delay=1)
def call_stripe_customers():
    return stripe.Customer.list(limit=3)

# Simulate multiple rapid requests to trigger rate limits
if __name__ == "__main__":
    for _ in range(100): # Make 100 quick requests in an attempt to trigger rate limit
        response = call_stripe_customers()
        print(response)