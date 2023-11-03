from pydantic import BaseModel, constr
from sqlalchemy import Column, String, Integer, DateTime
from datetime import date
from sqlalchemy.ext.declarative import declarative_base


class CalculateTaxInput(BaseModel):
    amount: int
    gender: constr(regex="male|female")
    age: int
    location: constr(regex="dhaka|chittagong|city|non_city")


class UserInput(BaseModel):
    id: str
    name: str
    password: str
    gender: constr(regex="male|female")
    date_of_birth: date

    class Config:
        schema_extra = {
            "example": {
                "id": "0001",
                "name": "Dhrubo Kamal",
                "password": "1234",
                "gender": "male",
                "date_of_birth": "1998-01-01",
            }
        }


class UserOutput(BaseModel):
    id: str
    name: str
    gender: str
    date_of_birth: date


class IncomeInput(BaseModel):
    year: int
    income: int
    location: constr(regex="dhaka|chittagong|city|non_city")

    class Config:
        schema_extra = {
            "example": {
                "year": 2023,
                "income": 1000000,
                "location": "dhaka",
            }
        }


class LoginInput(BaseModel):
    id: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "id": "0001",
                "password": "1234",
            }
        }


# SQL Classes
# Create a base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    gender = Column(String)
    date_of_birth = Column(DateTime)


# Define the TaxDetails model
class TaxDetails(Base):
    __tablename__ = "tax_details"

    tax_id = Column(String, primary_key=True)
    user_id = Column(String)
    year = Column(Integer)
    income = Column(Integer)
    taxable_income = Column(Integer)
    location = Column(String)
    tax_amount = Column(Integer)
