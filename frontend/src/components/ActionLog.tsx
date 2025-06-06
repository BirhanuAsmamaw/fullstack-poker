export default function ActionLog({ log }: { log: string[] }) {
  return (
    <div className="bg-white border rounded p-3 mt-4 h-96 overflow-y-auto">
      <pre className="whitespace-pre-wrap text-sm">{log.join('\n')}</pre>
    </div>
  )
}
