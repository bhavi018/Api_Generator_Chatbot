from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from models import User
from utils import generate_org_id, generate_api_key
from storage import db
from datetime import datetime
from fastapi.responses import HTMLResponse

from fastapi import Request
from fastapi.responses import JSONResponse

# import openai

# Optional: Serve static files (for frontend chatbot)
# app.mount("/static", StaticFiles(directory="static"), name="static")


# Load OpenAI key from .env
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        return open(
            "templates/index.html"
        ).read()  # ✅ FIX: try-except must wrap the whole logic
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="index.html not found")


@app.get("/generate_org")
def generate_org(name: str):
    org_id = generate_org_id(name)
    api_key = generate_api_key()
    base_url = f"/api/org/{org_id}/users/"

    # Initialize empty dict for this org
    if org_id not in db:
        db[org_id] = {}

    return {
        "message": "Org Created Successfully!",
        "organization_name": name,
        "org_id": org_id,
        "api_key": api_key,
        "base_url": base_url,
        "sample_endpoints": {
            "POST": base_url,
            "GET": base_url + "{org_user_id}",
            "PUT": base_url + "{org_user_id}",
            "DELETE": base_url + "{org_user_id}",
        },
    }


@app.post("/api/org/{org_id}/users/")
def create_user(org_id: str, user: User):
    if org_id not in db:
        raise HTTPException(status_code=404, detail="Organization not found")
    if user.org_user_id in db[org_id]:
        raise HTTPException(status_code=400, detail="User already exists")
    db[org_id][user.org_user_id] = user
    return {"message": "User created", "user": user}


@app.get("/api/org/{org_id}/users/{org_user_id}")
def get_user(org_id: str, org_user_id: str):
    if org_id not in db or org_user_id not in db[org_id]:
        raise HTTPException(status_code=404, detail="User not found")
    return db[org_id][org_user_id]


@app.put("/api/org/{org_id}/users/{org_user_id}")
def update_user(org_id: str, org_user_id: str, updated_user: User):
    if org_id not in db or org_user_id not in db[org_id]:
        raise HTTPException(status_code=404, detail="User not found")
    db[org_id][org_user_id] = updated_user
    return {"message": "User updated", "user": updated_user}


@app.delete("/api/org/{org_id}/users/{org_user_id}")
def delete_user(org_id: str, org_user_id: str):
    if org_id not in db or org_user_id not in db[org_id]:
        raise HTTPException(status_code=404, detail="User not found")
    del db[org_id][org_user_id]
    return {"message": "User deleted"}


@app.get("/generate_sample_code")
def generate_sample_code(org_id: str, org_name: str):
    code = f"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

app = FastAPI()

# In-memory DB
db: Dict[str, Dict[str, User]] = {{}}

class User(BaseModel):
    org_user_id: str
    name: str
    contact_no: str
    employee_code: str
    created_date: datetime
    valid_till: datetime

@app.get("/process")
def process(name: str = "world"):
    return {{"message": f"Hello, {{name}}!"}}

@app.post("/api/org/{org_id}/users/")
def create_user(user: User):
    if "{org_id}" not in db:
        db["{org_id}"] = {{}}
    if user.org_user_id in db["{org_id}"]:
        raise HTTPException(status_code=400, detail="User already exists")
    db["{org_id}"][user.org_user_id] = user
    return {{"message": "User created", "user": user}}

@app.get("/api/org/{org_id}/users/{{org_user_id}}")
def get_user(org_user_id: str):
    if "{org_id}" not in db or org_user_id not in db["{org_id}"]:
        raise HTTPException(status_code=404, detail="User not found")
    return db["{org_id}"][org_user_id]

@app.put("/api/org/{org_id}/users/{{org_user_id}}")
def update_user(org_user_id: str, updated_user: User):
    if "{org_id}" not in db or org_user_id not in db["{org_id}"]:
        raise HTTPException(status_code=404, detail="User not found")
    db["{org_id}"][org_user_id] = updated_user
    return {{"message": "User updated", "user": updated_user}}

@app.delete("/api/org/{org_id}/users/{{org_user_id}}")
def delete_user(org_user_id: str):
    if "{org_id}" in db and org_user_id in db["{org_id}"]:
        del db["{org_id}"][org_user_id]
        return {{"message": "User deleted"}}
    raise HTTPException(status_code=404, detail="User not found")
"""
    return {"org_id": org_id, "org_name": org_name, "generated_code": code}
