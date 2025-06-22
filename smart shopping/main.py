from fastapi import FastAPI, Query, HTTPException
from chatbot_model import chatbot_response
from comparison_model import compare_products
from pydantic import BaseModel
from typing import Dict
import pandas as pd
import google.generativeai as genai
import os

app = FastAPI()

# In-memory user storage (Replace with a database in production)
users_db = {}

class SignupRequest(BaseModel):
    name: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class EMICalculatorRequest(BaseModel):  # FIX: Defined missing class
    price: float
    down_payment: float
    tenure: int
    interest_rate: float

@app.post("/signup/")
def signup(user: SignupRequest):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users_db[user.username] = {"name": user.name, "password": user.password}
    return {"message": "Signup successful!"}

@app.post("/login/")
def login(user: LoginRequest):
    if user.username not in users_db or users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful!"}

# -------------------- AI SHOPPING ASSISTANT ROUTES --------------------
PRODUCT_CSV_FILES = {
    "Mobile": "backend/phones.csv",
    "Laptop": "backend/laptops.csv",
    "Smartwatch": "backend/smartwatches.csv",
    "Television": "backend/tvs.csv",
    "Air Conditioner": "backend/acs.csv",
    "Washing Machine": "backend/washing_machines.csv"
}

@app.get("/", tags=["Home"])
def home():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to AI Shopping Assistant"}

@app.get("/chatbot/", tags=["Chatbot"])
def chatbot(
    category: str = Query(..., description="Product category (e.g., Mobile, Laptop, AC)"),
    budget: int = Query(..., description="Budget in INR"),
    query: str = Query(..., description="User's query for recommendations")
):
    """Returns AI-based product recommendations."""
    if budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than 0")

    response = chatbot_response(category, budget, query)
    return {"response": response}

@app.get("/compare/", tags=["Comparison"])
def compare(
    product1: str = Query(..., description="First product to compare"),
    product2: str = Query(..., description="Second product to compare")
):
    """Compares two products and returns a recommendation."""
    if not product1.strip() or not product2.strip():
        raise HTTPException(status_code=400, detail="Both product names must be provided")

    response = compare_products(product1, product2)
    return {"response": response}

# -------------------- EMI CALCULATOR ROUTE --------------------
@app.post("/calculate_emi/")
def calculate_emi(data: EMICalculatorRequest):
    """Calculates EMI based on user input."""
    try:
        if data.price <= 0 or data.tenure <= 0 or data.interest_rate < 0:  # FIX: Corrected attribute references
            raise HTTPException(status_code=400, detail="Invalid input values.")

        loan_amount = data.price - data.down_payment  # FIX: Corrected reference to 'data'

        if loan_amount <= 0:
            return {"emi": 0, "message": "No EMI required. Fully paid by down payment."}

        monthly_interest_rate = (data.interest_rate / 100) / 12  # FIX: Corrected reference to 'data'

        if monthly_interest_rate == 0:
            emi = loan_amount / data.tenure  # FIX: Corrected reference to 'data'
        else:
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** data.tenure) / \
                  ((1 + monthly_interest_rate) ** data.tenure - 1)  # FIX: Corrected reference to 'data'

        return {
            "emi": round(emi, 2),
            "total_payment": round(emi * data.tenure, 2),  # FIX: Corrected reference to 'data'
            "total_interest": round((emi * data.tenure) - loan_amount, 2)  # FIX: Corrected reference to 'data'
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error calculating EMI. Please try again.")