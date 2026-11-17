---
id: computing-software.web-development.frontend-development.cookies-from-javascript
name: cookies-from-javascript
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, document-cookie, cookiestore, cookie-api, js-cookies, cookie-attributes]
level: practitioner
status: docs-checked
description: "Reading and writing cookies from script with document.cookie and the async Cookie Store API, attribute pitfalls, and which cookies JS must never touch."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie
  - https://developer.mozilla.org/en-US/docs/Web/API/Cookie_Store_API
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookies from JavaScript

**Goal:** set and read non-sensitive cookies from script correctly, and leave auth cookies to the server.

## 1. document.cookie
Reading returns `"a=1; b=2"` (only non-HttpOnly cookies visible to this path). Writing sets **one** cookie per assignment:
```js
document.cookie = `consent=${encodeURIComponent(JSON.stringify(v))}; Path=/; Max-Age=${60*60*24*180}; SameSite=Lax; Secure`;
```
- Without `Path`, the cookie defaults to the path of the current document (a directory), so set `Path=/` explicitly or you create per-path duplicates.
- Delete by setting the same name **with the same Path/Domain** and an `Expires` in the past or `Max-Age=0`; mismatched attributes leave the original.
- Encode values with `encodeURIComponent` (MDN: commas, semicolons and whitespace are not allowed in the value).
- MDN: browsers generally limit a cookie to about 4 KB, and matching cookies are sent with requests, so keep them small. `document.cookie` is synchronous and can block the main thread.

Parse:
```js
const get = n => document.cookie.split('; ').find(c => c.startsWith(n + '='))?.slice(n.length + 1);
```

## 2. Cookie Store API (async)
```js
await cookieStore.set({ name: 'consent', value: 'yes', expires: Date.now() + 180*864e5, sameSite: 'lax' });
const c = await cookieStore.get('consent');
cookieStore.addEventListener('change', e => console.log(e.changed, e.deleted));
```
Per MDN browser-compat data: Chrome 87, Firefox 140, Safari 18.4 (some options such as `maxAge` are newer: Chrome 145, Firefox 148, Safari 27). Available in windows and service workers, asynchronous, secure contexts only. Check the option you use against the compat table.

## 3. What JS must not handle
Session/auth cookies should be set by the server with `HttpOnly; Secure; SameSite`. If your script needs to read the session cookie, an XSS can too. Read-only state needed by JS (e.g. CSRF token) can be in a separate non-HttpOnly cookie or a meta tag.

## 4. Third-party contexts
Cookies set in third-party iframes may be blocked or partitioned depending on the browser. The `Partitioned` attribute (CHIPS) is supported from Chrome 114, Firefox 141 and Safari 26.2 (MDN browser-compat data). Don't rely on third-party cookies.

## Verify
- [ ] DevTools > Application > Cookies shows exactly one cookie per name with Path=/.
- [ ] Deleting works across pages.
- [ ] No auth token readable via `document.cookie`.

## Checked
Checked 2026-10-26 against MDN Document.cookie, Cookie Store API (CookieStore availability in windows and service workers, secure context), Cookies guide (4 KB limit, deletion rules) and Set-Cookie, plus MDN browser-compat data for CookieStore and Partitioned. Removed the unconfirmed per-browser third-party cookie blocking statement. The example snippets were not run.

Method: documentation only; no commands were run.
