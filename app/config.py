# app/config.py
from typing import Final

#: Domyślny URL do bazy danych SQLite.
DATABASE_URL: Final[str] = "sqlite:///./test.db"