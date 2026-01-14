from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    """
    Tworzy nowy element w bazie danych.

    Args:
        db: Sesja bazy danych.
        item_in: Dane elementu do utworzenia.

    Returns:
        Nowo utworzony obiekt Item.
    """
    db_item = models.Item(title=item_in.title, description=item_in.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Pobiera pojedynczy element po identyfikatorze.

    Args:
        db: Sesja bazy danych.
        item_id: Identyfikator elementu.

    Returns:
        Obiekt Item lub None, jeśli nie znaleziono.
    """
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Pobiera listę elementów z bazy.

    Args:
        db: Sesja bazy danych.
        skip: Liczba elementów do pominięcia.
        limit: Maksymalna liczba elementów do zwrócenia.

    Returns:
        Lista obiektów Item.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def update_item(
    db: Session, item_id: int, item_in: schemas.ItemUpdate
) -> Optional[models.Item]:
    """
    Aktualizuje istniejący element w bazie danych.

    Args:
        db: Sesja bazy danych.
        item_id: Identyfikator elementu.
        item_in: Dane do aktualizacji.

    Returns:
        Zaktualizowany obiekt Item lub None, jeśli element nie istnieje.
    """
    db_item = get_item(db, item_id)
    if db_item is None:
        return None

    if item_in.title is not None:
        db_item.title = item_in.title
    if item_in.description is not None:
        db_item.description = item_in.description

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    """
    Usuwa element z bazy danych.

    Args:
        db: Sesja bazy danych.
        item_id: Identyfikator elementu.

    Returns:
        True, jeśli element został usunięty, False w przeciwnym wypadku.
    """
    db_item = get_item(db, item_id)
    if db_item is None:
        return False

    db.delete(db_item)
    db.commit()
    return True