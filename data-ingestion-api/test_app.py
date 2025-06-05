import pytest
from fastapi.testclient import TestClient
import time

from main import app

client = TestClient(app)

def test_ingest_and_status():
    
    resp = client.post("/ingest", json={"ids": [1,2,3,4,5], "priority": "MEDIUM"})
    assert resp.status_code == 200
    mid = resp.json()["ingestion_id"]


    time.sleep(4)
    resp2 = client.post("/ingest", json={"ids": [6,7,8,9], "priority": "HIGH"})
    assert resp2.status_code == 200
    hid = resp2.json()["ingestion_id"]

    
    
    time.sleep(6)
    s = client.get(f"/status/{mid}").json()
    assert s["batches"][0]["status"] == "completed"
    assert s["batches"][1]["status"] in ["yet_to_start", "triggered"]
    s2 = client.get(f"/status/{hid}").json()
    assert s2["batches"][0]["status"] == "triggered" or s2["batches"][0]["status"] == "completed"

   
    time.sleep(6)
    s2 = client.get(f"/status/{hid}").json()
    assert s2["batches"][0]["status"] == "completed"
    assert s2["batches"][1]["status"] == "triggered" or s2["batches"][1]["status"] == "completed"

  
    time.sleep(6)
    s = client.get(f"/status/{mid}").json()
    s2 = client.get(f"/status/{hid}").json()
    assert all(b["status"] == "completed" for b in s["batches"])
    assert all(b["status"] == "completed" for b in s2["batches"])

def test_rate_limits_and_priorities():
    
    payloads = [
        ({"ids": [1,2,3], "priority": "LOW"}, "LOW"),
        ({"ids": [4,5,6], "priority": "MEDIUM"}, "MEDIUM"),
        ({"ids": [7,8,9], "priority": "HIGH"}, "HIGH"),
    ]
    ids = []
    for payload, _ in payloads:
        resp = client.post("/ingest", json=payload)
        ids.append(resp.json()["ingestion_id"])

    time.sleep(7)
    high_status = client.get(f"/status/{ids[2]}").json()
    assert high_status["batches"][0]["status"] == "completed"
    med_status = client.get(f"/status/{ids[1]}").json()
    low_status = client.get(f"/status/{ids[0]}").json()
   
    assert med_status["batches"][0]["status"] in ["yet_to_start", "triggered"]
    assert low_status["batches"][0]["status"] in ["yet_to_start", "triggered"]
