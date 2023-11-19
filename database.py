from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from dataclasses import dataclass
from dotenv import dotenv_values


import os
import json
import jwt


CFG = dotenv_values(".env")

@dataclass
class User():
    twitterAt: str
    username: str
    followerCount: int
    followingCount: int
    holdersCount: int
    confirmed: bool = False

router = APIRouter(prefix="/db",
                   tags=["database"])




@router.post("/db_check/{twitterAt}")
async def dbCheck(request: Request, twitterAt):
    if request.app.database["users"].find_one({"twitterAt": twitterAt}):
        return json.dumps({"success": True,
                           "action": "found"})
    elif request.app.database["users"].insert_one({"twitterAt": twitterAt,
                                                   "username": "",
                                                   "followerCount": 0,
                                                   "followingCount": 0,
                                                   "holdersCount": 0}):
        return json.dumps({"success": True,
                           "action": "create"})
    else:
        return json.dumps({"success": False,
                           "action": ""})


@router.get("/get_user_data/{twitterAt}")
async def getUserData(request: Request, twitterAt):
    found = request.app.database["users"].find_one({"twitterAt": twitterAt})
    
    if found:
        return json.dumps({"success": True,
                          "action": "found",
                          "data": found})
    else:
        return json.dumps({"success": False,
                           "action": ""})
        

@router.post("/set_user_data/{username}")
async def setUserData(request: Request, username):
    newvalues = { "$set": { 'username': username } }
    isSet = request.app.database["users"].update_one({"twitterAt": username})