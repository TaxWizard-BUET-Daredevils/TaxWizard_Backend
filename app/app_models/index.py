from pydantic import BaseModel, constr


class CalculateTaxInput(BaseModel):
    amount: int
    gender: constr(regex="male|female")
    age: int
    location: constr(regex="dhaka|chittagong|city|non_city")
