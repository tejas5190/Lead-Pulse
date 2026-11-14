"""
Seed the running LeadPulse AI server with realistic demo data.
"""
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def post(url, data, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {token}"} if token else {})
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def get(url, token=None):
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"} if token else {}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# 1. Register or Login
print("Registering demo account...")
try:
    auth_data = post(f"{BASE_URL}/auth/register", {
        "company_name": "Skyline Apex Properties",
        "industry": "real_estate",
        "email": "demo@skylineapex.com",
        "password": "Password123!"
    })
    token = auth_data["access_token"]
except Exception:
    print("Already registered, logging in...")
    auth_data = post(f"{BASE_URL}/auth/login", {
        "email": "demo@skylineapex.com",
        "password": "Password123!"
    })
    token = auth_data["access_token"]

print("Authenticated! Token acquired.")

# 2. Create Project
print("Creating project...")
try:
    project = post(f"{BASE_URL}/api/projects", {
        "name": "Greenfield Signature 3BHK",
        "qualification_rules": {
            "questions": [
                {"question": "Are you looking for 2BHK or 3BHK luxury apartments?", "pass_criteria": "2BHK or 3BHK", "is_required": True},
                {"question": "Our units start at ₹85 Lakhs. Does this match your planned budget?", "pass_criteria": ">= ₹85L", "is_required": True},
                {"question": "Are you looking for ready-to-move-in or under construction?", "pass_criteria": "Within 12 months", "is_required": True},
                {"question": "Would you like to schedule a private sample flat tour this Saturday?", "pass_criteria": "Book slot", "is_required": True}
            ],
            "greeting_message": "Namaste! Welcome to Greenfield Signature. Are you looking in the ₹85L+ range?",
            "ai_personality": "polite_professional",
            "language": "en+hi"
        }
    }, token)
    print(f"Project created: {project['name']} (ID: {project['id']})")
except Exception as e:
    print("Project may already exist:", e)

print("Demo environment successfully seeded!")
