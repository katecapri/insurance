from uuid import uuid4
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

from src.database.models import Rate, User


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_user = User
        self.model_rate = Rate

    async def create_user(self, name, email, password):
        new_user = self.model_user(
            id=uuid4(),
            name=name,
            email=email,
            password=password
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def get_user_by_email(self, email):
        query = select(self.model_user).where(self.model_user.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_rate_by_id(self, rate_id):
        query = select(self.model_rate).where(self.model_rate.id == rate_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_rate_by_date_and_type(self, date, cargo_type):
        query = select(self.model_rate).where(
            self.model_rate.date == date,
            self.model_rate.cargo_type == cargo_type
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def create_rate(self, date, cargo_type, rate):
        new_rate = self.model_rate(
            id=uuid4(),
            date=date,
            cargo_type=cargo_type,
            rate=rate
        )
        self.session.add(new_rate)
        await self.session.commit()
        return new_rate.id

    async def update_rate(self, rate_id, date, cargo_type, rate):
        try:
            query = update(self.model_rate).where(
                self.model_rate.id == rate_id
            ).values(
                date=date,
                cargo_type=cargo_type,
                rate=rate
            ).returning(self.model_rate)
            result = await self.session.execute(query)
            await self.session.commit()
            return result.scalars().one()
        except NoResultFound:
            return None

    async def delete_rate(self, rate_id):
        query = delete(self.model_rate).where(self.model_rate.id == rate_id)
        await self.session.execute(query)
        await self.session.commit()