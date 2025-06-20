from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import stripe
import os

app = FastAPI()

# ✅ CORS Configuration for frontend (shloakh.com)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Ayurveda remedies from local JSON file
with open("remedies.json", "r", encoding="utf-8") as file:
    remedies = json.load(file)

# ✅ Function to find remedy by symptom
def get_remedy(symptom):
    for item in remedies:
        if item["symptom"].lower() == symptom.lower():
            return item
    return {
        "symptom": symptom,
        "remedy": "No remedy found",
        "dosha": "Unknown"
    }

# ✅ Remedy endpoint
@app.get("/remedy")
def remedy(symptom: str = Query(..., description="Enter a symptom like 'constipation'")):
    return get_remedy(symptom)


# ✅ Stripe Payment Integration

# Load Stripe secret key from environment (set in render.yaml)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ✅ Create Stripe checkout session (key is optional now)
@app.get("/create-checkout-session")
def create_checkout_session(key: str = Query(None)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "Ayurveda API – Pro Plan",
                    },
                    "unit_amount": 49900,  # ₹499 in paisa
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://www.shloakh.com/success",
            cancel_url="https://www.shloakh.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}
