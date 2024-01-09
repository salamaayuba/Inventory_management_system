from fastapi import APIRouter, Depends, HTTPException, status
from database import db_crud, engine, models
from auth.jwt_token import oauth2_scheme
from pydantic import EmailStr
from typing import List
from typing_extensions import Annotated
from utils import password_hashing

# from utils.password_hashing import hash_password


router = APIRouter(
    tags=["Users"],
    prefix="/user",
)

collection = engine.db.get_collection("users")


@router.get(
    "/all",
    response_model=List[models.UserData],
)
# async def all_users(active_user: Annotated[dict, Depends(oauth2_scheme)]):
async def all_users():
    """returns all users on the platform"""

    data = await db_crud.fetch_all_documents(collection, models.UserData)
    return data


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(payload: models.Users):
    """registers a user"""

    temp_data = payload.model_dump().copy()
    hashed_pwd = password_hashing.hash_password(temp_data["password"])
    temp_data["password"] = hashed_pwd
    await db_crud.add_single_document(collection, temp_data)
    return {
        "msg": "user registered",
    }


@router.delete("/removeUser")
async def remove_user(
    user_email: EmailStr,
    active_user: Annotated[dict, Depends(oauth2_scheme)],
):
    """deletes a user account"""

    # check if the email is existing before you delete
    user = await db_crud.fetch_one(collection, email=user_email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    await db_crud.remove_one_document(collection, email=user_email)
