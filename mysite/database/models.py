from .db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, Date
from typing import Optional
from enum import Enum as PyEnum
from datetime import date

class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'user_profiles'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    ddate_registered: Mapped[date] = mapped_column(Date, default=date.today)