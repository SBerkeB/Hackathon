from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx

app = FastAPI()

# Load your Worldcoin API credentials from a .env file or your environment variables
# Make sure to replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Worldcoin API credentials
import os
from dotenv import load_dotenv

app = FastAPI()

# Load your Worldcoin API credentials from a .env file or your environment variables
# Make sure to replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Worldcoin API credentials
import os
from dotenv import load_dotenv

load_dotenv()

WORLDCOIN_CLIENT_ID = os.getenv("WORLDCOIN_CLIENT_ID")
WORLDCOIN_CLIENT_SECRET = os.getenv("WORLDCOIN_CLIENT_SECRET")
WORLDCOIN_AUTH_URL = "https://worldcoinindex.com/apiservice/oauth"
WORLDCOIN_TOKEN_URL = "https://worldcoinindex.com/apiservice/oauth/access_token"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=WORLDCOIN_AUTH_URL,
    tokenUrl=WORLDCOIN_TOKEN_URL,
)

async def get_worldcoin_user(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            WORLDCOIN_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": token,
                "client_id": WORLDCOIN_CLIENT_ID,
                "client_secret": WORLDCOIN_CLIENT_SECRET,
            },
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Worldcoin authentication error")
        
        worldcoin_user = response.json()
        return worldcoin_user

@app.get("/users/me", response_model=dict)
async def read_users_me(current_user: dict = Depends(get_worldcoin_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
