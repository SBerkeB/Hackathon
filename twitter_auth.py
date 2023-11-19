
import utility.Config as Config
from utility.TwitterUtil import TwitterUtil
import utility.ErrorResponse as ErrorResponse
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, status, Cookie, Form, Depends
from dataclasses import dataclass
from pydantic import BaseModel


import tweepy
import webbrowser




router = APIRouter(tags=["auth"])

twitter = TwitterUtil(Config.KEYS.TW_API_KEY, Config.KEYS.TW_API_SEC)

class Otp(BaseModel):
    otp: str


@router.get('/request_token/{oauth_callback}')
def request_token(oauth_callback):
    
    
    data = ""
    
    try:
        data =  twitter.request_token(oauth_callback)
        
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_request_invalid
    except Exception:
        raise ErrorResponse.tw_request_invalid
    
    webbrowser.open_new_tab("https://api.twitter.com/oauth/authenticate?oauth_token=" + data["oauth_token"])
    
    response = RedirectResponse(url="http://127.0.0.1:8000/otp", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=data, httponly=True, expires=1320)
    return response


@router.get('/access_token')
def access_token(request: Request, otpassword: Otp = Form(...)):
    print(otpassword)
    print("oauth_verifier")
    print(request.cookies.get("Authorization")["oauth_token"])
    try:
        return twitter.access_token(request.cookies.get("Authorization")["oauth_token"], otpassword)
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_access_invalid
