from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from models import User
from utils import generate_org_id, generate_api_key
from storage import db
from datetime import datetime
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import json   # ✅ Fix for Java template

# Optional: Serve static files (for frontend chatbot)
# app.mount("/static", StaticFiles(directory="static"), name="static"))

app = FastAPI()

# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        return open("templates/index.html").read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="index.html not found")

@app.get("/generate_org")
def generate_org(name: str):
    org_id = generate_org_id(name)
    api_key = generate_api_key()
    base_url = f"/api/org/{org_id}/users/"

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
    if org_id in db and org_user_id in db[org_id]:
        del db[org_id][org_user_id]
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

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

# ----------------------------
# ✅ NEW ENDPOINT: Generate from Postman Collection
# ----------------------------
class PostmanRequest(BaseModel):
    postman: Dict[str, Any]
    language: str

@app.post("/generate_from_postman")
def generate_from_postman(req: PostmanRequest):
    try:
        item = req.postman["item"][0]   # First API in collection
        name = item.get("name", "Unknown Endpoint")
        request_data = item.get("request", {})

        method = request_data.get("method", "GET")
        url = request_data.get("url", {}).get("raw", "http://example.com")

        headers_dict = {}
        body = ""
        if "header" in request_data:
            headers_dict = {h["key"]: h["value"] for h in request_data["header"]}
        if "body" in request_data and "raw" in request_data["body"]:
            body = request_data["body"]["raw"]

        # ---------- Python (FastAPI) ----------
        if req.language == "Python (FastAPI)":
            code = f"""import requests

url = "{url}"
headers = {headers_dict}

payload = {body if body else "{}"}

response = requests.{method.lower()}(url, headers=headers, json=payload)
print(response.status_code, response.text)
"""

        # ---------- Node.js (Express) ----------
        elif req.language == "Node.js (Express)":
            code = f"""const axios = require('axios');

const url = "{url}";
const headers = {json.dumps(headers_dict)};

axios.{method.lower()}(url, {body if body else "{}"}, {{ headers }})
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
"""

        # ---------- Go ----------
        elif req.language == "Go":
            code = f"""package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "io/ioutil"
)

func main() {{
    url := "{url}"
    payload := []byte(`{body if body else "{}"}`)

    req, _ := http.NewRequest("{method.upper()}", url, bytes.NewBuffer(payload))
    req.Header.Set("Content-Type", "application/json")

    for key, value := range map[string]string{json.dumps(headers_dict)} {{
        req.Header.Set(key, value)
    }}

    client := &http.Client{{}}
    resp, err := client.Do(req)
    if err != nil {{
        panic(err)
    }}
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(body))
}}
"""

        # ---------- Java (Spring Boot) ----------
        elif req.language == "Java (Spring Boot)":
            body_dict = {}
            try:
                if body:
                    body_dict = json.loads(body)
            except Exception:
                body_dict = {}

            headers_code = "".join([f'headers.set("{k}", "{v}");\n        ' for k,v in headers_dict.items()])
            payload_code = ", ".join([f'Map.entry("{k}", "{v}")' for k,v in body_dict.items()])

            code = f"""import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import java.util.*;

public class ApiClient {{
    public static void main(String[] args) {{
        String url = "{url}";

        RestTemplate restTemplate = new RestTemplate();
        Map<String, Object> payload = new HashMap<>();
        payload.putAll(Map.ofEntries(
            {payload_code}
        ));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        {headers_code}

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);

        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.{method.upper()}, entity, String.class);
        System.out.println(response.getBody());
    }}
}}
"""

        else:
            code = f"// {req.language} template not implemented yet."

        return {"generated_code": code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
