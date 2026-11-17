---
id: computing-software.web-development.appwrite.appwrite-email-otp-login
name: appwrite-email-otp-login
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, email-otp, passwordless, security-phrase]
level: practitioner
status: docs-checked
description: "Sign users in with a 6 digit emailed one-time code, optionally adding a security phrase to defend against phishing."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/email-otp/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: passwordless login using a 6 digit code delivered by email.

Steps:
1. Request the code with `account.createEmailToken` (GraphQL `accountCreateEmailToken`), passing `userId: ID.unique()` and `email`. The response returns `userId`, `secret` and `expire`; keep the returned user ID.
2. If the email address has never been used, a new account is created with the provided `userId`; if it is already attached to an account, the user ID is ignored. The user receives an email with a 6-digit one-time password.
3. Collect the code from the user and exchange it with `account.createSession` using the returned `userId` and `secret` (the code). A session is created once the secret is verified.

Security phrase: pass `phrase: true` to `createEmailToken`. Appwrite returns a randomly generated phrase to show on your login page and includes the same phrase in the email; the user checks they match. The docs say this protects against several phishing and man-in-the-middle attacks. It is disabled by default and must be enabled in the first step of the flow.

When to choose OTP over magic URL: it does not require the user to be signed into their mailbox on the same device, does not interrupt the app with a redirect, and needs no deep linking on mobile. Downsides: expires quicker and needs more user input.

Gotcha: security phrases are disabled by default and are enabled only in the first step (the token request), not at session creation.

Compared with Magic URL: Email OTP delivers a code instead of a clickable link, and both are passwordless.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Email OTP (auth/email-otp): the 6-digit code, the benefits and downsides table, new-account versus ignored user ID, the token response fields, session creation with `userId` and `secret`, and the security phrase behaviour and its default. Removed: the `t.userId` code shape and the Verify step, which are not on the page.
Method: documentation only; no commands were run.
