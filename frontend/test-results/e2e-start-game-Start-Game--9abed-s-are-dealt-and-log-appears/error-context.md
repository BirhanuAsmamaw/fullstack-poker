# Test info

- Name: Start Game Flow - Hole cards are dealt and log appears
- Location: C:\Users\Bemnet Aschalew\Desktop\fullstack-poker\fullstack-poker\frontend\e2e\start-game.spec.ts:3:5

# Error details

```
Error: expect.toBeVisible: Error: strict mode violation: locator('pre').filter({ hasText: /dealer/i }) resolved to 5 elements:
    1) <pre class="whitespace-pre-wrap text-sm">Player 1 is dealt 9c7s↵Player 2 is dealt 4h9s↵Pla…</pre> aka getByText('Player 1 is dealt 9c7s Player')
    2) <pre class="text-sm whitespace-pre-wrap">Hand #2bebf2ed-b417-485e-b9a9-4413d12bb3ef↵Stack …</pre> aka getByText('Hand #2bebf2ed-b417-485e-b9a9')
    3) <pre class="text-sm whitespace-pre-wrap">Hand #a5bd5e05-95a9-4c88-9f7d-fa33a7c6f80a↵Stack …</pre> aka getByText('Hand #a5bd5e05-95a9-4c88-9f7d')
    4) <pre class="text-sm whitespace-pre-wrap">Hand #58fb4ee5-3ba7-40a8-923e-1a071b2656c3↵Stack …</pre> aka getByText('Hand #58fb4ee5-3ba7-40a8-923e')
    5) <pre class="text-sm whitespace-pre-wrap">Hand #64180b07-2808-4418-a5f8-3324f552c0c0↵Stack …</pre> aka getByText('Hand #64180b07-2808-4418-a5f8')

Call log:
  - expect.toBeVisible with timeout 5000ms
  - waiting for locator('pre').filter({ hasText: /dealer/i })

    at C:\Users\Bemnet Aschalew\Desktop\fullstack-poker\fullstack-poker\frontend\e2e\start-game.spec.ts:21:61
```

# Page snapshot

```yaml
- heading "Playing field log" [level=2]
- text: Stacks
- spinbutton: "10000"
- button "Apply"
- button "Reset"
- text: Player 1 is dealt 9c7s Player 2 is dealt 4h9s Player 3 is dealt Ah3d Player 4 is dealt Ks5c Player 5 is dealt 2c9h Player 6 is dealt QcTd --- Player 1 is the dealer Player 2 posts small blind - 20 chips Player 3 posts big blind - 40 chips ---
- button "Fold"
- button "Check"
- button "Call"
- button "Bet 20"
- button "+"
- button "-"
- button "Raise 40"
- button "+"
- button "-"
- button "ALLIN"
- heading "Hand history" [level=2]
- text: "Hand #2bebf2ed-b417-485e-b9a9-4413d12bb3ef Stack 10000; Dealer: Player 1; Player 2 Small Blind; Player 3 Big Blind Hands: Player 1: 6hKd; Player 2: 7s9d; Player 3: 7cAs; Player 4: 3h2s; Player 5: 4d7d; Player 6: QsTd Actions: x: x: x: x: x: x: Qh9cQd x: x: x: x: x: x: 8s x: x: x: x: x: x: 8h x: x: x: x: x: x: Winnings: Player 1: -40; Player 2: -40; Player 3: -40; Player 4: -40; Player 5: -40; Player 6: 200 Hand #a5bd5e05-95a9-4c88-9f7d-fa33a7c6f80a Stack 1000; Dealer: Player 1; Player 2 Small Blind; Player 3 Big Blind Hands: Player 1: TdKh; Player 2: 7h9h; Player 3: 3c3h; Player 4: 9cKs; Player 5: 4sJd; Player 6: 4cTc Actions: c: c: c: c: c: c: 8sKcJh c: c: c: c: c: c: 4h c: c: c: c: c: c: 2d c: c: c: c: c: c: Winnings: Player 1: -40; Player 2: -40; Player 3: -40; Player 4: -40; Player 5: 200; Player 6: -40 Hand #58fb4ee5-3ba7-40a8-923e-1a071b2656c3 Stack 10000; Dealer: Player 1; Player 2 Small Blind; Player 3 Big Blind Hands: Actions: Tc5c 8cQh JcJs 9s7c 6cTs 2d6d f: f: f: f: f: Winnings: Player 1: -20; Player 2: 20; Player 3: 0; Player 4: 0; Player 5: 0; Player 6: 0 Hand #64180b07-2808-4418-a5f8-3324f552c0c0 Stack 10000; Dealer: Player 1; Player 2 Small Blind; Player 3 Big Blind Hands: Actions: 8c4s 9dQd QcTc Qs5d 2hTh 2s3h f: f: f: f: f: Winnings: Player 1: 20; Player 2: -20; Player 3: 0; Player 4: 0; Player 5: 0; Player 6: 0"
- alert
- button "Open Next.js Dev Tools":
  - img
```

# Test source

```ts
   1 | import { test, expect } from '@playwright/test'
   2 |
   3 | test('Start Game Flow - Hole cards are dealt and log appears', async ({ page }) => {
   4 |   await page.goto('http://localhost:3000/')
   5 |
   6 |   const stackInput = page.getByRole('spinbutton') // Assumes input type number
   7 |   await stackInput.fill('10000')
   8 |
   9 |   const applyButton = page.getByRole('button', { name: /apply/i })
  10 |   await applyButton.click()
  11 |
  12 |   // Wait for the log to update
  13 |   await expect(page.getByText(/Player 1 is dealt/i)).toBeVisible({ timeout: 5000 })
  14 |
  15 |   // Confirm multiple players received cards
  16 |   for (let i = 1; i <= 6; i++) {
  17 |     await expect(page.getByText(new RegExp(`Player ${i} is dealt`, 'i'))).toBeVisible()
  18 |   }
  19 |
  20 |   // Validate that dealer and blinds are posted
> 21 |   await expect(page.locator('pre', { hasText: /dealer/i })).toBeVisible()
     |                                                             ^ Error: expect.toBeVisible: Error: strict mode violation: locator('pre').filter({ hasText: /dealer/i }) resolved to 5 elements:
  22 |   await expect(page.getByText(/small blind/i)).toBeVisible()
  23 |   await expect(page.getByText(/big blind/i)).toBeVisible()
  24 | })
  25 |
```