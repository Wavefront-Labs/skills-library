---
id: computing-software.web-development.appwrite.appwrite-ssr-session-cookies
name: appwrite-ssr-session-cookies
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, ssr, cookies, server-sdk, sessions]
level: advanced
status: docs-checked
description: "Authenticate in server-rendered apps with an admin client and a per-request session client that carries the session cookie."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/server-side-rendering/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle Appwrite auth in Next.js, SvelteKit, Nuxt, Remix or similar with a Server SDK.

Two clients:
- Admin client: `new Client().setEndpoint(...).setProject(...).setKey('<API_KEY>')`. The key needs the `sessions.write` scope. Using a key lets your server bypass client rate limits; without one the server is rate limited like a single IP.
- Session client: created fresh for every request and never shared. Read the cookie named `a_session_<PROJECT_ID>` and call `setSession(value)`.

Login endpoint: take email and password from the request, call `account.createEmailPasswordSession` with the admin client, then store `session.secret` as the cookie value with the session `expire` as its lifetime. The docs recommend `httpOnly`, `secure` and `sameSite` options to prevent XSS reads and force HTTPS.

Authenticated requests: read the cookie, return 401 if missing, otherwise `sessionClient.setSession(cookie)` and call the API as that user.

Extras: forward the visitor user agent with `client.setForwardedUserAgent(req.headers['user-agent'])` for session records. For the cookie to work client-side as well, use `a_session_` naming and a custom domain on your Appwrite endpoint.

Gotcha: create a new session client for each request and never share it between requests.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/server-side-rendering. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Gotcha reworded to the page instruction (create a new client per request, never share it; the page does not say what goes wrong); removed the invented Verify.

Method: documentation only; no commands were run.
