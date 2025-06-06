export default function HandHistory({ hands }: { hands: string[] }) {
  return (
    <div className="space-y-4">
      {hands.map((hand, idx) => (
        <div key={idx} className="bg-blue-100 p-3 rounded">
          <pre className="text-sm whitespace-pre-wrap">{hand}</pre>
        </div>
      ))}
    </div>
  );
}
