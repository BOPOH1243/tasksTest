from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from db import Base
import sqlalchemy.types as types

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
