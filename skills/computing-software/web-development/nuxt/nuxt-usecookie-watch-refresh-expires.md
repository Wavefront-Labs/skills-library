---
id: computing-software.web-development.nuxt.nuxt-usecookie-watch-refresh-expires
name: nuxt-usecookie-watch-refresh-expires
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usecookie, cookie-watch, sliding-session, cookie-refresh]
level: advanced
status: docs-checked
description: "Control when useCookie writes: deep and shallow watch, readonly behaviour, refresh for sliding expiry, and dynamic expires getters."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-cookie.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How `watch` affects writes:
- Default `true` (deep): changes are watched and written to the cookie.
- `watch: false`: the page's example mutates `user.value.score++` and notes the actual cookie is not updated.
- `watch: 'shallow'`: only top-level changes count. Pushing to the array does not update the cookie; assign a new array to save:

```ts
const list = useCookie('list', { default: () => [], watch: 'shallow' })
function add () { list.value?.push(1) } // cookie NOT updated
function save () { list.value &&= [...list.value] } // cookie updated
```

`readonly: true` disables writing on both server and client; a `default` value is still returned but never persisted to the browser.

Sliding sessions: `refresh: true` (v4.4, default false) refreshes the expiration on every explicit write, even if the value is unchanged. Expiry is not refreshed automatically; you must assign to `.value`:

```ts
const session = useCookie('session', { maxAge: 60 * 60, refresh: true, default: () => 'active' })
session.value = 'active' // expiry refreshed
```

Dynamic expiry: `expires` may be a getter such as `() => new Date(Date.now() + 60 * 60 * 1000)`. It is evaluated on every cookie write, should be pure (no side effects), and returning `undefined` creates a session cookie. Assigning a new value also refreshes the expiry.

The page also notes you should refresh `useCookie` values manually, with the `refreshCookie` util, when a cookie has changed.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/4.api/2.composables/use-cookie.md. Confirmed against the page: watch modes and examples, readonly, refresh, the expires getter and the refreshCookie note. Changed: refreshCookie is described only as the page words it (the old "re-read from the browser" detail is not on the page); removed the invented Verify step.

Method: documentation only; no commands were run.
