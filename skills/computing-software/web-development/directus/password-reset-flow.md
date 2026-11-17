---
id: computing-software.web-development.directus.password-reset-flow
name: password-reset-flow
category: computing-software
field: web-development
product: directus
tags: [password-reset, reset-url, seamless-reset, allow-list]
level: practitioner
status: docs-checked
description: "Run a Directus password reset, including a seamless in-app flow with reset_url, the token parameter and PASSWORD_RESET_URL_ALLOW_LIST."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/4.email-login.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Request: `POST /auth/password/request` with `{ "email": "hello@example.com" }`. The user gets an email linking to the Data Studio reset page.
2. For your own app's page, add `reset_url` to the request body. The email links to that URL and appends the reset token as a `token` query parameter.
3. Your app reads `token`, collects the new password, then calls `POST /auth/password/reset` with `{ "token": "...", "password": "..." }`.

SDK: `client.request(passwordReset(reset_token, new_password))`. GraphQL: `auth_password_reset(token:, password:)`.

Requirements and gotchas:
- An email service must be configured to send the request mail.
- The `PASSWORD_RESET_URL_ALLOW_LIST` environment variable must be configured for the seamless flow.
- Only users on the default authentication provider can reset; users from OAuth, SAML or LDAP get no reset email.

## Checked

2026-11-04: request, reset_url and token parameter, reset endpoint, SDK and GraphQL calls, email service requirement, allow list variable and default-provider restriction confirmed against the Directus Email Login page. Reworded the allow list note (the page only says it must be configured) and removed a Verify line.

Method: documentation only; no commands were run.
