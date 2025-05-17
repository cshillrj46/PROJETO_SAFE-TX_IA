// File: src/TransactionAnalyzer.tsx
import { useState } from "react";

export default function TransactionAnalyzer() {
  const [sender, setSender] = useState("");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");
  const [risk, setRisk] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setRisk(null);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sender,
          recipient,
          amount_eth: parseFloat(amount),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze transaction");
      }

      const result = await response.json();
      setRisk(result.risk); // espera que o backend retorne { "risk": "suspicious" }, por exemplo
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center text-white">
      <h2 className="text-2xl font-bold mb-4">Transaction Analyzer</h2>
      <div className="w-full max-w-xs">
        <input
          type="text"
          placeholder="Sender Address"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
          className="w-full p-2 mb-2 rounded bg-gray-800 text-white border border-gray-600"
        />
        <input
          type="text"
          placeholder="Recipient Address"
          value={recipient}
          onChange={(e) => setRecipient(e.target.value)}
          className="w-full p-2 mb-2 rounded bg-gray-800 text-white border border-gray-600"
        />
        <input
          type="number"
          placeholder="Amount (ETH)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full p-2 mb-4 rounded bg-gray-800 text-white border border-gray-600"
        />
        <button
          onClick={handleAnalyze}
          className="w-full p-2 rounded bg-blue-600 hover:bg-blue-700 text-white font-bold"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Transaction"}
        </button>
        {risk && (
          <p className="mt-4 text-lg font-semibold text-center">
            Risk Level: <span className="capitalize text-yellow-400">{risk}</span>
          </p>
        )}
        {error && <p className="mt-2 text-red-500 text-sm text-center">{error}</p>}
      </div>
    </div>
  );
}
