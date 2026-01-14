from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """
    Bazowy schemat elementu.

    Atrybuty:
        title: Tytuł elementu.
        description: Opcjonalny opis elementu.
    """
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """
    Schemat używany przy tworzeniu nowego elementu.
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schemat używany przy aktualizacji istniejącego elementu.

    Atrybuty:
        title: Opcjonalny nowy tytuł.
        description: Opcjonalny nowy opis.
    """
    title: Optional[str] = None
    description: Optional[str] = None


class ItemInDB(ItemBase):
    """
    Schemat reprezentujący element przechowywany w bazie.

    Atrybuty:
        id: Unikalny identyfikator elementu.
    """
    id: int

    class Config:
        orm_mode = True