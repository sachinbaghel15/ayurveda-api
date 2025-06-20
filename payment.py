import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow CORS for your site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Stripe Secret Key (Test Mode)
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# 🎯 Create Stripe Checkout Session
@app.get("/create-checkout-session")
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Ayurveda API – Pro Plan',
                    },
                    'unit_amount': 49900,  # ₹499 = 49900 paisa
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://www.shloakh.com/success',
            cancel_url='https://www.shloakh.com/cancel',
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}
