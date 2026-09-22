import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server running and connected to Supabase"}

print("Server running and connected to Supabase")
