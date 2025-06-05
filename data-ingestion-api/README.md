# Data Ingestion API

A simple RESTful API for asynchronous, rate-limited data ingestion with prioritization.

## Endpoints

- `POST /ingest`  
  Submit a job with a list of IDs and a priority (HIGH, MEDIUM, LOW).  
  Response: `{ "ingestion_id": "<uuid>" }`

- `GET /status/<ingestion_id>`  
  Query the status of a previously submitted ingestion job.

## Features

- Processes IDs in batches of 3, max 1 batch every 5 seconds.
- Respects job priority (`HIGH` > `MEDIUM` > `LOW`).
- Batch and overall status tracking.
- Fully async background processing, safe to run with Uvicorn/Gunicorn.
- No external dependencies except FastAPI and standard lib.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing

```bash
pytest test_app.py
```

## Design Choices

- **FastAPI** for async & rapid prototyping.
- **Threading** for the batch processor, but can be upgraded to Celery.
- **In-memory store** for demo; swap to Redis/DB for production.
- **No authentication** as required by the assignment.

## Screenshot

![Screenshot 2025-06-05 124130](https://github.com/user-attachments/assets/3f6e8f0d-057e-48e8-8b74-b46116308bb1)
![Screenshot 2025-06-05 124121](https://github.com/user-attachments/assets/9b335ed0-76ba-4cf9-a903-b959afa02cff)

## Hosted Demo

> Your hosted URL here (e.g., https://loop-ai-assignment-9t3d.onrender.com/)
