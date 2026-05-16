import { test, Page } from '@playwright/test'
import path from 'path'
import fs from 'fs'

const EMAIL    = process.env.TEST_USER_EMAIL    ?? 'admin@sotifibre.dz'
const PASSWORD = process.env.TEST_USER_PASSWORD ?? 'SOTIFibre@2026!'

const OUT = path.resolve(__dirname, '../../docs/screenshots')
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true })

test.use({ viewport: { width: 1600, height: 900 } })

async function login(page: Page) {
  await page.goto('/login')
  await page.locator('input[type="email"], input[name="email"]').fill(EMAIL)
  await page.locator('input[type="password"]').fill(PASSWORD)
  await page.locator('button[type="submit"]').click()
  await page.waitForURL(/\/(dashboard)?$/, { timeout: 20_000 })
}

test('screenshot – dashboard', async ({ page }) => {
  await login(page)
  await page.goto('/dashboard')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(OUT, 'dashboard.png'), fullPage: false })
})

test('screenshot – kpis', async ({ page }) => {
  await login(page)
  await page.goto('/kpis')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(OUT, 'kpis.png'), fullPage: false })
})

test('screenshot – reports', async ({ page }) => {
  await login(page)
  await page.goto('/reports')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(OUT, 'reports.png'), fullPage: false })
})

test('screenshot – pipelines', async ({ page }) => {
  await login(page)
  await page.goto('/pipelines')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(OUT, 'pipelines.png'), fullPage: false })
})

test('screenshot – ml-analytics', async ({ page }) => {
  await login(page)
  await page.goto('/ml-analytics')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(OUT, 'ml-analytics.png'), fullPage: false })
})

test('screenshot – connections', async ({ page }) => {
  await login(page)
  await page.goto('/sources/connections')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1000)
  await page.screenshot({ path: path.join(OUT, 'connections.png'), fullPage: false })
})

test('screenshot – admin', async ({ page }) => {
  await login(page)
  await page.goto('/admin')
  await page.waitForLoadState('networkidle')
  await page.waitForTimeout(1000)
  await page.screenshot({ path: path.join(OUT, 'admin.png'), fullPage: false })
})
