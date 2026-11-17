---
id: computing-software.cybersecurity-defensive.application-security.cookie-security-attributes
name: cookie-security-attributes
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-headers, cookie-security-flags, samesite, httponly, secure-cookie, cookie-prefixes, csrf]
level: practitioner
status: docs-checked
description: "Set session and auth cookies with Secure, HttpOnly, SameSite, narrow Path and Domain, and __Host- prefixes, per MDN and the OWASP session cheat sheet."
sources: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie", "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookie security attributes

**Goal:** session cookies cannot be read by script, sent over HTTP, shared with sibling hosts, or sent on cross-site
requests.

## Recommended session cookie
The OWASP cheat sheet example: `Set-Cookie: __Host-SessionID=<value>; Secure; HttpOnly; SameSite=Strict; Path=/`
- **`Secure`**: sent only over HTTPS (MDN: except localhost); mandatory per OWASP to prevent session ID disclosure
  via MitM. MDN notes it does not stop access to cookie data with access to the client disk or, without `HttpOnly`,
  from JavaScript.
- **`HttpOnly`**: scripts cannot read the cookie via `document.cookie`, which mitigates session theft through XSS.
  The cookie is still sent on JavaScript-initiated requests, so combined XSS and CSRF still works; it protects
  confidentiality only.
- **`SameSite`**: `Strict` sends the cookie only for same-site requests; `Lax` also allows top-level navigations using
  safe methods (not `POST`, `PUT`, `DELETE`, not subresource, `fetch` or iframe requests); `None` sends it
  cross-site and requires `Secure`. OWASP: set `Strict` (preferred) or `Lax` explicitly on session cookies, never
  `None` without `Secure`, and do not rely on browser defaults, which vary. Treat it as defence in depth against
  CSRF, not a replacement for CSRF tokens. MDN notes that where `Lax` is the browser default, a more permissive
  variant also sends the cookie on `POST` requests made within two minutes of it being set.
- **`Domain`**: omit it. Without it the cookie is host-only; setting it makes the cookie available to that domain and
  all subdomains (OWASP: a permissive value such as `example.com` enables cross-subdomain attacks and session fixation).
- **`Path`**: scope as restrictively as possible, but MDN says it is not a security measure and does not stop other
  paths reading the cookie; OWASP advises not running applications of different security levels on one host.
- **Expiry**: without `Expires` or `Max-Age` a cookie is a session cookie; `Max-Age` takes precedence over `Expires`.
  A cookie with either is persistent. Browser session restore can bring session cookies back.

## Prefixes
- `__Secure-`: must be set with `Secure` from an HTTPS page.
- `__Host-`: `Secure`, no `Domain`, and `Path=/`; the cookie goes only to the host that set it and cannot be
  overridden on another path. OWASP recommends it for session IDs; it prevents subdomain forgery and HTTPS downgrade
  attacks.
- `__Http-` and `__Host-Http-` additionally require `HttpOnly`. MDN warns that browsers without prefix support accept
  prefixed cookies without the guarantees.

## Other
- Do not store session IDs, JWTs, refresh tokens or other credentials in `localStorage` or `sessionStorage`; any
  script in the origin can read them. Use `HttpOnly; Secure; SameSite=Strict` cookies (preferred) or a BFF.
- To invalidate a cookie, set an empty value and an `Expires` (or `Max-Age`) in the past.
- `Partitioned` requires `Secure`; MDN recommends a `__Host` or `__Host-Http-` prefix with it.

## Verify
Auth cookies in the browser's storage view or in `curl -sI` output carry `Secure`, `HttpOnly`, an explicit
`SameSite`, no `Domain`, and the `__Host-` prefix.

## Checked
Method: docs-checked 2026-11-09 against the MDN Set-Cookie reference (read in full) and the OWASP Session Management
Cheat Sheet (cookie attribute, prefix and storage sections). Removed unconfirmed claims and sources not read: the
RFC 6265bis draft, framework settings for Express, Django, ASP.NET Core and Spring, the ZAP rule numbers, and the
claim that CSRF token cookies cannot be HttpOnly.
