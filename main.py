from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import difflib  # for fuzzy matching
import stripe
import os

app = FastAPI()

# ✅ CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load remedies data from JSON file
with open("remedies.json", "r", encoding="utf-8") as file:
    remedies = json.load(file)

# ✅ Helper: Normalize text
def normalize(text):
    return text.lower().strip()

# ✅ Remedy search logic
def get_remedy(symptom):
    normalized_symptom = normalize(symptom)

    # 1. Exact or partial match
    for item in remedies:
        if normalized_symptom in normalize(item["symptom"]):
            return {
                "symptom": item["symptom"],
                "description": item.get("description", "No description available."),
                "remedy": item.get("remedy", "No remedy found."),
                "dosha": item.get("dosha", "Unknown"),
                "herbs": item.get("herbs", "Not specified"),
                "prevention": item.get("prevention", "No tips available.")
            }

    # 2. Fuzzy matching for suggestions
    all_symptoms = [normalize(r["symptom"]) for r in remedies]
    close_matches = difflib.get_close_matches(normalized_symptom, all_symptoms)

    return {
        "symptom": symptom,
        "remedy": "❌ No exact match found.",
        "suggested_matches": close_matches if close_matches else ["Try different symptom keywords"]
    }

# ✅ API route for remedies
@app.get("/remedy")
def remedy(symptom: str = Query(..., description="Enter a symptom like 'constipation'")):
    return get_remedy(symptom)

# ✅ Stripe payment integration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/create-checkout-session")
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "Ayurveda API – Pro Plan",
                    },
                    "unit_amount": 49900,  # ₹499 in paise
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://www.shloakh.com/p/success.html",
            cancel_url="https://www.shloakh.com/p/cancel.html",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}
