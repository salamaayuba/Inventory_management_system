from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(prefix="/auth", tags=["Authentication"])

from auth import forgot_password, login, logout, send_email_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
