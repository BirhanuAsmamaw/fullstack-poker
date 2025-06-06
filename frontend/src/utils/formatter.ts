const logMessageFormatter = (data: any, displayAction: string) => {
    const pokerLevels = ['Preflop', 'Flop', 'Turn', 'River']
    let loggedMessage = []

    if (data.current_player_index !== null) {
        let defaultMessage = `Player ${data.current_player_index + 1} ${displayAction}`
        loggedMessage.push(defaultMessage)
    }

    if (data.is_round_changed) {
        let actionMessage =  `${pokerLevels[data.street_index]} cards dealt : ${data.board}`
        loggedMessage.push(actionMessage) 
    }

    if (data.is_game_over) {
        let handCompletionMessage = `Hand #${data.hand_id} ended`
        let finalPotMessage = `Final pot was ${data.final_pot}`
        loggedMessage.push(handCompletionMessage, finalPotMessage)
    }

    return loggedMessage
}

const logApplyMessageFormatter = (data : any) => {
    const { dealer_index, small_blind_index, big_blind_index, preflop_dealings } = data.cards

    const formattedLog: string[] = []

    preflop_dealings.forEach((card: string, index: number) => {
      formattedLog.push(`Player ${index + 1} is dealt ${card}`)
    })

    formattedLog.push('---')
    formattedLog.push(`Player ${dealer_index + 1} is the dealer`)
    formattedLog.push(`Player ${small_blind_index + 1} posts small blind - 20 chips`)
    formattedLog.push(`Player ${big_blind_index + 1} posts big blind - 40 chips`)
    formattedLog.push('---')
    return formattedLog

}

const formatHand = (hand: any): string => {
    const numPlayers = 6;
    const dealerIndex = hand.dealer;
    const smallBlindIndex = (dealerIndex + 1) % numPlayers;
    const bigBlindIndex = (dealerIndex + 2) % numPlayers;
  
    const labelPlayers = (items: any[]) =>
      items.map((item, idx) => `Player ${idx + 1}: ${item}`).join("; ");
  
    return [
      `Hand #${hand.hand_id}`,
      `Stack ${hand.stack_size}; Dealer: Player ${dealerIndex + 1}; Player ${smallBlindIndex + 1} Small Blind; Player ${bigBlindIndex + 1} Big Blind`,
      `Hands: ${labelPlayers(hand.player_hands)}`,
      `Actions: ${hand.actions.join(" ")}`,
      `Winnings: ${labelPlayers(hand.winnings)}`
    ].join('\n');
}

export  {logMessageFormatter, logApplyMessageFormatter, formatHand} 