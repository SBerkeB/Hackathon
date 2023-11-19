from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


import database
# import auth.user_access as user_access
import endpoints
import twitter_auth
#import os


CFG = dotenv_values(".env")


app = FastAPI()

origins = ["null", "http://127.0.0.1:5500"]
app.add_middleware(CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

app.include_router(database.router)
# app.include_router(user_access.router)
app.include_router(endpoints.router)
app.include_router(twitter_auth.router)







@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(CFG["DB_URL"])
    app.database = app.mongodb_client[CFG["DB_NAME"]]
    print("Connected to the MongoDB database!")

    
    
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
