from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "dbuser"
DB_PASSWORD = "dbpassword"
DB_URL = "exampledb.cculi2axzscc.us-east-1.rds.amazonaws.com"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:5432/exampledb")
Session = sessionmaker(bind=engine)
db_session = Session()
