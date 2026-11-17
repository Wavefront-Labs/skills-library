---
id: computing-software.web-development.appwrite.appwrite-jwt-act-on-behalf-of-user
name: appwrite-jwt-act-on-behalf-of-user
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, jwt, server-sdk, permissions]
level: advanced
status: docs-checked
description: "Mint short-lived JWTs so a backend using a Server SDK acts with a specific user permissions rather than API key superpowers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/jwt/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let your backend call Appwrite as the user.

Why: a Server SDK with an API key reads all resources regardless of permissions. A client built with a JWT only sees what that user may see.

Steps:
1. The user signs in directly with Appwrite (they need an active session).
2. Create the token with a Server SDK: `users.createJWT({ userId: '<USER_ID>', duration: 900 })`. This needs an API key with the `users.write` scope.
3. In your backend, build a fresh client per request: `new Client().setEndpoint(...).setProject('<PROJECT_ID>').setJWT('<JWT>')`.
4. Discard that client after the request.

Lifetime: the JWT is stateless proof of the session and expires after 15 minutes by default (configurable up to 1 hour), or when the session is deleted. A JWT cannot mint another JWT, so a leaked token cannot outlive its expiry.

In Appwrite Functions, if an authenticated user invoked the function, the `x-appwrite-user-jwt` header is passed in automatically (see the functions develop docs).

Gotcha: create a `Client` with the JWT for each request your server receives and discard it afterwards to keep your API secure.

Example from the docs: a table whose rows each have a different `read("user:...")` permission. Listing rows with a JWT for `user-a` returns only that user's row, while a client using an API key returns every row regardless of permissions.


## Checked

2026-11-04. Confirmed against the Appwrite docs page JWT login (auth/jwt): why backends use JWTs, `users.createJWT` with `userId` and `duration`, the `users.write` scope, the 15 minute default and 1 hour maximum, per-request clients, and the birthdays example comparing JWT and API key results. The functions header is documented on the functions develop page. Removed: the `X-Appwrite-JWT` REST header claim, the "can leak another user's identity" wording, and the Verify step.
Method: documentation only; no commands were run.
