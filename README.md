# ⚽ Soccer Events API (FastAPI + SportsDB)

A FastAPI backend service that aggregates **soccer match events** and their **timelines** from the SportsDB API. The service supports **date-based retrieval** (defaults to today) and returns **frontend-ready** data including scores, match status, kickoff time, live minute, team badges, and event timelines.

---

## ✨ Features

- Fetch soccer events **by date** (defaults to today)
- Aggregate **event + timeline** data
- Match details:
  - Home & away teams
  - Scores
  - Match status (NS, LIVE, HT, FT, etc.)
  - Live minute (computed)
  - Kickoff time (UTC)
  - Minutes to kickoff (for upcoming matches)
  - Team badges
- Clean, normalized responses
- Auto-generated API docs (Swagger & ReDoc)

---

## 🧱 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **httpx** (async HTTP client)
- **SportsDB API**

---

## 📂 Project Structure

```
react-test-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── events.py
│   └── services/
│       ├── __init__.py
│       └── sportsdb.py
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd react-test-backend
```

---

### 2️⃣ Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate
```

or (Conda)

```bash
conda create -n soccer-api python=3.11
conda activate soccer-api
```

---

### 3️⃣ Install dependencies

```bash
pip install fastapi uvicorn httpx
```

---

### 4️⃣ Configure SportsDB API key

Edit `app/services/sportsdb.py`:

```python
API_KEY = "YOUR_SPORTSDB_API_KEY"
```

---

### 5️⃣ Run the server

From the **project root**:

```bash
uvicorn app.main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI auto-generates documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🔗 API Endpoints

### 1️⃣ Get soccer events by date (defaults to today)

```
GET /events/today
```

Optional query parameter:

```
GET /events/today?date=YYYY-MM-DD
```

**Example**

```
GET /events/today?date=2025-12-13
```

---

### 2️⃣ Get a single event by ID

```
GET /events/{event_id}
```

---

## 📦 Example Response

```json
{
  "id": "2104567",
  "home_team": "Arsenal",
  "away_team": "Man City",
  "home_badge": "https://www.thesportsdb.com/images/media/team/badge/arsenal.png",
  "away_badge": "https://www.thesportsdb.com/images/media/team/badge/mancity.png",
  "home_score": 2,
  "away_score": 1,
  "status": "LIVE",
  "minute": 67,
  "kickoff_time_utc": "2025-12-13T19:30:00Z",
  "minutes_to_kickoff": null,
  "timeline": [
    {
      "time": "23'",
      "event": "Goal",
      "player": "Saka"
    }
  ]
}
```

---

## 🧠 Data Normalization

### Match Status

Raw SportsDB statuses are normalized to:

- `NS` – Not Started
- `LIVE` – Live
- `HT` – Half Time
- `FT` – Full Time
- `AET` – After Extra Time
- `PEN` – Penalties
- `POSTPONED` – Postponed

---

### Match Minute

- Computed from kickoff time
- Calculated only for `LIVE` / `HT`
- Clamped to realistic bounds

---

### Kickoff Time

- Stored and returned in **UTC**
- Frontend should convert to local time

---

## 🧪 Local Testing

```bash
curl http://127.0.0.1:8000/events/today
```

```bash
curl http://127.0.0.1:8000/events/today?date=2025-12-15
```

---

## 🔮 Future Enhancements

- Redis caching (per date & live matches)
- League / country filters
- Live polling optimization
- WebSocket live updates
- Persistent team metadata cache
- Dockerized deployment

---

## 📄 License

For internal, educational, or prototype use. Refer to SportsDB API terms for data usage and redistribution.

