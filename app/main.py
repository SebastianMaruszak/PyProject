# app/main.py
from datetime import datetime
from typing import Any, Dict, List

import asyncio
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

# Tworzenie tabel przy starcie aplikacji
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD API z WebSocket")


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    """
    Zwraca prostą stronę HTML z informacją o API.

    Returns:
        Treść HTML z opisem API i linkiem do dokumentacji.
    """
    return """
    <html>
        <head><title>FastAPI CRUD</title></head>
        <body>
            <h1>FastAPI CRUD + WebSocket</h1>
            <p>Dokumentacja: <a href="/docs">/docs</a></p>
            <p>WebSocket: <code>ws://localhost:8000/ws/server-info</code></p>
        </body>
    </html>
    """


# --------- REST API CRUD ---------


@app.post("/items/", response_model=schemas.ItemInDB, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
) -> schemas.ItemInDB:
    """
    Tworzy nowy element poprzez REST API.

    Args:
        item: Dane nowego elementu.
        db: Sesja bazy danych.

    Returns:
        Utworzony element.
    """
    db_item = crud.create_item(db, item)
    return schemas.ItemInDB.from_orm(db_item)


@app.get("/items/", response_model=List[schemas.ItemInDB])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.ItemInDB]:
    """
    Zwraca listę elementów.

    Args:
        skip: Liczba elementów do pominięcia.
        limit: Maksymalna liczba elementów do zwrócenia.
        db: Sesja bazy danych.

    Returns:
        Lista elementów z bazy.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return [schemas.ItemInDB.from_orm(item) for item in items]


@app.get("/items/{item_id}", response_model=schemas.ItemInDB)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> schemas.ItemInDB:
    """
    Zwraca pojedynczy element na podstawie identyfikatora.

    Args:
        item_id: Identyfikator elementu.
        db: Sesja bazy danych.

    Raises:
        HTTPException: Jeśli element nie istnieje.

    Returns:
        Pobrany element.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.ItemInDB.from_orm(db_item)


@app.put("/items/{item_id}", response_model=schemas.ItemInDB)
def update_item_endpoint(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db),
) -> schemas.ItemInDB:
    """
    Aktualizuje istniejący element.

    Args:
        item_id: Identyfikator elementu.
        item: Dane do aktualizacji.
        db: Sesja bazy danych.

    Raises:
        HTTPException: Jeśli element nie istnieje.

    Returns:
        Zaktualizowany element.
    """
    db_item = crud.update_item(db, item_id=item_id, item_in=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.ItemInDB.from_orm(db_item)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Usuwa element z bazy.

    Args:
        item_id: Identyfikator elementu.
        db: Sesja bazy danych.

    Raises:
        HTTPException: Jeśli element nie istnieje.
    """
    deleted = crud.delete_item(db, item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")


# --------- Asynchroniczny WebSocket ---------


@app.websocket("/ws/server-info")
async def websocket_server_info(websocket: WebSocket) -> None:
    """
    Utrzymuje połączenie WebSocket i okresowo wysyła informacje o serwerze.

    Wysyłane są dane w formacie JSON zawierające:
    - status
    - bieżącą datę i godzinę (UTC, ISO 8601)
    """
    await websocket.accept()
    try:
        while True:
            payload: Dict[str, Any] = {
                "status": "ok",
                "datetime": datetime.utcnow().isoformat(),
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        # Klient rozłączył się – kończymy pętlę
        return