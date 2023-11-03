from fastapi import FastAPI
from app.app_models.index import CalculateTaxInput
from app.tax_calculation import calculate_final_tax

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!", "success": True}


@app.post("/calculate_tax")
def calculate_tax(tax_input: CalculateTaxInput):
    tax = calculate_final_tax(
        amount=tax_input.amount,
        age=tax_input.age,
        gender=tax_input.gender,
        location=tax_input.location,
    )
    return {"tax_amount": tax}
