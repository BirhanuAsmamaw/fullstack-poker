'use client'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"

export default function StackControl({
  defaultStack = 10000,
  onApply,
}: {
  defaultStack?: number
  stack: number
  onApply: (value: number) => void
}) {
  const [value, setValue] = useState(defaultStack)

  const resetValue = (): void => {
    setValue(defaultStack);
  }

  return (
    <div className="flex items-center gap-2">
      <label className="text-lg font-semibold">Stacks</label>
      <Input
        type="number"
        value={value}
        className="w-24"
        onChange={(e) => setValue(Number(e.target.value))}
      />
      <Button onClick={() => onApply(value)}>Apply</Button>
      <Button variant="destructive" onClick={resetValue}>Reset</Button>
    </div>
  )
}
