from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

import pytz
import ast

import user_db
import verify_db
import mainpage
import auth


TWITTER_ACCESS = 30
config = dotenv_values(".env")
istanbul_tz = pytz.timezone('Europe/Istanbul')



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = ["null", "http://127.0.0.1:5500"]
app.add_middleware(CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

app.include_router(user_db.router)
app.include_router(verify_db.router)
app.include_router(mainpage.router)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(db_url)
    app.database = app.mongodb_client[db_name]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    

@app.get("/login", status_code=status.HTTP_200_OK)
async def FunctionName(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
    

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    print(env_db)
    user = auth.authenticate_user(ast.literal_eval(env_db), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    current_time_utc = datetime.utcnow()
    current_time_utc = pytz.utc.localize(current_time_utc)
    current_time_istanbul = current_time_utc.astimezone(istanbul_tz)
    expiration_time = current_time_istanbul + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = expiration_time.strftime("%a, %d %b %Y %H:%M:%S %Z")
    
    # access_token_expires = datetime.now(istanbul_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # localized_expiration = istanbul_tz.localize(access_token_expires)
    # expiration = localized_expiration.strftime("%a, %d %b %Y %H:%M:%S %Z")
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    
    response = RedirectResponse(url="http://127.0.0.1:8000/mainpage", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=access_token, httponly=True, expires=expiration)
    return response

@app.get("/datedata")
async def getDateData(request: Request):
    users = list(request.app.database["users_db"].find({}, {'_id': False}, limit=0))
    object = {}
    for i in range(len(users)):
        date = str(users[i]["date"].year) +" "+ str(users[i]["date"].month) +" "+ str(users[i]["date"].day)
        if date not in object:
            object[date] = 1
        else:
            object[date] += + 1
    return object



@app.get("/accounttype")
async def getAccountType(request: Request):
    users = list(request.app.database["users_db"].find({}, {'_id': False}, limit=0))
    object = {}
    for i in range(len(users)):
        accountType = users[i]["username"]
        if accountType not in object:
            object[accountType] = 1
        else:
            object[accountType] += 1
            
    return object