from typing import Optional

from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Item(Base):
    """
    Model reprezentujący element w bazie danych.

    Atrybuty:
        id: Unikalny identyfikator elementu.
        title: Krótki tytuł elementu.
        description: Opcjonalny opis elementu.
    """
    __tablename__ = "items"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(100), index=True, nullable=False)
    description: Optional[str] = Column(Text, nullable=True)