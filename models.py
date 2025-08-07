from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    org_user_id: str
    name: str
    contact_no: str
    employee_code: str
    created_date: datetime
    valid_till: datetime
