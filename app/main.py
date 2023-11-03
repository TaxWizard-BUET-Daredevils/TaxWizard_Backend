from fastapi import FastAPI, Depends
from app.app_models.models import (
    CalculateTaxInput,
    User,
    UserInput,
    LoginInput,
    TaxDetailsModel,
    TaxDetails,
)
from app.tax_calculation import calculate_final_tax
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
        age=user.age,
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
