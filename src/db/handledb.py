from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()

class User(Base):
    __tablename__ = 'accounts_user'
    email = Column(String(50),primary_key=True, index=True)


