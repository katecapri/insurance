import re
from pydantic import BaseModel
from datetime import datetime


class Rate(BaseModel):
    date: str
    cargo_type: str
    rate: float

class SignUp(BaseModel):
    name: str
    email: str
    password: str
    referrer_code: str | None = None


class LogIn(BaseModel):
    email: str
    password: str


def validate_email(email):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    is_valid = bool(re.match(email_validate_pattern, email))
    return is_valid


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return False

