---
id: computing-software.web-development.appwrite.appwrite-magic-url-login
name: appwrite-magic-url-login
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, magic-url, passwordless]
level: intro
status: docs-checked
description: "Implement passwordless sign-in where Appwrite emails a magic link and your redirect page exchanges the secret for a session."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/magic-url/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: log users in through an emailed link, no password.

Steps:
1. Start the flow with `account.createMagicURLToken({ userId: ID.unique(), email, url: 'https://example.com/verify' })`.
2. If the email has never been used, a new account is created using the supplied `userId`. If the email already belongs to an account, the `userId` you pass is ignored and the existing user gets the link.
3. The `url` parameter is where the user lands after clicking the link; Appwrite appends `secret` and `userId` as query parameters.
4. On that page parse `userId` and `secret` from `window.location.search` and call `account.createSession({ userId, secret })`.

The step 4 snippet from the docs uses `new URLSearchParams(window.location.search)` and `urlParams.get('secret')` / `urlParams.get('userId')`.

GraphQL equivalents on the page: `accountCreateMagicURLToken` and `accountCreateSession`.

Gotcha: because the user ID is ignored for existing emails, use the `userId` and `secret` from the redirect query string for the session rather than assuming the ID you generated.

Only the sign-in flow is covered here.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Magic URL login (auth/magic-url): the Create Magic URL Token call and its parameters, new-account versus existing-account behaviour, the `url` redirect with `secret` and `userId` appended, the session creation snippet and the GraphQL mutations. Removed: the Email OTP comparison (not on this page) and the Verify step.
Method: documentation only; no commands were run.
