# DB connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "dbuser"
DB_PASSWORD = "dbpassword"
DB_URL = "exampledb.cculi2axzscc.us-east-1.rds.amazonaws.com"


def get_db_session():
    import os

    db_url = os.environ.get("DB_URL")
    if not db_url:
        db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:5432/exampledb"
    print(db_url)
    engine = create_engine(db_url)

    # engine = create_engine(
    # f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:5432/exampledb"
    # )
    Session = sessionmaker(bind=engine)
    db_session = Session()
    return db_session


# authentication
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SECRET"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
