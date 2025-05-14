import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

# Test call (e.g. list customers)
response = stripe.Customer.list(limit=3)
print(response)