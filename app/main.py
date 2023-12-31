from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from uuid import uuid4
from datetime import datetime
from app.app_models.models import (
    CalculateTaxInput,
    User,
    UserInput,
    UserOutput,
    LoginInput,
    IncomeInput,
    TaxDetails,
)
from app.tax_calculation import calculate_final_tax, get_taxable_income
from app.utils import get_db_session, AuthHandler

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    logging.info(
        f"calculated tax = {tax} for amount = {tax_input.amount}, age={tax_input.age}, gender = {tax_input.gender}, location = {tax_input.location}"
    )
    return {"tax_amount": tax}


@app.post("/signup", tags=["Authentication"])
async def signup(user: UserInput):
    # check for existing user_id
    existing_user = db_session.query(User).filter(User.id == user.id).first()
    if existing_user:
        logging.info(f"User already exists with id = {user.id}")
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
    logging.info(f"User created successfully with id = {user.id}")
    return {"message": "User created successfully", "success": True}


@app.post("/login", tags=["Authentication"])
async def login(credentials: LoginInput):
    user = db_session.query(User).filter(User.id == credentials.id).first()
    if not user:
        logging.info(f"User not found with id = {credentials.id}")
        return {"message": "User not found", "success": False}

    if not auth_handler.verify_password(credentials.password, user.password):
        logging.info(f"Incorrect password for user with id = {credentials.id}")
        return {
            "message": "Incorrect password",
            "success": False,
        }

    logging.info(f"User logged in with id = {credentials.id}")
    token = auth_handler.encode_token(user.id)
    return {
        "user_id": credentials.id,
        "token": token,
        "success": True,
    }


@app.get("/user/{user_id}", tags=["User Profile"])
async def get_user(user_id: str, auth_id=Depends(auth_handler.auth_wrapper)):
    if auth_id != user_id:
        logging.info(f"Unauthorized access for user with id = {user_id}")
        return {"message": "Unauthorized", "success": False}
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        logging.info(f"User not found with id = {user_id}")
        return {"message": "User not found", "success": False}

    user_profile = UserOutput(
        id=user.id, name=user.name, gender=user.name, date_of_birth=user.date_of_birth
    )
    logging.info(f"User profile fetched for user with id = {user_id}")
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
        logging.info(
            f"Tax details already exists for user with id = {auth_id} and year = {income_input.year}"
        )
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

    logging.info(
        f"Tax details added successfully for user with id = {auth_id} and year = {income_input.year}"
    )

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
        logging.info(f"No tax details found for user with id = {auth_id}")
        return {"message": "No tax details found", "success": False}

    logging.info(f"Tax details fetched for user with id = {auth_id}")
    return {"tax_details": tax_details, "success": True}
