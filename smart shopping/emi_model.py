from fastapi import APIRouter, Query
from pydantic import BaseModel
import math

router = APIRouter()

class EMIRequest(BaseModel):
    category: str
    price: float
    tenure: int
    interest_rate: float

def calculate_emi(price: float, tenure: int, interest_rate: float):
    """Calculate EMI using the formula: EMI = [P * R * (1+R)^N] / [(1+R)^N - 1]"""
    if tenure <= 0 or interest_rate < 0:
        return {"error": "Invalid tenure or interest rate"}
    
    monthly_rate = (interest_rate / 100) / 12
    emi = (price * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
    
    total_payment = emi * tenure
    interest_paid = total_payment - price
    
    return {
        "EMI per Month (INR)": round(emi, 2),
        "Total Payment (INR)": round(total_payment, 2),
        "Interest Paid (INR)": round(interest_paid, 2)
    }

@router.post("/calculate/")
def get_emi(data: EMIRequest):
    """API Endpoint for EMI Calculation"""
    return calculate_emi(data.price, data.tenure, data.interest_rate)
