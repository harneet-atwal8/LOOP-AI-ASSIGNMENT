import threading
import time
import uuid
from store import ingestion_store

PRIORITY_ORDER = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

class BatchProcessor(threading.Thread):
    def run(self):
        while True:
            
            jobs = []
            for ingestion_id, data in ingestion_store.store.items():
                for idx, batch in enumerate(data["batches"]):
                    if batch["status"] == "yet_to_start":
                        jobs.append({
                            "ingestion_id": ingestion_id,
                            "priority": batch["priority"],
                            "created_time": batch["created_time"],
                            "batch_idx": idx
                        })
            
            jobs.sort(key=lambda x: (PRIORITY_ORDER[x["priority"]], x["created_time"]))
            if jobs:
                job = jobs[0]
                ingestion_id = job["ingestion_id"]
                idx = job["batch_idx"]
                batch = ingestion_store.store[ingestion_id]["batches"][idx]
                batch["status"] = "triggered"
                ingestion_store.update_batch(ingestion_id, idx, batch)
                
                for id_ in batch["ids"]:
                    time.sleep(0.5)  # simulate API call
                batch["status"] = "completed"
                ingestion_store.update_batch(ingestion_id, idx, batch)
                time.sleep(5) 
            else:
                time.sleep(1)
