from fastapi import FastAPI, Depends
from uuid import uuid4
from datetime import datetime
from app.app_models.models import (
    CalculateTaxInput,
    User,
    UserInput,
    LoginInput,
    IncomeInput,
    TaxDetails,
)
from app.tax_calculation import calculate_final_tax, get_taxable_income
from app.utils import get_db_session, AuthHandler

app = FastAPI()

db_session = get_db_session()
auth_handler = AuthHandler()


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
async def signup(user: UserInput):
    # check for existing user_id
    existing_user = db_session.query(User).filter(User.id == user.id).first()
    if existing_user:
        return {"message": "User already exists", "success": False}

    user.password = auth_handler.get_password_hash(user.password)

    new_user = User(
        id=user.id,
        name=user.name,
        password=user.password,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
    )
    db_session.add(new_user)
    db_session.commit()

    return {"message": "User created successfully", "success": True}


@app.post("/login", tags=["Authentication"])
async def login(credentials: LoginInput):
    user = db_session.query(User).filter(User.id == credentials.id).first()
    if not user:
        return {"message": "User not found", "success": False}

    if not auth_handler.verify_password(credentials.password, user.password):
        return {
            "message": "Incorrect password",
            "success": False,
        }

    token = auth_handler.encode_token(user.id)
    return {
        "user_id": credentials.id,
        "token": token,
        "success": True,
    }


@app.get("/user/{user_id}", tags=["User Profile"])
async def get_user(user_id: str, auth_id=Depends(auth_handler.auth_wrapper)):
    if auth_id != user_id:
        return {"message": "Unauthorized", "success": False}
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found", "success": False}

    # remove password from response
    user.password = None

    return {"user": user, "success": True}


@app.post("/income_details", tags=["Tax Details"])
async def add_tax_details(
    income_input: IncomeInput, auth_id=Depends(auth_handler.auth_wrapper)
):
    # check for existing tax details for the same person of the same year
    tax_details_exists = (
        db_session.query(TaxDetails)
        .filter(TaxDetails.user_id == auth_id, TaxDetails.year == income_input.year)
        .first()
    )
    if tax_details_exists:
        return {
            "success": False,
            "message": "Tax details already exists for the same year",
        }

    # fetch user_details
    user = db_session.query(User).filter(User.id == auth_id).first()
    gender = user.gender
    date_of_birth = user.date_of_birth

    current_date = datetime.now()

    # Calculate the age by subtracting the birthdate from the current date
    age = (
        current_date.year
        - date_of_birth.year
        - (
            (current_date.month, current_date.day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )

    data = {
        "tax_id": uuid4(),
        "user_id": auth_id,
        "year": income_input.year,
        "income": income_input.income,
        "taxable_income": get_taxable_income(income_input.income, gender, age),
        "location": income_input.location,
        "tax_amount": calculate_final_tax(
            income_input.income, gender, age, income_input.location
        ),
    }

    tax_details = TaxDetails(**data)

    db_session.add(tax_details)
    db_session.commit()

    return {
        "success": True,
        "message": "Tax details added successfully",
        "data": data,
    }


@app.get("/tax_details", tags=["Tax Details"])
async def get_tax_details(auth_id=Depends(auth_handler.auth_wrapper)):
    tax_details = (
        db_session.query(TaxDetails)
        .filter(TaxDetails.user_id == auth_id)
        .order_by(TaxDetails.year)
        .all()
    )
    if not tax_details:
        return {"message": "No tax details found", "success": False}

    return {"tax_details": tax_details, "success": True}
