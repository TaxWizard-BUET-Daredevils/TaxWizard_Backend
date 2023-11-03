from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Create the SQLAlchemy engine. Replace 'your_connection_string' with your RDS database connection string.
DB_USER = "dbuser"
DB_PASSWORD = "dbpassword"
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@exampledb.cculi2axzscc.us-east-1.rds.amazonaws.com:5432/exampledb"
)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    gender = Column(String)
    age = Column(Integer)


# Define the TaxDetails model
class TaxDetails(Base):
    __tablename__ = "tax_details"

    tax_id = Column(String, primary_key=True)
    user_id = Column(String)
    year = Column(Integer)
    income = Column(Integer)
    location = Column(String)
    tax_amount = Column(Integer)


# Create the tables in the database
Base.metadata.create_all(engine)


# Insert a User record
new_user = User(id="1", name="John Doe", password="password123", gender="Male", age=30)
session.add(new_user)
session.commit()


# Insert a TaxDetails record
new_tax_details = TaxDetails(
    tax_id="1",
    user_id="1",
    year=2023,
    income=50000,
    location="New York",
    tax_amount=10000,
)
session.add(new_tax_details)
session.commit()

# Get a User record by ID
user = session.query(User).filter(User.id == "1").first()
print(f"User Name: {user.name}, Age: {user.age}")

# Get a TaxDetails record by tax ID
tax_details = session.query(TaxDetails).filter(TaxDetails.tax_id == "1").first()
print(
    f"Year: {tax_details.year}, Income: {tax_details.income}, Tax Amount: {tax_details.tax_amount}"
)
