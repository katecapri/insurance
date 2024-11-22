from uuid import uuid4
from sqlalchemy import MetaData, Column, String, DateTime, Float
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = 'users'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    password = Column(String(), nullable=False)


class Rate(Base):
    __tablename__ = 'rates'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    date = Column(DateTime(), nullable=False)
    cargo_type = Column(String(), nullable=False)
    rate = Column(Float(), nullable=False)