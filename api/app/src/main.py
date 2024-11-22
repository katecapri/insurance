from typing import Annotated
from fastapi import FastAPI, Request, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer

from src.services.main_service import save_input_rates_to_base, get_insurance_cost_for_date_and_type, get_rate_by_id, \
    update_rate_by_id, delete_rate_by_id,  create_user, authenticate_user
from src.services.serializers import validate_date, Rate, SignUp, LogIn, validate_email
from src.services.token_service import decode_jwt
from src.services.kafka_service import aio_producer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


@app.on_event("startup")
async def startup_event():
    await save_input_rates_to_base()

@app.on_event("shutdown")
def shutdown_event():
    aio_producer.close()


@app.post("/auth/signup/", status_code=201)
async def signup_user(signup_user_info: SignUp):
    try:
        is_email_valid = validate_email(signup_user_info.email)
        if not is_email_valid:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Invalid email")
        user_id = await create_user(signup_user_info)
        if not user_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="User was not created")
        return {"user_id": str(user_id)}
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")


@app.post("/auth/login/", status_code=200)
async def login_user(login_user_info: LogIn):
    try:
        is_email_valid = validate_email(login_user_info.email)
        if not is_email_valid:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Invalid email")
        token = await authenticate_user(login_user_info.email, login_user_info.password)
        if not token:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                            content="Not authenticated")
        return token
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")

@app.get("/insurance_cost")
async def get_insurance_cost(date: str, cargo_type: str, declared_value: float) -> float:
    try:
        input_date = validate_date(date)
        if not input_date:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Invalid date. Correct date format: '%Y-%m-%d'.")
        is_correct, insurance_cost_or_error = await get_insurance_cost_for_date_and_type(input_date,
                                                                                         cargo_type, declared_value)
        if not is_correct:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=insurance_cost_or_error)
        return insurance_cost_or_error
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")


@app.get("/rate/{rate_id}")
async def get_rate(rate_id: str):
    try:
        rate = await get_rate_by_id(rate_id)
        if not rate:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Rate with such id doesn't exist.")
        return rate
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")

@app.post("/rate/{rate_id}")
async def update_rate(token: Annotated[str, Depends(oauth2_scheme)], rate_id: str, rate_info: Rate):
    try:
        user_id = decode_jwt(token)
        if not user_id:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                            content="Not authenticated")
        input_date = validate_date(rate_info.date)
        if not input_date:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Invalid date. Correct date format: '%Y-%m-%d'.")
        rate = await update_rate_by_id(rate_id, input_date, rate_info.cargo_type, rate_info.rate, user_id)
        if not rate:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Rate with such id doesn't exist.")
        return rate
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")

@app.delete("/rate/{rate_id}")
async def delete_rate(token: Annotated[str, Depends(oauth2_scheme)], rate_id: str):
    try:
        user_id = decode_jwt(token)
        if not user_id:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                            content="Not authenticated")
        await delete_rate_by_id(rate_id, user_id)
        return "OK"
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content="An unexpected error occurred. Contact your administrator.")
