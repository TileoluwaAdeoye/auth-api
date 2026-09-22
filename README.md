# Auth API

A secure API with user authentication — sign up, log in, log out — built with Python, FastAPI, and Supabase Auth as the Identity Provider. Protected routes verify a JWT bearer token before responding.

Part of the FlyRank AI Internship, Backend Track.

## Why Supabase

Rolling your own password hashing and token signing is a real security risk. Supabase handles account storage, password hashing, and JWT signing as a trusted Identity Provider — this server only ever forwards credentials to Supabase and verifies the tokens it hands back. No password is ever stored or hashed in this codebase.

## Setup

**1. Clone and install:**
```bash
git clone https://github.com/TileoluwaAdeoye/auth-api.git
cd auth-api
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```

**2. Create your own Supabase project:**
- Sign up free at [supabase.com](https://supabase.com), create a new project
- Under **Project Settings → API**, copy your **Project URL** and **anon key**
- Under **Authentication → Sign In / Providers → Email**, turn OFF "Confirm email" for easier local testing

**3. Set your environment variables** — copy `.env.example` to `.env` and fill in your real values:
```bash
cp .env.example .env
```


SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here
PORT=8000



**4. Run it:**
```bash
uvicorn main:app --reload
```

Server runs at **http://localhost:8000**
Interactive docs (Swagger UI) at **http://localhost:8000/docs**

## Endpoints

| Method | Path                  | Description                      | Auth required |
|--------|------------------------|-----------------------------------|-----------------|
| GET    | `/`                    | Server/connection health check     | No              |
| POST   | `/auth/signup`         | Create a new user account           | No              |
| POST   | `/auth/login`          | Log in, returns access + refresh token | No           |
| POST   | `/auth/logout`         | End the current session              | Yes (Bearer)     |
| GET    | `/public/info`         | Open, unprotected data                | No              |
| GET    | `/protected/profile`   | Current user's profile data            | Yes (Bearer)     |
| GET    | `/protected/dashboard` | Second protected route (proves middleware reuse) | Yes (Bearer) |

## Example requests

**Sign up:**


$ curl.exe -i -X POST http://localhost:8000/auth/signup -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"password123"}'

HTTP/1.1 201 Created
{"id":"29e4add2-...","email":"test@example.com", ...}



**Accessing a protected route without a token:**


$ curl.exe -i http://localhost:8000/protected/profile

HTTP/1.1 401 Unauthorized
{"error":"Access token required"}



**Accessing a protected route with a valid token:**


$ curl.exe -i http://localhost:8000/protected/profile -H "Authorization: Bearer <token>"

HTTP/1.1 200 OK
{"id":"29e4add2-...","email":"test@example.com","created_at":"2026-09-22T11:43:23.507996+00:00"}



## Swagger UI

Bearer auth configured with a padlock on every protected route — click "Authorize", paste a JWT, and test directly from the browser.

![Swagger UI screenshot](swagger-screenshot.png)

## Security notes

- `.env` is git-ignored; only `.env.example` (with placeholder values) is committed.
- The Supabase **anon key** is used here — never the `service_role` key, which bypasses all security and must stay server-side only.
- Every request to a protected route calls `supabase.auth.get_user(token)`, a real network call to Supabase — this means a tampered or expired token is always rejected, not just checked for shape.