import { useEffect, useRef } from 'react';

export default function ActionLog({ log }: { log: string[] }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [log]); // scrolls down every time the log updates

  return (
    <div
      ref={containerRef}
      className="bg-white border rounded p-3 mt-4 h-96 overflow-y-auto"
    >
      <pre className="whitespace-pre-wrap text-sm">
        {log.join('\n')}
      </pre>
    </div>
  );
}
