from fastapi import FastAPI
from app.app_models.models import (
    CalculateTaxInput,
    User,
    UserInput,
    TaxDetailsModel,
    TaxDetails,
)
from app.tax_calculation import calculate_final_tax
from app.utils import db_session

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


@app.post("/signup", tags=["Authentication"])
def signup(user: UserInput):
    # check for existing user_id
    existing_user = db_session.query(User).filter(User.id == user.id).first()
    if existing_user:
        return {"message": "User already exists", "success": False}

    new_user = User(
        id=user.id,
        name=user.name,
        password=user.password,
        gender=user.gender,
        age=user.age,
    )
    db_session.add(new_user)
    db_session.commit()

    return {"message": "User created successfully", "success": True}


@app.get("/user/{user_id}", tags=["User Profile"])
def get_user(user_id: str):
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found", "success": False}

    return {"user": user, "success": True}
