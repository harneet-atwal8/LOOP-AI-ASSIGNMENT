from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestRequest(BaseModel):
    ids: List[int] = Field(..., min_items=1)
    priority: Priority

class BatchStatus(str, Enum):
    YET_TO_START = "yet_to_start"
    TRIGGERED = "triggered"
    COMPLETED = "completed"

class BatchResponse(BaseModel):
    batch_id: str
    ids: List[int]
    status: BatchStatus

class StatusResponse(BaseModel):
    ingestion_id: str
    status: str
    batches: List[BatchResponse]