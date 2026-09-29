import os
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set. Add it to your .env file.")

security = HTTPBearer()


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(user_id: int):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    FastAPI dependency: verifies the Bearer token on every protected route and
    returns the real user_id from it. This is what makes data isolation (Feature 1)
    actually enforced -- routes no longer trust a user_id the client sends.
    """
    try:
        payload = decode_token(credentials.credentials)
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired, please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token.")
