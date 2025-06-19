from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# ✅ CORRECT CORS SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com"],  # Make sure there's NO trailing slash
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load remedies from the JSON file
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

# ✅ API route
@app.get("/remedy")
def remedy(symptom: str = Query(..., description="Enter a symptom like 'constipation'")):
    return get_remedy(symptom)

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com", "http://localhost", "*"],

      # You can replace "*" with your domain like "https://shloakh.com"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load remedies from the JSON file
with open("remedies.json", "r", encoding="utf-8") as file:
    remedies = json.load(file)

# Function to find remedy by symptom
def get_remedy(symptom):
    for item in remedies:
        if item["symptom"].lower() == symptom.lower():
            return item
    return {
        "symptom": symptom,
        "remedy": "No remedy found",
        "dosha": "Unknown"
    }

# API route
@app.get("/remedy")
def remedy(symptom: str = Query(..., description="Enter a symptom like 'constipation'")):
    return get_remedy(symptom)
