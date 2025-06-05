import React, { useState } from "react";
import IngestionForm from "./IngestionForm";
import StatusView from "./StatusView";

function App() {
  const [ingestionId, setIngestionId] = useState("");

  return (
    <div style={{ maxWidth: 600, margin: "auto" }}>
      <h1>Data Ingestion System</h1>
      <IngestionForm onSuccess={setIngestionId} />
      {ingestionId && (
        <StatusView ingestionId={ingestionId} />
      )}
    </div>
  );
}
export default App;