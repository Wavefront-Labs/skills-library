---
id: computing-software.web-development.node-express.samesite-cookies-csrf-defence
name: samesite-cookies-csrf-defence
category: computing-software
field: web-development
product: node-express
tags: [csrf, samesite-cookies, cookies, security, defence-in-depth]
level: practitioner
status: verified
description: "Using SameSite=Lax/Strict session cookies as CSRF defence in depth: what each value blocks, same-site vs same-origin gaps, top-level GET exposure and browser defaults."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value
  - https://web.dev/articles/samesite-cookies-explained
  - https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SameSite cookies as CSRF defence in depth

## 1. Values
| `SameSite=` | Sent on cross-site requests? |
|---|---|
| `Strict` | Never. Even following a link from another site arrives logged-out. |
| `Lax` | Only top-level navigations with safe methods (clicking a link, GET form). Not on cross-site POST, iframes, `fetch`, images. |
| `None` | Always - requires `Secure`. Needed for embedded/third-party contexts (and third-party cookie blocking may still drop it). |
Chrome defaults cookies without the attribute to `Lax` (with a 2-minute POST exception for new cookies: in Chrome 156 a just-set cookie with no attribute was sent on a cross-site form POST, while an explicit `SameSite=Lax` cookie was not); Safari/Firefox defaults differ - **always set it explicitly**.

```js
res.cookie("sid", id, { httpOnly: true, secure: true, sameSite: "lax", path: "/" });
```
Pattern for high-value apps: a `Lax` session cookie for browsing + a `Strict` cookie required for sensitive actions.

## 2. Why it is not enough alone
- **Same-site is not same-origin**: `evil.example.com` and `app.example.com` are same-site, so a compromised or user-content subdomain can CSRF you. (Site = scheme + registrable domain; github.io-style shared hosts are on the Public Suffix List.)
- `Lax` allows top-level GET - any state change on GET is exploitable.
- Method override middleware (`_method=DELETE` on GET/POST) can turn an allowed request into a destructive one.
- Older browsers ignore SameSite.
- Login CSRF and cookie tossing from subdomains bypass it.
So keep tokens or Origin checks as the primary control; SameSite reduces the blast radius.

## 3. Checklist
- Session cookies: `HttpOnly; Secure; SameSite=Lax` (or Strict), `__Host-` prefix to block subdomain overwrites.
- No state changes on GET.
- Cross-site embeds/SSO that need cookies: isolate those cookies (`SameSite=None; Secure; Partitioned` for CHIPS) away from the main session.

## Verify
DevTools > Application > Cookies shows SameSite per cookie; a cross-site form POST from another domain arrives without the session cookie (Network panel "filtered out" cookie warning).

## Checked
Run in headless Chrome 156 (Windows, via Playwright) with two local sites that are cross-site to each other (`http://127.0.0.1:18101` sets four cookies, `http://localhost:18102` embeds it): the browser stored the attribute-less cookie as `Lax`; cross-site `img`, `fetch(credentials: include)` and `iframe` requests carried only the `SameSite=None` cookie (Chrome accepted a `Secure` cookie on http loopback); a cross-site link click (top-level GET) carried Lax, None and default but not Strict; a cross-site form POST carried only None and the fresh default cookie (not explicit Lax, not Strict); a cross-site GET form carried Lax. Same-origin requests carried all four. Not run: Firefox and Safari defaults, the `__Host-` prefix, `Partitioned`/CHIPS, third-party cookie blocking, same-site subdomain attacks, method-override middleware, the Strict-cookie-for-sensitive-actions pattern. Browser behaviour is OS-independent but version-dependent: re-check on current browsers.
