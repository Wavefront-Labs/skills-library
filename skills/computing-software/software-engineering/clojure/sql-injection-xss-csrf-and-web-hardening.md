---
id: computing-software.software-engineering.clojure.sql-injection-xss-csrf-and-web-hardening
name: sql-injection-xss-csrf-and-web-hardening
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, security, sql-injection, xss, csrf, hiccup, ring-defaults, cors, headers, authentication, sessions, security-sql-web]
level: advanced
status: draft
description: "Prevent SQL injection with parameters, XSS with escaping (Hiccup/Selmer), CSRF with anti-forgery, and set secure headers, cookies and CORS in Ring apps."
sources: ["https://github.com/ring-clojure/ring-defaults", "https://cheatsheetseries.owasp.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL injection and web hardening

**Goal:** close the common OWASP classes of web bugs.

- SQL: always parameters (`["... where id = ?" id]`, HoneySQL values); never `(str "... " input)`. Identifiers
  (table/column names) from user input must come from an allow-list.
- XSS: Hiccup (`hiccup.core/html`) escapes strings in text and attribute positions; `hiccup.util/raw-string` and
  `(hiccup.core/html [:div (raw ...)])` bypass escaping. Selmer escapes `{{ var }}` by default; `|safe` disables.
  Set a restrictive `Content-Security-Policy`.
- CSRF: `ring.middleware.anti-forgery/wrap-anti-forgery` (included in `wrap-defaults` `site-defaults`); APIs using
  bearer tokens in headers are not CSRF-prone but need CORS controls.
- Cookies: `:http-only true`, `:secure true`, `:same-site :lax`/`:strict`; sign or encrypt session cookies with a
  strong key (`ring.middleware.session.cookie/cookie-store {:key bytes}`).
- Passwords: hash with bcrypt/argon2 (for example `buddy-hashers`), never plain SHA; compare constant-time.
- Auth: libraries such as buddy-auth for JWT/session; validate `exp`, algorithm and audience; do not accept
  `alg: none`.
- CORS: allow only known origins (`ring-cors`); do not reflect arbitrary `Origin` with credentials.
- Headers: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`; `secure-api-defaults`
  or `site-defaults` set several.
- Rate limit and log authentication failures; return generic error messages.

## Failure modes
- Trusting the `X-Forwarded-*` headers without a proxy that sets them.
- Returning stack traces to clients.

## Self-check
Submit `<script>` and `' OR 1=1 --` through a form and verify both are inert.
