from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import router
from database import engine, db_crud, models
from auth.jwt_token import create_token
from utils import password_hashing

# from utils.password_hashing import verify_password
from typing_extensions import Annotated


collection = engine.db.get_collection("users")


@router.post("/signin")
async def user_login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """exchange user credentials for token"""

    user = await db_crud.fetch_one(collection, email=payload.username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not password_hashing.verify_password(
        payload.password, user.get("password")
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_token = create_token(user)

    return {
        "acces_token": user_token,
        "token_type": "Bearer",
    }
