---
id: computing-software.web-development.elysia.sign-and-rotate-cookie-secrets
name: sign-and-rotate-cookie-secrets
category: computing-software
field: web-development
product: elysia
tags: [cookie, cookie-signature, secret-rotation, t-cookie, unsigned-transition]
level: practitioner
status: docs-checked
description: "Sign Elysia cookies with secrets and sign lists, set them globally in the constructor, rotate secrets, and migrate from unsigned cookies."
sources:
  - https://elysiajs.com/patterns/cookie.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make selected cookies tamper-evident with a signature, and change secrets without invalidating live sessions.

## Per-route signing

Pass `secrets` and `sign` as the second argument of `t.Cookie`. Elysia then signs on write and verifies on read automatically.

```ts
import { Elysia, t } from 'elysia'

new Elysia().get('/', ({ cookie: { profile } }) => {
  profile.value = { id: 617, name: 'Summoning 101' }
}, {
  cookie: t.Cookie(
    { profile: t.Object({ id: t.Numeric(), name: t.String() }) },
    { secrets: 'my-secret', sign: ['profile'] }
  )
})
```

## Global signing

Put `secrets` and `sign` in the constructor so every route gets them:

```ts
new Elysia({ cookie: { secrets: 'my-secret', sign: ['profile'] } })
```

(The config section of the page also describes a single key named `secret`: "The secret key for signing/verifying cookies".) Routes still declare their cookie shape with `t.Cookie({...})`.

## Rotation

Give `secrets` an array. The first entry signs new cookies; the older entries are still accepted for verifying.

```ts
new Elysia({ cookie: { secrets: ['new-secret', 'old-secret'] } })
```

## Moving from unsigned to signed

Append `null` to the array: `secrets: ['new-secret', 'old-secret', null]`. Unsigned cookies then pass through, while cookies that carry an invalid signature are still checked. New cookies are signed with the first secret.

## Gotchas

- Only allow `null` during the transition period; the page recommends allowing unsigned cookies only during the transition to prevent unsafe cookies.
- Put the newest secret first, or new cookies will be signed with the retiring key.
- The signature protects against modification of the cookie value by malicious actors (integrity and authenticity).

## Checked

2026-11-07. Read in full: patterns/cookie, the Cookie Signature, Using Cookie Signature, Constructor, Cookie Rotation, Unsigned Cookie Transition and Config (`secret`) sections. Confirmed `secrets` plus `sign` on `t.Cookie` and in the constructor, an array of secrets with the first signing new cookies, and `null` at the end of the array for the unsigned transition. Reworded one gotcha that called unsigned cookies "forgeable"; the page only says to limit the transition period to prevent unsafe cookies. The secret strings are placeholders.

Method: documentation only; no commands were run.
