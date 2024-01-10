from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Union


class UserData(BaseModel):
    """the response data model for users"""

    name: str
    email: EmailStr
    mobile_no: str
    role: str
    department: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "salama ayuba",
                "email": "salamaayuba111@gmail.com",
                "mobile_no": "+2348136342967",
                "role": "admin",
                "department": "art",
            }
        }


class Users(UserData, BaseModel):
    """the nongoDB user schema"""

    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "salama ayuba",
                "email": "salamaayuba111@gmail.com",
                "mobile_no": "+2348136342967",
                "role": "admin",
                "department": "art",
                "password": "your_Password_Here",
            }
        }


class Items(BaseModel):
    item_name: str
    category: str
    model: str
    asset_no: int
    serial_no: str
    is_available: bool
    condition: str

    class Config:
        json_schema_extra = {
            "example": {
                "item_name": "itel s23",
                "category": "mobile phone",
                "model": "SCVDVBCN-234",
                "asset_no": "1234321",
                "serial_no": "dha12345678d9",
                "is_available": True,
                "condition": "Brand New",
            }
        }


class BorrowedItems(Items, BaseModel):
    borrowed_by: EmailStr
    borrowed_at: datetime
    organization: str
    returned: bool
    returned_at: datetime = None

    class Config:
        json_schema_extra = {
            "example": {
                "item_name": "itel s23",
                "category": "mobile phone",
                "model": "SCVDVBCN-234",
                "asset_no": "1234321",
                "serial_no": "dha12345678d9",
                "is_available": True,
                "condition": "Brand New",
                "borrowed_by": "user@example.com",
                "borrowed_at": "2024-01-12T15:34",
                "organization": "Nestle PLC",
                "returned": True,
                "returned_at": "2024-01-13T13:45",
            }
        }
