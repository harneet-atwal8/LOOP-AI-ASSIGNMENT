import threading

class IngestionStore:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def add_ingestion(self, ingestion_id, priority, batches, created_time):
        with self.lock:
            self.store[ingestion_id] = {
                "priority": priority,
                "created_time": created_time,
                "batches": batches
            }

    def get_ingestion(self, ingestion_id):
        with self.lock:
            return self.store.get(ingestion_id)

    def update_batch(self, ingestion_id, batch_idx, batch_data):
        with self.lock:
            if ingestion_id in self.store and 0 <= batch_idx < len(self.store[ingestion_id]["batches"]):
                self.store[ingestion_id]["batches"][batch_idx] = batch_data

# ✅ Singleton instance to be used across the app
ingestion_store = IngestionStore()
