from pydantic import BaseModel, constr
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
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
    date_of_birth: datetime


class IncomeInput(BaseModel):
    year: int
    income: int
    location: constr(regex="dhaka|chittagong|city|non_city")


class LoginInput(BaseModel):
    id: str
    password: str


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
