from auth import router
from auth.jwt_token import decode_token
from database import engine
from utils.password_hashing import hash_password


collection = engine.db.get_collection("users")


@router.patch(
    "/resetPassword",
    summary="resets the users password",
)
async def password_reset(token: str, new_password: str):
    """resets the users password"""

    user = decode_token(token)
    hashed_pwd = hash_password(new_password)
    # user = await db_crud.fetch_one(collection, email=user.get("email"))

    result = await collection.find_one_and_update(
        {"email": user["email"]}, {"$set": {"password": hashed_pwd}}
    )

    print(result)

    return {"msg": "Password changed successfully"}
