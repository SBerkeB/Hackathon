from fastapi import APIRouter, Cookie
from typing import Optional

router = APIRouter()

@router.get("/get_cookie")
async def getCookie(authorization: Optional[str] = Cookie(None)):
    return authorization