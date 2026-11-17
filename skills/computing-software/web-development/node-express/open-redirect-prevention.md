---
id: computing-software.web-development.node-express.open-redirect-prevention
name: open-redirect-prevention
category: computing-software
field: web-development
product: node-express
tags: [broken-access-control, authorization, open-redirect, unvalidated-redirects, return-url, next-parameter, phishing]
level: practitioner
status: verified
description: "Fixing open redirects in login returnTo/next parameters: relative-path allowlisting, URL parsing traps (//evil, backslashes) and OAuth redirect_uri rules."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html
  - https://portswigger.net/kb/issues/00500100_open-redirection-reflected
  - https://datatracker.ietf.org/doc/html/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open redirect prevention

**Goal:** `?next=` / `returnTo` parameters can only send users to your own pages, so your domain can't be used to launder phishing links or leak OAuth codes.

## 1. The bug
```js
app.post('/login', async (req, res) => { /* auth */ res.redirect(req.query.next || '/'); });
// https://app.example.com/login?next=https://evil.example/fake-login
```

## 2. Allow only same-site relative paths
```js
function safeNext(raw, fallback = '/') {
  if (typeof raw !== 'string' || !raw.startsWith('/') || raw.startsWith('//') || raw.startsWith('/\\')) return fallback;
  const u = new URL(raw, 'https://app.example.com');     // normalise with a fixed base
  if (u.origin !== 'https://app.example.com') return fallback;
  const out = u.pathname + u.search + u.hash;
  return /^\/(?![\/\\])/.test(out) ? out : fallback;   // normalisation can create '//host': '/..//evil.com' -> '//evil.com'
}
res.redirect(303, safeNext(req.query.next));
```
The last check is essential: with only the origin check, `/..//evil.com`, `/.//evil.com` and `/%2e%2e//evil.com` all normalise to a pathname of `//evil.com`, which `res.redirect` sends as `Location: //evil.com` (protocol-relative, an open redirect; reproduced on Express 4). Traps that naive checks miss: `//evil.com` (protocol-relative), `/\evil.com` (browsers treat `\` as `/`), `https:evil.com`, `javascript:` URLs, encoded variants (`%2F%2Fevil.com`), `https://app.example.com.evil.com` (prefix matching), and userinfo `https://app.example.com@evil.com`.

## 3. Cross-domain redirects that must exist
Use an allowlist of full origins, or map ids to URLs (`?dest=billing` -> server-side table). For "you are leaving" links, show an interstitial.

## 4. OAuth
Register exact `redirect_uri`s with the authorization server (no wildcards); open redirects on your own domain can still leak codes/tokens via a registered URI that then redirects - another reason to kill them. RFC 9700 (OAuth security BCP) requires exact string matching.

## 5. Frameworks
Django: `url_has_allowed_host_and_scheme(next, allowed_hosts={request.get_host()}, require_https=True)` (used by `LoginView`). Rails 7+: `redirect_to params[:next]` raises `UnsafeRedirectError` for other hosts unless `allow_other_host: true`. Next.js: validate before `redirect()`.

## Verify
- [ ] Test vectors above all redirect to the fallback.
- [ ] Legit deep links (`/orders/42?tab=items#notes`) survive login.
- [ ] No route redirects to a raw request parameter (grep `redirect(req.`).

## Checked
Run on Windows with Node 20.20.2 and Express 4.22: 24 vectors through the original and the fixed `safeNext`. The original passed `/..//evil.com`, `/a/..//evil.com`, `/.//evil.com`, `/./\evil.com` and `/%2e%2e//evil.com` through as `//evil.com`, and Express answered `Location: //evil.com`; the fixed version returns the fallback for all of them and keeps `/orders/42?tab=items#notes`, `/a/../b` and `/?x=//y`. `//evil.com`, `/\evil.com`, `https:evil.com`, `javascript:`, `%2F%2Fevil.com`, `https://app.example.com.evil.com` and `https://app.example.com@evil.com` were all rejected by both. `new URL` treats a tab or backslash after the first slash as a slash. Not run: a real browser, Django, Rails and Next.js helpers, the OAuth redirect_uri advice (RFC 9700 not fetched). WHATWG URL parsing is part of Node, so Windows and Linux behave the same.
