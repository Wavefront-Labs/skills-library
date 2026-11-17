---
id: computing-software.qa-testing-engineering.playwright.permissions-offline-and-http-credentials
name: permissions-offline-and-http-credentials
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [grant-permissions, http-credentials, offline-mode, playwright-network, browser-context-options]
level: practitioner
status: docs-checked
description: "Set Playwright browser-context options for permissions (geolocation, clipboard, notifications), offline mode, HTTP basic auth, extra headers and ignoring HTTPS errors."
sources:
  - https://playwright.dev/docs/emulation
  - https://playwright.dev/docs/api/class-browsercontext
  - https://playwright.dev/docs/network#http-authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions, offline mode and HTTP credentials

**Goal:** control browser-level conditions that real users hit but tests often ignore.

## Permissions
```ts
use: { permissions: ['geolocation', 'clipboard-read', 'clipboard-write'], geolocation: { latitude: -36.85, longitude: 174.76 } }
// at runtime
await context.grantPermissions(['notifications'], { origin: 'https://app.test' });
await context.clearPermissions();   // test the "denied/prompt" path
```
The docs warn that supported permissions differ between browsers, and even between versions of the same browser, so any permission may stop working after an update; guard per project.

## Offline / network conditions
```ts
await context.setOffline(true);
await page.getByRole('button', { name: 'Save' }).click();
await expect(page.getByText('You are offline')).toBeVisible();
await context.setOffline(false);
```
The `offline` context option (`use: { offline: true }`) starts a context offline. Offline emulation affects requests going through the browser's regular network stack (navigations, `fetch()`, `XMLHttpRequest`, WebSockets), not WebRTC traffic.

## HTTP auth and headers
```ts
use: {
  httpCredentials: { username: 'stage', password: process.env.BASIC_PASS!, origin: 'https://staging.example.com' },
  extraHTTPHeaders: { 'x-test-run': process.env.GITHUB_RUN_ID ?? 'local' },
  ignoreHTTPSErrors: true,    // self-signed staging certs only
}
```
`origin` (scheme://host:port) restricts where credentials are sent; with no origin they are sent to any server that answers unauthorized. An array of credentials can be given for different origins.

## Gotchas
- `extraHTTPHeaders` are sent with every request the context makes, including third-party hosts.
- `httpCredentials.send` only applies to requests from the corresponding APIRequestContext, not to browser requests.
- Do not set `ignoreHTTPSErrors` for production checks; certificate errors are real failures there.

## Verify
Geolocation test shows the expected city; denied-permission path shows the fallback UI.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: permissions and geolocation via context options, grantPermissions with an origin and clearPermissions, the warning that supported permissions differ across browsers, setOffline and the offline option and what offline emulation covers, httpCredentials with origin and the send option, extraHTTPHeaders going on every request, and ignoreHTTPSErrors defaulting to false. Removed: the Chromium-only clipboard claim, the CDP throttling suggestion and the CORS preflight remark.

Method: documentation only; no commands were run.
