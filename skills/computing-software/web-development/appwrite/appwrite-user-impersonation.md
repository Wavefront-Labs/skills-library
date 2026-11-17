---
id: computing-software.web-development.appwrite.appwrite-user-impersonation
name: appwrite-user-impersonation
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, impersonation, support, users]
level: advanced
status: docs-checked
description: "Let a trusted operator act as another user by ID, email or phone for debugging and support, with the impersonatorUserId audit hint."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/impersonation/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/rest/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reproduce what a customer sees without their credentials.

Setup:
1. Grant the `impersonator` capability to an internal user, either in Console under Auth > Users (toggle on the profile) or via the Users API by setting `impersonator` to true (`users.updateImpersonator`). Use one dedicated operator account per person. This capability also grants the `users.read` scope so tools can list and search users.
2. The operator signs in normally with any supported flow. In server flows an API key alone is not enough; a valid operator session must be on the client.
3. Set exactly one target on the client: `.setImpersonateUserId('<TARGET_USER_ID>')`, `.setImpersonateUserEmail('user@example.com')` or `.setImpersonateUserPhone('+12065550100')`.
4. Requests now run with the target user's permissions.

Detect it: the user model includes `impersonatorUserId` while impersonating, so you can show a banner or block risky actions. REST uses the headers `X-Appwrite-Impersonate-User-Id`, `X-Appwrite-Impersonate-User-Email` or `X-Appwrite-Impersonate-User-Phone`.

Gotcha: only one target at a time; create a fresh client or replace the value to switch users.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/impersonation, apis/rest. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify; REST impersonation headers now backed by the REST page (added to sources); Gotcha kept as the page states (one value at a time).

Method: documentation only; no commands were run.
