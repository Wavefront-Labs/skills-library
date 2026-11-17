---
id: computing-software.web-development.appwrite.appwrite-users-api-server-management
name: appwrite-users-api-server-management
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, users, server-sdk, api-keys]
level: practitioner
status: docs-checked
description: "Manage all project users from a server with the Users API and API key, versus the client-facing Account API."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/users/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/accounts/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right API for user management.

Account API: used for user signup and login in client applications. Signup and login methods include email password, phone (SMS), anonymous, magic URL and OAuth2.

Users API: for managing users in server applications. It can only be used with an API key and a Server SDK, and manages all users. It can create users, import users, update user info, get user audit logs and remove users.

Related options from the same docs: to act on behalf of a user from a Function or your own backend use JWT login; to troubleshoot as a user without their credentials use impersonation.

Account-level permission roles: `Role.users('verified')` and `Role.users('unverified')` grant by verification status; `Role.user('<USER_ID>', 'verified')` and `Role.user('<USER_ID>', 'unverified')` target one user.

Gotcha: the Users API works only with an API key and a Server SDK, not with a client session.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/users, products/auth/accounts. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed users.createToken/createJWT/getMFAChallenge, the bare Role.users() line, the key-scope advice and the browser Gotcha as worded, and the invented Verify (none are on the cited pages); the account-vs-user partial is not in the page source and was not opened.

Method: documentation only; no commands were run.
