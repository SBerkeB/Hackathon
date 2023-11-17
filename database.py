from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from dataclasses import dataclass
from dotenv import dotenv_values
# from cryptography.fernet import Fernet


import os
import json
import jwt


CFG = dotenv_values(".env")
# fernet = Fernet("a2Wn5KsaXtzTFfDAlQuxeRZQqmdnhIBrkkNUwNgLZdk=")

@dataclass
class User():
    username: str
    twitterAt: str
    balance: float
    followerCount: int
    followingCount: int
    holdersCount: int
    buyPrice: int
    sellPrice: int

router = APIRouter(prefix="/db")


# def writeToDB(object, db):
#     if db.insert_one(object)


@router.post("/db_check")
async def db_check(request: Request, user: User = Depends()):
    if request.app.database["users"].find_one({"twitterAt": user.twitterAt}):
        return json.dumps({"success": True,
                           "action": "found"})
    elif request.app.database["users"].insert_one(user.__dict__):
        return json.dumps({"success": True,
                           "action": "create"})
    else:
        return json.dumps({"success": False,
                           "action": "false"})



# @router.get("/write_to_db/{encoded_jwt}")
# async def write_to_db(request: Request, encoded_jwt):
    
#     decoded = jwt.decode(encoded_jwt, CFG["JWT_SECRET"], algorithms=["256"])
    
#     db_object = {
#         "username": decoded["username"],
#         "twitterAt": decoded["twitterAt"],
#         "balance": decoded["balance"],
#         "followerCount": decoded["followerCount"],
#         "followingCount": decoded["followingCount"],
#         "holdersCount": decoded["holdersCount"],
#         "buyPrice": decoded["buyPrice"],
#         "sellPrice": decoded["sellPrice"]
#     }
    
#     print(db_object)
    
#     created = request.app.database["users"].insert_one(db_object)
    
#     if created:
#         return json.dumps({"success": True,
#                            "action": "create"})
#     else:
#         return json.dumps({"success": False,
#                            "action": "create"})