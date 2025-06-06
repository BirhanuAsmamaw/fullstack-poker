import { test, expect } from '@playwright/test'

test('Start Game Flow - Hole cards are dealt and log appears', async ({ page }) => {
  await page.goto('http://localhost:3000/')

  const stackInput = page.getByRole('spinbutton') // Assumes input type number
  await stackInput.fill('10000')

  const applyButton = page.getByRole('button', { name: /apply/i })
  await applyButton.click()

  // Wait for the log to update
  await expect(page.getByText(/Player 1 is dealt/i)).toBeVisible({ timeout: 5000 })

  // Confirm multiple players received cards
  for (let i = 1; i <= 6; i++) {
    await expect(page.getByText(new RegExp(`Player ${i} is dealt`, 'i'))).toBeVisible()
  }

  // Validate that dealer and blinds are posted
  await expect(page.locator('pre', { hasText: /dealer/i })).toBeVisible()
  await expect(page.getByText(/small blind/i)).toBeVisible()
  await expect(page.getByText(/big blind/i)).toBeVisible()
})
