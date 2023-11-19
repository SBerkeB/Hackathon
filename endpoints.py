from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="html")


router = APIRouter(prefix="/ep", tags=["endpoints"])

# @router.get("/main_page")
# async def mainPage():
    
    
@router.get("/login", status_code=status.HTTP_200_OK)
async def loginPage(request: Request):
    return templates.TemplateResponse("login.html", { "request": request })


@router.get("/main", status_code=status.HTTP_200_OK)
async def mainPage(request: Request):
    return templates.TemplateResponse("main.html", { "request": request })


@router.get("/profile", status_code=status.HTTP_200_OK)
async def profilePage(request: Request):
    return templates.TemplateResponse("profile.html", { "request": request })


@router.get("/explore", status_code=status.HTTP_200_OK)
async def explorePage(request: Request):
    return templates.TemplateResponse("explore.html", { "request": request })


@router.get("/notifications", status_code=status.HTTP_200_OK)
async def notificationsPage(request: Request):
    return templates.TemplateResponse("notifications.html", { "request": request })


@router.get("/otp", status_code=status.HTTP_200_OK)
async def otpPage(request: Request):
    return templates.TemplateResponse("otp.html", { "request": request })
    

# @router.get("/username", status_code=status.HTTP_200_OK)
# async def defineUsername(request: Request):
#     return templates.TemplateResponse("login.html", { "request": request })