from fastapi import HTTPException
from auth import router
from auth.jwt_token import create_token
from database import engine, db_crud
from pydantic import EmailStr

collection = engine.db.get_collection("users")


@router.get(
    "/generate/emailToken",
    summary="generates verification email token",
)
async def verify_user_email(user_email: EmailStr):
    """creates email verification token"""

    user = await db_crud.fetch_one(collection, email=user_email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token(user)
    return {"token": token}
