# FastAPI CRUD + WebSocket – Projekt zaliczeniowy

## 📌 Opis projektu
Aplikacja jest kompletnym backendem demonstracyjnym zbudowanym w oparciu o **FastAPI**, **SQLAlchemy** oraz **SQLite**.  
Udostępnia:

- REST API z pełnym zestawem operacji **CRUD**
- Asynchroniczny **WebSocket**, który wysyła aktualne informacje o serwerze
- Integrację z bazą danych
- Pełne **type annotations** i dokumentację w docstringach
- Testy jednostkowe z wykorzystaniem **pytest**
- Możliwość uruchomienia w środowisku wirtualnym lub kontenerowym

---

## 📁 Struktura projektu
```bash
    fastapi_app/ 
        ├── app/    
            ├── init.py    
            ├── main.py    
            ├── database.py  
            ├── models.py   
            ├── schemas.py   
            ├── crud.py   
            └── config.py 
        ├── tests/    
            ├── init.py    
            ├── test_items.py    
            └── test_websocket.py 
        ├── requirements.txt 
        └── README.md
```
---

## 🚀 Uruchomienie aplikacji

### 1. Utworzenie środowiska wirtualnego

#### Windows:
```bash
  python -m venv .venv .venv\Scripts\activate
```
#### Linux / macOS:
```bash
  python3 -m venv .venv source .venv/bin/activate
```
---
### 2. Instalacja zależności
```bash
  pip install -r requirements.txt
```
---
### 3. Uruchomienie serwera
```bash
  uvicorn app.main:app --reload
```
---
Aplikacja będzie dostępna pod adresem:
http://localhost:8000
---

## 📚 Dokumentacja API

FastAPI generuje dokumentację automatycznie:

- Swagger UI:  
  http://localhost:8000/docs

- ReDoc:  
  http://localhost:8000/redoc

---

## 🔌 WebSocket

### WebSocket działa pod adresem:

```bash
  ws://localhost:8000/ws/server-info
```

---

#### Przykład testu w konsoli przeglądarki:

```js
let ws = new WebSocket("ws://localhost:8000/ws/server-info");
ws.onmessage = (msg) => console.log(msg.data);
```

---

#### Co sekundę pojawi się JSON:

```json
{
  "status": "ok",
  "datetime": "2026-01-13T12:34:56.789Z"
}
```

---

## 🧪 Testy jednostkowe
### Uruchamianie testów:

```bash
    pytest -q
```

---

### Testy obejmują:
- połączenie WebSocket

---

## 🛠 Technologie
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- pytest
- WebSockets
