---
id: computing-software.qa-testing-engineering.playwright.multiple-authenticated-roles
name: multiple-authenticated-roles
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [multi-role-auth, storage-state, playwright-authentication, setup-project, role-based-testing]
level: practitioner
status: docs-checked
description: "Test with multiple logged-in roles in Playwright: per-role storageState from a setup project, role fixtures, and two browser contexts interacting in one test."
sources:
  - https://playwright.dev/docs/auth#multiple-signed-in-roles
  - https://playwright.dev/docs/auth#testing-multiple-roles-together
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple authenticated roles (Playwright)

**Goal:** log in once per role per run, reuse the session, and test interactions between roles.

## Setup project writes one state file per role
```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
const roles = { admin: 'playwright/.auth/admin.json', member: 'playwright/.auth/member.json' };
for (const [role, file] of Object.entries(roles)) {
  setup(`authenticate ${role}`, async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill(process.env[`${role.toUpperCase()}_EMAIL`]!);
    await page.getByLabel('Password').fill(process.env[`${role.toUpperCase()}_PASSWORD`]!);
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page.getByRole('button', { name: 'Account' })).toBeVisible();
    await page.context().storageState({ path: file });
  });
}
```
Add `playwright/.auth` to `.gitignore`. Faster: authenticate via API with `request` and save `request.storageState()`.

## Config
```ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  { name: 'chromium', use: { ...devices['Desktop Chrome'] }, dependencies: ['setup'] },
]
```
Per file: `test.use({ storageState: 'playwright/.auth/admin.json' });`

## Two roles in one test
```ts
test('admin approval appears for member', async ({ browser }) => {
  const adminCtx = await browser.newContext({ storageState: 'playwright/.auth/admin.json' });
  const memberCtx = await browser.newContext({ storageState: 'playwright/.auth/member.json' });
  const admin = await adminCtx.newPage(); const member = await memberCtx.newPage();
  await admin.goto('/requests'); await admin.getByRole('button', { name: 'Approve' }).first().click();
  await member.goto('/my-requests');
  await expect(member.getByText('Approved')).toBeVisible();
  await adminCtx.close(); await memberCtx.close();
});
```
Wrap as fixtures (`adminPage`, `memberPage`) via `test.extend` for reuse.

## Gotchas
- Tests that mutate shared accounts (change password, delete data) break parallel runs; use per-worker accounts (`testInfo.parallelIndex`) for those.
- Sessions expire; regenerate state each run, not committed files.

## Verify
Each role logs in once per run (check setup project count), and a cross-role test passes with two independent contexts.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the playwright/.auth directory added to .gitignore, setup project with testMatch for .setup.ts and dependencies, one storageState file per role written with page.context().storageState, test.use storageState per file or describe group, two browser contexts with different storage states in one test, fixtures per role, authenticating through request and saving request.storageState, per-worker accounts via parallelIndex for tests that modify server-side state, and the need to delete expired stored state.

Method: documentation only; no commands were run.
