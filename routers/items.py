from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
)
from database import db_crud, engine, models
from auth.jwt_token import oauth2_scheme
from utils import read_csv
from datetime import datetime
from pydantic import EmailStr
from typing import List
from typing_extensions import Annotated


router = APIRouter(
    tags=["Items"],
    prefix="/items",
)

item_collection = engine.db.get_collection("items")
borrowed_collection = engine.db.get_collection("borrowed_items")
ALLOWED_FILE_TYPES = (
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)


@router.get(
    "/allItems",
    response_model=List[models.Items],
)
# async def all_items(active_user: Annotated[dict, Depends(oauth2_scheme)]):
async def all_items():
    """returns all items on the platform"""

    data = await db_crud.fetch_all_documents(
        item_collection, models.Items
    )
    return data


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register_item(payload: models.Items):
    """registers a item"""

    temp_data = payload.model_dump().copy()
    await db_crud.add_single_document(item_collection, temp_data)
    return {
        "msg": "Item registered",
    }


@router.post("/bulkUpload")
async def bulk_item_upload(file: UploadFile):
    """bulk register items from file"""

    data = await verify_file_upload(file)

    # if file.content_type == "text/csv":
    # items_array = read_csv.csv_reader(data)
    # await db_crud.add_multiple_documents(collection, items_array)

    items_array = read_csv.panda_reader(data, file)
    await db_crud.add_multiple_documents(item_collection, items_array)

    return {
        "msg": "Upload Successfully",
        "file": file.filename,
        "file_type": file.content_type,
    }


@router.delete("/thrashItem")
async def delete_item(serial_num: str):
    """deletes an item"""

    # checks from utils
    user = await db_crud.fetch_one(item_collection, serial_no=serial_num)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    await db_crud.remove_one_document(
        item_collection, serial_no=serial_num
    )

    return {"msg": "successful"}


@router.get(
    "/available",
    summary="returns all items available to borrow",
    response_model=List[models.Items],
)
async def available_items():
    """return all items available to borrow"""

    filter_conditions = {"is_available": {"$eq": 1}}
    documents = await db_crud.fetch_all_documents(
        item_collection, models.Items, filter_conditions
    )

    return documents


@router.post("/borrow", summary="borrows an item from store")
async def borrow_item(serial_num: str, user_email: EmailStr, firm: str):
    """borrows an item from the store"""

    document = await check_item(serial_num)
    item_meta_data = {
        "borrowed_by": user_email,
        "borrowed_at": datetime.utcnow(),
        "organization": firm,
        "returned": False,
    }

    document.update(item_meta_data)
    await db_crud.add_single_document(borrowed_collection, document)

    await item_collection.find_one_and_update(
        {"serial_no": serial_num}, {"$set": {"is_available": False}}
    )

    return {"status": "successful"}


@router.patch("/returnItem", summary="marks a borrowed item returned")
async def return_item(serial_num: str):
    """returns an items"""

    await borrowed_collection.find_one_and_update(
        {"serial_no": serial_num},
        {"$set": {"returned": True, "returned_at": datetime.utcnow()}},
    )

    await item_collection.find_one_and_update(
        {"serial_no": serial_num}, {"$set": {"is_available": True}}
    )

    return {"status": "successfull"}


@router.get(
    "/borrowedItems",
    summary="returns all borrowed items",
    # response_model=List[models.BorrowedItems],
)
async def all_borrowed_items():
    """returns all borrowed items"""

    documents = await db_crud.fetch_all_documents(
        borrowed_collection, models.Items
    )

    return documents


async def verify_file_upload(file: UploadFile):
    """verify's the integrity of uploaded file and returns the binary data"""

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="file type not allowed",
        )

    data = await file.read()
    if len(data) > (1024 * 1024 * 3):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="file size greater than 3mb",
        )

    return data


async def check_item(serial_num) -> dict:
    """checks the serial number if it matches any existing document and returns it"""

    document = await db_crud.fetch_one(
        item_collection, serial_no=serial_num
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid serial number",
        )

    if document["condition"] != "good" or not document["is_available"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="item not available for use",
        )

    return document
