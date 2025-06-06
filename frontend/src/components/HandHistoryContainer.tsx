import { useEffect, useState } from "react";
import HandHistory from "./HandHistory";
import makeApiRequest from "@/utils/apiClient"; // Adjust path as needed
import { formatHand } from "@/utils/formatter";

export default function HandHistoryContainer() {
  const [hands, setHands] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHands = async () => {
      try {
        const data = await makeApiRequest("/hand/history", "GET");
        const formatted = data.map(formatHand);
        setHands(formatted);
      } catch (err: any) {
        setError(err.detail || "Failed to fetch hand history.");
      } finally {
        setLoading(false);
      }
    };

    fetchHands();
  }, []);

  return (
    <div className="flex-1 p-4">
      <div className="bg-gray-100 p-4 rounded-lg shadow-inner h-96 overflow-y-auto whitespace-pre-wrap text-sm">
        <h2 className="text-xl font-semibold mb-4">Hand history</h2>
        {loading ? (
          <p>Loading hand history...</p>
        ) : error ? (
          <p className="text-red-600">{error}</p>
        ) : (
          <HandHistory hands={hands} />
        )}
      </div>
    </div>
  );
}
