---
id: computing-software.web-development.nuxt.nuxt-usecookie-basics-options
name: nuxt-usecookie-basics-options
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usecookie, cookies, ssr, composables]
level: practitioner
status: docs-checked
description: "Read and write cookies SSR-safely with useCookie and its options: default, maxAge, expires, httpOnly, secure, sameSite, encode and decode."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-cookie.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`const cookie = useCookie(name, options)` returns a Vue ref bound to a cookie, working on server and client in pages, components and plugins. It only works in the Nuxt context. Values are serialised to and from JSON automatically. Updating the ref updates the cookie unless `readonly` is set.

```ts
const counter = useCookie('counter')
counter.value ||= Math.round(Math.random() * 1000)
counter.value = null // the docs' reset button does this
```

Options (most pass straight to the `cookie` package):
- `default: () => T | Ref<T>`: value when the cookie does not exist (the function may return a Ref).
- `decode` / `encode`: custom functions. Defaults are decodeURIComponent plus destr, and JSON.stringify plus encodeURIComponent. If `decode` throws, the original undecoded value is returned.
- `maxAge` (seconds, rounded down), `expires` (Date or a getter), `domain`, `path` (default `/`), `sameSite` (`true` = Strict, `false` = unset, or `'lax'`, `'none'`, `'strict'`), `secure`, `httpOnly`, `partitioned` (not yet fully standardised; clients may ignore it).
- `watch` (default `true`, deep), `'shallow'` or `false`; `readonly`; `refresh` (v4.4).
- With neither `expires` nor `maxAge` set, the cookie is session-only. If both are set they should point to the same time, since not all clients let `maxAge` take precedence.

Cautions from the page: with `httpOnly: true`, compliant clients will not let client-side JavaScript see the cookie in `document.cookie`. With `secure: true`, compliant clients will not send the cookie back over a non-HTTPS connection, which can lead to hydration errors.

In server API routes use h3's `getCookie(event, 'counter')` and `setCookie(event, 'counter', value)`.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/4.api/2.composables/use-cookie.md. Confirmed against the page: signature behaviour, option names, defaults, the secure and httpOnly warnings and the API-route helpers. Removed: the invented Verify step, the unsupported advice to set httpOnly cookies in a server handler, and the theme/locale "typical use" cross-reference.

Method: documentation only; no commands were run.
