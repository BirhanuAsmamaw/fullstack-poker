'use client'

import React, { useState } from "react"
import StackControl from "@/components/StackControl"
import ActionLog from "@/components/ActionLog"
import ActionButtons from "@/components/ActionButtons"
import HandHistory from "@/components/HandHistory"
import {logMessageFormatter, logApplyMessageFormatter} from '@/utils/formatter'
import endpointActionManager from "@/utils/endpointActionManager"
import makeApiRequest from "@/utils/apiClient"
import HandHistoryContainer from "@/components/HandHistoryContainer"

export default function Home() {
  const [stack, setStack] = useState(10000)
  const [log, setLog] = useState<string[]>([])
  const [hands, setHands] = useState<string[]>([])

  const handleApply = async (value: number) => {
    setStack(value)

    try {
      const data = await makeApiRequest('/hand/start/game', 'POST', { stack_size: value })
      const formattedLog = logApplyMessageFormatter(data)
      console.log(formattedLog)
      setLog((prev: any) => [...prev, ...formattedLog])

    } catch (error: any) {
      alert(`Error: ${error?.detail || error?.message || 'Unknown error occurred'}`);
    }
  }

  const handleAction = async (action: string, value?: number) => {
    const actionStr = value !== undefined ? `${action}${value}` : action
    let [endpoint, displayAction] = endpointActionManager(action, value)

    try {
      const data = await makeApiRequest(endpoint, 'POST', {
        action: actionStr,
        amount: value,
      })

      let loggedMessage = logMessageFormatter(data, displayAction)

      setLog((prev: any) => 
        [...prev, ...loggedMessage]
      )

    } catch (error: any) {
      alert(`Error: ${error?.detail || error?.message || 'Unknown error occurred'}`);
    }
  }

  return (
    <div className="p-6">
      <div className="flex flex-col md:flex-row gap-0 md:gap-0 min-h-screen">
        {/* Left Side */}
        <div className="flex-1 p-4">
          <h2 className="text-xl font-semibold mb-2">Playing field log</h2>
          <StackControl defaultStack={stack} onApply={handleApply} />
          <ActionLog log={log} />
          <ActionButtons onAction={handleAction} />
        </div>

        {/* Divider */}
        <div className="w-[3px] bg-black" />

        {/* Right Side */}
        {/* <div className="flex-1 p-4">
          <div className="bg-gray-100 p-4 rounded-lg shadow-inner h-96 overflow-y-auto whitespace-pre-wrap text-sm">
            <h2 className="text-xl font-semibold mb-4">Hand history</h2>
            <div className="mt-0">
              <HandHistory
                hands={hands.length ? hands : [
                  `Hand #395b5999-cdc1-4469-947e-649d30aa6158
Stack 10000; Dealer: Player 3; Player 4 Small Blind; Player 6
Hands: Player 1: Tc2c; Player 2: 5d4c; Player 3: AhAs; Player 4: QcTd
Actions: ffrr300cT 3hKdQs xx0100c Ac xx Th bb80r160c
Winnings: Player 1: -40; Player 2: 0; Player 3: -560; Player 4: +600`
                ]}
              />
            </div>
          </div>
        </div> */}
        <HandHistoryContainer />
      </div>
    </div>
  )
  
}
