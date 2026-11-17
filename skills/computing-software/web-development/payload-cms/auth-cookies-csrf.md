---
id: computing-software.web-development.payload-cms.auth-cookies-csrf
name: auth-cookies-csrf
category: computing-software
field: web-development
product: payload-cms
tags: [cookies, http-only-cookies, csrf, credentials-include]
level: practitioner
status: docs-checked
description: "Use HTTP-only cookie auth, send credentials with fetch, and configure CSRF protection with the csrf allowlist."
sources:
  - https://payloadcms.com/docs/authentication/cookies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cookies and CSRF

Goal: authenticate with HTTP-only cookies safely.

Payload sets an HTTP-only cookie on login. Browsers send it automatically on direct navigation, but `fetch` needs credentials:

```ts
const response = await fetch('http://localhost:3000/api/pages', {
  credentials: 'include',
})
```

HTTP-only cookies remove many XSS risks but CSRF is still possible: a malicious page can make a logged-in user's browser send authenticated requests. Defend with the root `csrf` option, a whitelist array of URLs from which Payload will accept cookies:

```ts
export default buildConfig({
  csrf: ['https://my-app.com'],
  cors: ['https://my-app.com'],
})
```

Cookie attributes (`secure`, `sameSite`, `domain`) are set under the collection's `auth.cookies` option; use `secure: true` behind TLS in production. The `cookiePrefix` root option changes the cookie name prefix. `serverURL` is added to the `csrf` allowlist by default. Cross-domain requests need `sameSite: 'None'` with `secure: true`; `secure: true` fails on plain-http localhost.

## Checked

2026-11-04. Read authentication/cookies, authentication/overview (cookies options) and configuration/overview (csrf, cookiePrefix) in the payloadcms/payload docs. Confirmed: credentials include, csrf allowlist, cookie attributes, cookiePrefix. Removed: the DevTools instruction and the verify step (not on the pages). Added: serverURL default and cross-domain requirements.
Method: documentation only; no commands were run.
