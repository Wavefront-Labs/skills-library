---
id: computing-software.web-development.hono.hono-cookie-helper
name: hono-cookie-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, cookies, security]
level: practitioner
status: docs-checked
description: "Set, read, sign and delete cookies in Hono with hono/cookie, including prefixes, generateCookie and the validation rules that throw."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/cookie.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cookie helper

Import: `import { deleteCookie, getCookie, getSignedCookie, setCookie, setSignedCookie, generateCookie, generateSignedCookie } from 'hono/cookie'`.

## Regular
```ts
app.get('/cookie', (c) => {
  setCookie(c, 'cookie_name', 'cookie_value')
  const yummyCookie = getCookie(c, 'cookie_name')
  deleteCookie(c, 'cookie_name')
  const allCookies = getCookie(c)
})
```

## Signed (async, HMAC SHA-256 via WebCrypto)
```ts
await setSignedCookie(c, 'cookie_name0', 'cookie_value', secret)
const v = await getSignedCookie(c, secret, 'cookie_name0')
const all = await getSignedCookie(c, secret)
```
`getSignedCookie` returns `false` if a signature fails verification, and `undefined` if the cookie is missing or has no valid signature format. Both are falsy, so `if (!value)` handles both. The page's example comments that the secret should be a large enough string to be secure.

## Generate strings only
`generateCookie('delicious_cookie', 'macha')` returns `'delicious_cookie=macha; Path=/'`; `await generateSignedCookie(name, value, secret, opts)` likewise. These do NOT set headers; you must add them yourself.

## Options (setCookie / setSignedCookie)
`domain`, `expires: Date`, `httpOnly`, `maxAge: number`, `path`, `secure`, `sameSite: 'Strict'|'Lax'|'None'`, `priority: 'Low'|'Medium'|'High'`, `prefix: 'secure'|'host'`, `partitioned`. `deleteCookie(c, name, { path, secure, domain })` returns the deleted value.

## Prefixes
`setCookie(c, 'delicious_cookie', 'macha', { prefix: 'secure' })` (or `'host'`); read with `getCookie(c, 'yummy_cookie', 'secure')` or `getSignedCookie(c, secret, 'fortune_cookie', 'host')`.

## Gotcha: it throws
Following RFC6265bis and CHIPS, an Error is thrown if: name starts with `__Secure-` or `__Host-` without `secure`; `__Host-` with `path` not `/` or with `domain` set; `maxAge` greater than 400 days; `expires` more than 400 days ahead.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/cookie.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); "long, random secret" (reworded to the page comment).

Method: documentation only; no commands were run.
