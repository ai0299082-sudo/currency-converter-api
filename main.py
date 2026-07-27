from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")

@app.get("/")
def home():
    return {"message": "Currency Converter API"}

@app.get("/convert/{from_currency}/{to_currency}/{amount}")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency.upper()}"

    response = requests.get(url)
    data = response.json()

    if data["result"] != "success":
        return {"error": "Invalid currency"}

    rate = data["conversion_rates"].get(to_currency.upper())

    if rate is None:
        return {"error": "Currency not found"}

    converted_amount = amount * rate

    return {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "converted_amount": round(converted_amount, 2),
        "exchange_rate": rate
    }