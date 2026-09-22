import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

class AuthRequest(BaseModel):
    email: str = None
    password: str = None

@app.get("/")
def read_root():
    return {"message": "Server running and connected to Supabase"}

@app.post("/auth/signup", status_code=201)
def signup(payload: AuthRequest):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="email and password are required")

    result = supabase.auth.sign_up({
        "email": payload.email,
        "password": payload.password
    })
    return result.user

@app.post("/auth/login")
def login(payload: AuthRequest):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="email and password are required")

    try:
        result = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token
    }

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer ") or len(auth_header.split(" ")) != 2:
        raise HTTPException(status_code=401, detail="Access token required")

    token = auth_header.split(" ")[1]

    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = user_response.user
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }