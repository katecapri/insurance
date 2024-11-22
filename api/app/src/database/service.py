from src.init_database import session_maker
from src.database.repository import Repository


async def create_rate_in_base(date, cargo_type, rate):
    async with session_maker() as session:
        repository = Repository(session)
        existing_rate = await repository.get_rate_by_date_and_type(date, cargo_type)
        if existing_rate:
            print(f"Rate for date {existing_rate.date.strftime('%Y-%m-%d')} "
                  f"for {existing_rate.cargo_type} type already exists in base.")
            return
        rate_id = await repository.create_rate(date, cargo_type, rate)
    return rate_id


async def get_rate_by_date_and_type_from_base(date, cargo_type):
    async with session_maker() as session:
        repository = Repository(session)
        rate = await repository.get_rate_by_date_and_type(date, cargo_type)
    return rate


async def get_rate_by_id_from_base(rate_id):
    async with session_maker() as session:
        repository = Repository(session)
        rate = await repository.get_rate_by_id(rate_id)
    return rate


async def update_rate_in_base(rate_id, date, cargo_type, rate):
    async with session_maker() as session:
        repository = Repository(session)
        rate = await repository.update_rate(rate_id, date, cargo_type, rate)
    return rate


async def delete_rate_from_base(rate_id):
    async with session_maker() as session:
        repository = Repository(session)
        await repository.delete_rate(rate_id)


async def get_user_by_email(user_email):
    async with session_maker() as session:
        repository = Repository(session)
        user = await repository.get_user_by_email(user_email)
    return user


async def create_user_in_base(user_info):
    async with session_maker() as session:
        repository = Repository(session)
        user_id = await repository.create_user(user_info.name, user_info.email, user_info.password)
    return user_id
