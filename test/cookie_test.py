from fastapi import FastAPI

app = FastAPI()

@app.get()
async def func():
    response = RedirectResponse(url="http://127.0.0.1:8000/mainpage", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=access_token, httponly=True, expires=expiration)
    return response