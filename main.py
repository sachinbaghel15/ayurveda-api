from fastapi import FastAPI, Query
import json

app = FastAPI()

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
