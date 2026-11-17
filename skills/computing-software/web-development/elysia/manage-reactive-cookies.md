---
id: computing-software.web-development.elysia.manage-reactive-cookies
name: manage-reactive-cookies
category: computing-software
field: web-development
product: elysia
tags: [cookie, reactive-cookie, t-cookie, cookie-attributes, elysia-handlers]
level: practitioner
status: docs-checked
description: "Read, write, update and remove cookies through Elysia's reactive cookie proxy, including cookie attributes and a t.Cookie schema."
sources:
  - https://elysiajs.com/patterns/cookie.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use the `cookie` context property to get, set, validate and delete cookies without get/set helper calls.

## Basics

```ts
import { Elysia } from 'elysia'

new Elysia().get('/', ({ cookie: { name } }) => {
  name.value                // read
  name.value = 'New Value'  // write (Set-Cookie header is produced automatically)
})
```

`cookie` is a Proxy, so `cookie.name` is never `undefined`; only `cookie.name.value` can be. Objects are encoded and decoded automatically. If TypeScript warns that `cookie.name` may be undefined, add a cookie schema or disable `strictNullChecks`. Iterating the jar only yields cookies that already exist.

## Attributes

Assign properties directly: `name.domain = 'example.com'; name.httpOnly = true`. Or use methods:

- `name.set({ domain, httpOnly })` resets all attributes and overwrites them with the given values.
- `name.add({ ... })` overwrites only the properties you pass.
- Remove with `name.remove()` or `delete cookie.name`.

Supported attributes: `domain`, `encode` (default `encodeURIComponent`), `expires` (Date), `httpOnly` (default false), `maxAge` (seconds, default undefined, rounded down), `path`, `priority` (`low`/`medium`/`high`), `sameSite` (`true`=Strict, `false`, `'lax'`, `'none'`, `'strict'`), `secure` (default false).

## Typed cookies with `t.Cookie`

```ts
import { Elysia, t } from 'elysia'

new Elysia().get('/', ({ cookie: { name } }) => {
  name.value = { id: 617, name: 'Summoning 101' }
}, {
  cookie: t.Cookie({
    name: t.Object({ id: t.Numeric(), name: t.String() })
  })
})
```

Wrap a field in `t.Optional(...)` to allow the cookie to be absent.

## Gotchas

- If both `expires` and `maxAge` are set, the spec says `maxAge` wins but not every client obeys, so point both at the same instant.
- `httpOnly: true` hides the cookie from `document.cookie`; `secure: true` means clients will not send it back over plain HTTP.
- `priority` and `sameSite` are not fully standardised; some clients ignore them.

## Checked

2026-11-07. Read in full: patterns/cookie (the repo has no include files). Confirmed the get/set example, the Proxy and `strictNullChecks` warning, jar iteration, direct attribute assignment, `set` versus `add`, `remove()` and `delete cookie.name`, the attribute list with defaults (`encode`, `httpOnly` false, `maxAge` undefined and rounded down, `secure` not set by default), `priority` values, `sameSite` values, the `expires`/`maxAge` tip, `t.Cookie` and `t.Optional`. Nothing removed. Signing and rotation are covered by the separate cookie-secrets skill.

Method: documentation only; no commands were run.
