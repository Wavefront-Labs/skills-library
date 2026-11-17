---
id: computing-software.web-development.appwrite.appwrite-custom-token-login
name: appwrite-custom-token-login
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, custom-token, server-sdk, external-auth]
level: advanced
status: docs-checked
description: "Build your own authentication flow by creating tokens with the Users API and exchanging the secret for a session from the client."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/custom-token/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/tokens/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: sign users in through logic you control (captcha, username login, Auth0 and similar).

Server side (Appwrite Function or your backend):
1. Authenticate the user by your own means first. The docs warn to confirm the user really authenticated before issuing a token.
2. Call the Users API create token endpoint with a Server SDK (`users.createToken`). The token includes a `secret`, a 6 character long hexadecimal string; you can configure the secret length and expiry when creating a token.
3. Deliver the secret over a channel of your choice rather than echoing it straight back to the browser.
4. If the client does not know its user ID, return the user ID from this step (create the user first if it does not exist).

Client side: exchange the secret using the Client SDK create session endpoint: `account.createSession({ userId, secret })`. The session is then persisted and requests run as that user.

Tokens are the same short-lived secrets used by Magic URL, Email OTP and Phone (SMS) login. Token properties: `$id`, `$createdAt`, `userId`, `secret` and `expire`. `secret` is an empty string unless the response comes from an API key or a webhook payload. A token can be used to skip authentication when you integrate providers such as Auth0 or TypingDNA.

Gotcha: skipping your own verification effectively lets anyone obtain a session for any user ID.

GraphQL equivalent of the exchange: the `accountcreateSession(userId, secret)` mutation as written on the docs page.


## Checked

2026-11-04. Confirmed against the Appwrite docs pages Custom token login and Tokens: tokens as short-lived secrets created by a Server SDK and exchanged by a Client SDK, `users.createToken`, the 6 character hexadecimal secret with configurable length and expiry, the validate-first and share-over-your-own-channel warnings, returning the user ID, `account.createSession` with `userId` and `secret`, session persistence, and the token property table. Removed: the `account.get()` Verify step, which no page describes.
Method: documentation only; no commands were run.
