// File: src/ReclassificationForm.tsx
import { useState } from "react";

export default function ReclassificationForm() {
  const [txId, setTxId] = useState("");
  const [newRisk, setNewRisk] = useState("safe");
  const [reason, setReason] = useState("");
  const [reclassifiedBy, setReclassifiedBy] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  const handleSubmit = async () => {
    setStatus(null);
    if (!txId || !reason || !reclassifiedBy) {
      setStatus("Please fill in all fields.");
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/reclassify/${txId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          new_risk: newRisk,
          reason,
          reclassified_by: reclassifiedBy,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to reclassify transaction");
      }

      setStatus("Transaction successfully reclassified.");
      setTxId("");
      setNewRisk("safe");
      setReason("");
      setReclassifiedBy("");
    } catch (err: any) {
      setStatus(err.message);
    }
  };

  return (
    <div className="text-white p-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-center">Manual Classification</h2>
      <input
        type="number"
        placeholder="Transaction ID"
        value={txId}
        onChange={(e) => setTxId(e.target.value)}
        className="w-full p-2 mb-2 rounded bg-gray-800 border border-gray-600"
      />
      <select
        value={newRisk}
        onChange={(e) => setNewRisk(e.target.value)}
        className="w-full p-2 mb-2 rounded bg-gray-800 border border-gray-600"
      >
        <option value="safe">Safe</option>
        <option value="suspicious">Suspicious</option>
        <option value="high-risk">High-Risk</option>
      </select>
      <input
        type="text"
        placeholder="Reason"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        className="w-full p-2 mb-2 rounded bg-gray-800 border border-gray-600"
      />
      <input
        type="text"
        placeholder="Your Name"
        value={reclassifiedBy}
        onChange={(e) => setReclassifiedBy(e.target.value)}
        className="w-full p-2 mb-4 rounded bg-gray-800 border border-gray-600"
      />
      <button
        onClick={handleSubmit}
        className="w-full p-2 rounded bg-blue-600 hover:bg-blue-700 font-bold"
      >
        Submit Reclassification
      </button>
      {status && (
        <p className="mt-4 text-center text-sm text-yellow-400">{status}</p>
      )}
    </div>
  );
}
