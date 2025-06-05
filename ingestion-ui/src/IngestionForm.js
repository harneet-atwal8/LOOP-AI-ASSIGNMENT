import React, { useState } from "react";
import axios from "axios";

export default function IngestionForm({ onSuccess }) {
  const [ids, setIds] = useState("");
  const [priority, setPriority] = useState("MEDIUM");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const idList = ids.split(/[\s,]+/).map(x => parseInt(x)).filter(Boolean);
    try {
      const { data } = await axios.post("http://localhost:8000/ingest", {
        ids: idList,
        priority
      });
      onSuccess(data.ingestion_id);
    } catch (err) {
      alert("Error submitting ingestion");
    }
    setLoading(false);
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: "500px",
        margin: "40px auto",
        padding: "30px",
        backgroundColor: "#f9f9ff",
        border: "1px solid #ddd",
        borderRadius: "12px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
        fontFamily: "Arial, sans-serif"
      }}
    >
      <h2 style={{ textAlign: "center", color: "#333", marginBottom: "20px" }}>
        Ingestion Form
      </h2>

      <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
        IDs (comma or space separated):
      </label>
      <textarea
        value={ids}
        onChange={e => setIds(e.target.value)}
        rows={3}
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "14px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          marginBottom: "20px"
        }}
      />

      <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
        Priority:
      </label>
      <select
        value={priority}
        onChange={e => setPriority(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "14px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          marginBottom: "20px"
        }}
      >
        <option value="HIGH"> HIGH</option>
        <option value="MEDIUM"> MEDIUM</option>
        <option value="LOW"> LOW</option>
      </select>

      <button
        type="submit"
        disabled={loading}
        style={{
          width: "100%",
          padding: "12px",
          fontSize: "16px",
          backgroundColor: loading ? "#ccc" : "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: loading ? "not-allowed" : "pointer",
          transition: "background-color 0.3s"
        }}
      >
        {loading ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
}
