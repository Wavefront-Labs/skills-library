---
id: computing-software.web-development.appwrite.appwrite-verify-email-phone-recovery
name: appwrite-verify-email-phone-recovery
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, verification, password-recovery, email, phone]
level: practitioner
status: docs-checked
description: "Verify a user email or phone number and run password recovery with redirect URLs, then gate resources to verified users with permission roles."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/verify-user/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/email-password/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: confirm ownership of an email or phone and let users reset a forgotten password.

Email verification:
1. The user must already be logged in. Call `account.createVerification({ url: 'https://example.com/verify' })`.
2. The email link redirects to that URL with `userId` and `secret` query parameters (mobile apps need a deep link).
3. On that page read both parameters and call `account.updateVerification({ userId, secret })`.

Phone verification:
1. Set a number with `account.updatePhone({ phone: '+12065550100', password })`.
2. Call `account.createPhoneVerification()`, then `account.updatePhoneVerification({ userId, secret })` with the code the user receives.

Restrict access: `user([USER_ID], "verified")` targets one verified user; `users("verified")` targets any verified user. Users do not need to be verified to log in. Verification triggers `users.*.verification.*` events (`.create` when a token is created, `.update` when validated).

Password recovery: `account.createRecovery({ email, url })` emails a temporary secret key; the user is redirected back to your reset URL with the secret key and email address attached as query strings. Complete it with `account.updateRecovery({ userId, secret, password })`. The link is valid for 1 hour.

Gotcha: only redirect URLs on domains added as a platform in your Appwrite Console are accepted for recovery; others are rejected to protect against redirect attacks.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/verify-user, products/auth/email-password. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify; recovery details corrected to the page (secret key and email address attached to the reset URL, link valid for 1 hour); added createRecovery/updateRecovery calls.

Method: documentation only; no commands were run.
