---
id: computing-software.software-engineering.javascript.js-storage-quota-security
name: js-storage-quota-security
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, storage-quota, js-storage]
level: practitioner
status: docs-checked
description: "Pick localStorage, sessionStorage, cookies or IndexedDB; handle quota errors, eviction and persistence."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API", "https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria", "https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage choices quota and security

- `localStorage` is partitioned by origin and persists across browser restarts; `sessionStorage` is partitioned by tab and origin and is destroyed when the tab closes. Both are synchronous and block other JavaScript while they run; MDN suggests asynchronous alternatives such as IndexedDB for large datasets or performance-sensitive code.
- Web Storage is string-only key/value. Per MDN, browsers allow up to 5 MiB of local storage and 5 MiB of session storage per origin. When the limit is hit they throw `QuotaExceededError`, which should be handled with `try...catch`.
- Writes to IndexedDB, Cache or OPFS can also fail with `QuotaExceededError`; wrap them in `try...catch` and free space before storing new data.
- Access to Web Storage from third-party iframes is denied if the user has disabled third-party cookies. In private browsing, `localStorage` is treated like `sessionStorage` and data is deleted when the window or tab closes.
- Do not put cookies to work as general storage: they are sent with every HTTP request, which inflates requests.
- Data is best-effort by default and can be evicted (least recently used origin first under storage pressure). `navigator.storage.persist()` requests persistent storage, which exempts the origin from that eviction; Firefox asks the user, while Safari and Chromium-based browsers decide from interaction history without a prompt.
- `navigator.storage.estimate()` returns an estimated usage and quota, not exact values.
- Safari proactively deletes script-created data of origins with no user interaction in seven days when cross-site tracking prevention is on. Eviction removes all of an origin's data at once.
- The `storage` event fires when another document sharing the same storage area updates it, and not on the window that made the change. For `localStorage` it reaches other same-origin contexts including other tabs; for `sessionStorage` only same-tab iframes. It is not cancelable and does not bubble.
- Namespace keys and version your schema (for example `app:v2:key`).

Self-check: simulate a full quota and confirm the app degrades without crashing.

## Checked

2026-11-08. Confirmed on MDN Web Storage API, Storage quotas and eviction criteria, and the storage event page. Removed the claim that web storage is unavailable in workers, the advice to prefer `HttpOnly; Secure; SameSite` cookies for tokens, and the XSS claim about storing secrets, which none of these pages state; check the OWASP guidance before adding them back.

Method: docs-only read of cited pages, 2026-11-08
