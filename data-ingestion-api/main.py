import uuid
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum
from threading import Thread, Lock
from processor import BatchProcessor
from store import ingestion_store
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestRequest(BaseModel):
    ids: List[int] = Field(..., min_items=1)
    priority: Priority

@app.on_event("startup")
def start_background_worker():
    # Start the batch processor thread
    processor = BatchProcessor()
    processor.daemon = True
    processor.start()

@app.post("/ingest")
def ingest(req: IngestRequest):
    ingestion_id = str(uuid.uuid4())
    ids = req.ids
    priority = req.priority

    # Split into batches of 3
    batches = [ids[i:i+3] for i in range(0, len(ids), 3)]
    batch_entries = []
    now = time.time()
    for batch in batches:
        batch_id = str(uuid.uuid4())
        batch_entries.append({
            "batch_id": batch_id,
            "ids": batch,
            "status": "yet_to_start",
            "created_time": now,
            "priority": priority,
        })
    ingestion_store.add_ingestion(ingestion_id, priority, batch_entries, now)
    return JSONResponse({"ingestion_id": ingestion_id})

@app.get("/status/{ingestion_id}")
def get_status(ingestion_id: str):
    data = ingestion_store.get_ingestion(ingestion_id)
    if not data:
        raise HTTPException(status_code=404, detail="Ingestion not found")
    # Gather batch statuses
    batch_statuses = [batch["status"] for batch in data["batches"]]
    if all(s == "yet_to_start" for s in batch_statuses):
        overall = "yet_to_start"
    elif all(s == "completed" for s in batch_statuses):
        overall = "completed"
    elif any(s == "triggered" for s in batch_statuses):
        overall = "triggered"
    else:
        overall = "yet_to_start"
    return {
        "ingestion_id": ingestion_id,
        "status": overall,
        "batches": [
            {
                "batch_id": batch["batch_id"],
                "ids": batch["ids"],
                "status": batch["status"]
            }
            for batch in data["batches"]
        ]
    }