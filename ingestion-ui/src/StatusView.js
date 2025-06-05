import React, { useEffect, useState } from "react";
import axios from "axios";

export default function StatusView({ ingestionId }) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let interval = setInterval(fetchStatus, 3000);
    fetchStatus();
    return () => clearInterval(interval);

    async function fetchStatus() {
      try {
        const { data } = await axios.get(`http://localhost:8000/status/${ingestionId}`);
        setStatus(data);
      } catch {
        setStatus(null);
      }
    }
  }, [ingestionId]);

  const statusColor = {
    yet_to_start: "gray",
    triggered: "goldenrod",
    completed: "green"
  };

  const statusEmoji = {
    yet_to_start: "🔘",
    triggered: "🟡",
    completed: "🟢"
  };

  if (!status) return <div style={{ textAlign: "center", padding: "20px" }}>Loading status...</div>;

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "40px auto",
        padding: "30px",
        backgroundColor: "#fff8f0",
        border: "1px solid #ddd",
        borderRadius: "12px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        fontFamily: "Arial, sans-serif"
      }}
    >
      <h2 style={{ textAlign: "center", color: "#333", marginBottom: "16px" }}>
        Status for Ingestion ID: <code>{ingestionId}</code>
      </h2>

      <p style={{ fontSize: "16px", marginBottom: "24px" }}>
        Overall Status:{" "}
        <b style={{ color: statusColor[status.status] }}>
          {statusEmoji[status.status]} {status.status}
        </b>
      </p>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          backgroundColor: "#fff"
        }}
      >
        <thead style={{ backgroundColor: "#eee" }}>
          <tr>
            <th style={{ padding: "10px", border: "1px solid #ccc" }}>Batch ID</th>
            <th style={{ padding: "10px", border: "1px solid #ccc" }}>IDs</th>
            <th style={{ padding: "10px", border: "1px solid #ccc" }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {status.batches.map(batch => (
            <tr key={batch.batch_id}>
              <td style={{ padding: "10px", border: "1px solid #eee" }}>{batch.batch_id}</td>
              <td style={{ padding: "10px", border: "1px solid #eee" }}>{batch.ids.join(", ")}</td>
              <td
                style={{
                  padding: "10px",
                  border: "1px solid #eee",
                  color: statusColor[batch.status],
                  fontWeight: "bold"
                }}
              >
                {statusEmoji[batch.status]} {batch.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
