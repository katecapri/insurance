import os
import json

import aiofiles
from datetime import datetime

from src.database.service import create_rate_in_base, get_rate_by_date_and_type_from_base, get_rate_by_id_from_base, \
    update_rate_in_base, delete_rate_from_base, get_user_by_email, create_user_in_base
from src.services.token_service import generate_jwt
from src.services.password_service import encrypt_password, check_password
from src.services.kafka_service import send_update_rate_message_to_kafka, send_delete_rate_message_to_kafka


def convert_rate_to_response(rate_obj):
    result = {
        "date": rate_obj.date.strftime('%Y-%m-%d'),
        "cargo_type": rate_obj.cargo_type,
        "rate": float(rate_obj.rate),
    }
    return result


async def create_user(user_info):
    user_with_email = await get_user_by_email(user_info.email)
    if user_with_email:
        print("User with such email already exists")
        return None

    encrypted_password = encrypt_password(user_info.password)
    user_info.password = encrypted_password.decode()
    new_user_id = await create_user_in_base(user_info)
    return new_user_id


async def authenticate_user(email, password):
    user_with_email = await get_user_by_email(email)
    if not user_with_email:
        print("User with such email not exists")
        return None

    is_password_valid = check_password(password, str.encode(user_with_email.password))
    if not is_password_valid:
        return None

    jwt = generate_jwt(user_with_email.id)
    return jwt


async def save_input_rates_to_base():
    try:
        async with aiofiles.open(os.getenv("INPUT_DATA_JSON_PATH"), mode='r') as f:
            rates_data = await f.read()
        rates_dict = json.loads(rates_data)
    except Exception:
        print(f"File for loading rates not found. Correct path: {os.getenv('INPUT_DATA_JSON_PATH')}")
        return
    try:
        for date_str, rates_info in rates_dict.items():
            for rate_info in rates_info:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                await create_rate_in_base(date, rate_info["cargo_type"], float(rate_info["rate"]))
    except Exception:
        print("Error loading rates data from file. Correct form: {'date': [{'cargo_type': 'type', 'rate': 'rate'}]}."
              "Date format: '%Y-%m-%d', rate format - float.")


async def get_insurance_cost_for_date_and_type(date, cargo_type, declared_value):
    rate = await get_rate_by_date_and_type_from_base(date, cargo_type)
    if not rate:
        return False, "No rate for this date and cargo_type"
    insurance_cost = rate.rate * declared_value
    return True, insurance_cost

async def get_rate_by_id(rate_id):
    rate = await get_rate_by_id_from_base(rate_id)
    return convert_rate_to_response(rate) if rate else None

async def update_rate_by_id(rate_id, date, cargo_type, rate, user_id):
    rate = await update_rate_in_base(rate_id, date, cargo_type, rate)
    if not rate:
        return
    send_update_rate_message_to_kafka(rate_id, date, cargo_type, rate.rate, user_id)
    return convert_rate_to_response(rate) if rate else None

async def delete_rate_by_id(rate_id, user_id):
    rate = await get_rate_by_id_from_base(rate_id)
    if not rate:
        return
    send_delete_rate_message_to_kafka(rate_id, rate.date, rate.cargo_type, rate.rate, user_id)
    await delete_rate_from_base(rate_id)