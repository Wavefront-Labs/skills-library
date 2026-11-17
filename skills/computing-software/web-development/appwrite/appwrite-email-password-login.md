---
id: computing-software.web-development.appwrite.appwrite-email-password-login
name: appwrite-email-password-login
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, email-password, sessions]
level: intro
status: docs-checked
description: "Create accounts and sign users in with email and password using the Appwrite Account service, including hashing and password-quality options."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/email-password/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: register a user and open a session with email and password from a Client SDK.

Steps:
1. Initialize the SDK client (endpoint plus `<PROJECT_ID>`) and create `new Account(client)`.
2. Sign up with `account.create({ userId: ID.unique(), email, password })`. Pass a fixed `userId` only if you need to control it.
3. Log in with `account.createEmailPasswordSession({ email, password })`. The returned session is stored by the SDK for later requests.
4. Optionally verify the email afterwards (see the verification skill). Users do not have to be verified to log in; restrict resources with the `user([USER_ID], "verified")` permission role instead.

What the docs state: passwords are hashed with Argon2. You can enable password strength requirements, a password dictionary, password history, and disallowing personal data in passwords to encourage better choices. Separate email policies (see the email policies skill) can refuse free, aliased or disposable addresses at sign-up.

Gotcha: logging in does not require a verified email, so enforce verification through permissions on resources rather than assuming unverified users cannot sign in.

Verification link: the verification page parses the `userId` and `secret` query parameters that Appwrite appends to the URL you give `createVerification`.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Email and password login (auth/email-password): `account.create` with `userId`, `email` and `password`, `account.createEmailPasswordSession`, Argon2 hashing, the unverified-login rule and the `user([USER_ID], "verified")` role, the verification page query parameters, and the password security features. Removed: the claim about enabling the method in Auth > Settings, and the `account.get()` and Console Verify step.
Method: documentation only; no commands were run.
