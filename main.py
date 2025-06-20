from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.shloakh.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Remedies
with open("remedies.json", "r", encoding="utf-8") as file:
    remedies = json.load(file)

# ✅ Load API Keys
def load_keys():
    with open("api_keys.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_keys(keys):
    with open("api_keys.json", "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2)

# ✅ Validate API Key + Track Usage
def validate_key(api_key):
    keys = load_keys()
    for user in keys:
        if user["key"] == api_key:
            if user["usage"] < user["limit"]:
                user["usage"] += 1
                save_keys(keys)
                return True
            else:
                raise HTTPException(status_code=429, detail="API usage limit exceeded.")
    raise HTTPException(status_code=401, detail="Invalid API key.")

# ✅ Remedy Search
def get_remedy(symptom):
    for item in remedies:
        if item["symptom"].lower() == symptom.lower():
            return item
    return {
        "symptom": symptom,
        "remedy": "No remedy found",
        "dosha": "Unknown"
    }

# ✅ API Endpoint
@app.get("/remedy")
def remedy(symptom: str = Query(...), key: str = Query(...)):
    validate_key(key)
    return get_remedy(symptom)
