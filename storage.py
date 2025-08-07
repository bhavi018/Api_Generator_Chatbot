# storage.py
from typing import Dict
from models import User

# Structure: { org_id: { org_user_id: User } }
db: Dict[str, Dict[str, User]] = {}

# # Store API keys per organization
# # Structure: { org_id: api_key }
# api_keys: Dict[str, str] = {}
