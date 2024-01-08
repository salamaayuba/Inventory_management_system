# to hold all jwt token actions such as authentication opf tokens, creating of tokens, decoding of user tokens
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing_extensions import Annotated
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="singin")

load_dotenv()

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"Authorization": "Bearer"},
    )


def token_payload(user: dict) -> dict:
    """data encodedin the user token"""

    return {
        "name": user.get("name", None),
        "email": user.get("email", None),
    }


def create_token(user: dict) -> str:
    """creates the user token"""

    payload = token_payload(user)
    expire_time = datetime.utcnow() + timedelta(minutes=int(os.getenv("JWT_TIMEOUT")))
    payload.update(iat=datetime.utcnow(), exp=expire_time)
    token = jwt.encode(
            payload,
            os.getenv("JWT_SECRET_KEY"),
            algorithm=os.getenv("JWT_ALGORITHM"),
        )

    return token


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """decodes the user token"""

    try:
        active_user = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                os.getenv("JWT_ALGORITHM"),
            )

    except JWTError:
        raise CREDENTIALS_EXCEPTION

    return active_user
