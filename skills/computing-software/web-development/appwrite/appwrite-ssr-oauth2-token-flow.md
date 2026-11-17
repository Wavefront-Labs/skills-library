---
id: computing-software.web-development.appwrite.appwrite-ssr-oauth2-token-flow
name: appwrite-ssr-oauth2-token-flow
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, ssr, oauth2, server-sdk]
level: advanced
status: docs-checked
description: "Run OAuth2 login on the server with createOAuth2Token and a success callback that turns userId and secret into a session cookie."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/server-side-rendering/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: social login in an SSR app.

Two server endpoints are required, both using the admin client (a Server SDK client with an API key that has the `sessions.write` scope).

1. Initiation endpoint (for example `/oauth`): call `account.createOAuth2Token({ provider: OAuthProvider.Github, success: 'https://example.com/oauth/success', failure: 'https://example.com/oauth/failure' })`. It returns a URL; redirect the browser to it with `res.redirect(redirectUrl)`.
2. Success callback: after authenticating with the provider the user is redirected to the `success` URL with `userId` and `secret` URL parameters. Read them, call `account.createSession({ userId, secret })` on the server, and set the returned session `secret` as the `a_session_<PROJECT_ID>` cookie (`httpOnly`, `secure` and `sameSite` are recommended).

From then on the cookie comes back with each request and you pass it to a session client with `setSession` to act as that user.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/server-side-rendering. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the provider-configuration prerequisite, the createOAuth2Session comparison, the callback-parameters Gotcha and the invented Verify (none are on the SSR page); added the sessions.write key scope and the cookie details from the page.

Method: documentation only; no commands were run.
