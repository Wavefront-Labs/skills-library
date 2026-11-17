---
id: computing-software.web-development.frontend-development.localstorage-and-sessionstorage
name: localstorage-and-sessionstorage
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, web-storage, localstorage, sessionstorage, storage-limits, json-storage, private-browsing]
level: practitioner
status: docs-checked
description: "Using localStorage/sessionStorage correctly: size limits, sync cost, JSON and versioning, quota errors, what never to store there, and per-tab sessionStorage behaviour."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
  - https://html.spec.whatwg.org/multipage/webstorage.html
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# localStorage and sessionStorage

**Goal:** store small, non-sensitive preferences reliably, and know when Web Storage is the wrong tool.

## 1. Facts that drive the decision
- Strings only, about 5 MiB of localStorage and 5 MiB of sessionStorage per origin (MDN), **synchronous** - reads and writes block the main thread, so avoid large amounts of data.
- `localStorage`: persists, shared by all tabs of the origin. `sessionStorage`: per tab (top-level browsing context) and origin; it survives reloads, opening the page in a new tab or window creates a new session with a copy of the opener's value, and it is cleared when the page session ends.
- `localStorage` and `sessionStorage` are properties of `Window`, so workers and service workers do not have them. Use IndexedDB there.
- Any script on the origin (including an XSS payload or a compromised third-party script) can read it. OWASP advises against storing sensitive information, and says not to store session identifiers in local storage because the data is always accessible by JavaScript; cookies can mitigate this with `HttpOnly`. Do not keep tokens or personal data there.

## 2. A safe wrapper
```js
const KEY = 'prefs:v2';
export function loadPrefs() {
  try { return { theme: 'system', ...JSON.parse(localStorage.getItem(KEY) ?? '{}') }; }
  catch { return { theme: 'system' }; }        // corrupt JSON or storage disabled
}
export function savePrefs(p) {
  try { localStorage.setItem(KEY, JSON.stringify(p)); }
  catch (e) { if (e.name === 'QuotaExceededError') console.warn('storage full'); }
}
```
- Version keys (`:v2`) and migrate or drop old shapes; old payloads otherwise crash new code.
- `setItem` throws `QuotaExceededError` when the quota is exhausted (some browsers give private-browsing pages a quota of zero); accessing `localStorage` throws `SecurityError` when the user has configured the browser to prevent persisting data, so wrap access.
- Namespace keys on shared origins (`app1:`).

## 3. Good fits
Theme, dismissed banners, last-used tab, small drafts. Avoid for: large datasets, anything queried, binary data, anything accessed in hot loops (cache in memory instead).

## 4. SSR frameworks
`localStorage` doesn't exist on the server. Read it in an effect / `onMounted`, and avoid hydration mismatches by rendering a neutral state first (or set a class from an inline script before paint for theme).

## Verify
- [ ] Clearing or corrupting the key doesn't break the app.
- [ ] No tokens or personal data visible in DevTools > Application > Local Storage.
- [ ] Private-browsing windows and browsers with storage blocked still load the page.

## Checked

Checked 2026-10-26 against MDN Using the Web Storage API, Window.localStorage, Window.sessionStorage and the storage quotas page, and the OWASP HTML5 Security Cheat Sheet (OWASP/CheatSheetSeries main): string-only values, 5 MiB per storage type, synchronous blocking, sessionStorage page-session semantics, `QuotaExceededError`, `SecurityError`, and the advice against storing session identifiers. Removed the unconfirmed 'hits disk' and Safari-private-mode remarks.

Method: documentation only; no commands were run.
