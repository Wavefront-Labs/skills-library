---
id: computing-software.cybersecurity-defensive.authelia.password-reset-and-change-options
name: password-reset-and-change-options
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, password-reset, jwt, identity-validation, password-change, refresh-interval, custom-url]
level: practitioner
status: docs-checked
description: "Configure Authelia's password reset JWT (secret, lifespan, algorithm) and the switches that disable reset or change or point to an external reset service."
sources:
  - https://www.authelia.com/configuration/identity-validation/reset-password/
  - https://www.authelia.com/configuration/first-factor/introduction/
  - https://www.authelia.com/configuration/notifications/events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reset by email works through an HMAC-signed JWT that Authelia issues itself.

```yaml
identity_validation:
  reset_password:
    jwt_secret: '<RESET_JWT_SECRET>'
    jwt_lifespan: '5 minutes'
    jwt_algorithm: 'HS256'
```

- `jwt_secret` is required; it signs the token with HMAC. Use random printable ASCII, strongly recommended as a random alphanumeric string of 64 or more characters. The page's example leaves it empty.
- `jwt_lifespan` (default 5 minutes) is how long the token stays valid after generation.
- `jwt_algorithm` must be `HS256`, `HS384` or `HS512`.

Related switches live under `authentication_backend`:

```yaml
authentication_backend:
  refresh_interval: '5m'
  password_reset:
    disable: false
    custom_url: ''
  password_change:
    disable: false
```

- `password_reset.disable` removes reset from the web frontend. A `custom_url` (must be `http` or `https`) replaces the built-in flow and disables its endpoints.
- `password_change.disable` stops users changing passwords in the portal.
- `refresh_interval` controls how often groups, email and display name are re-read from the backend; default 5 minutes, but `always` for the file provider. `always` and `disable` are also accepted.
- `registration.custom_url` (must be `http` or `https`, otherwise rejected at startup) only adds a login page link to your own registration service, opened in a new tab. Authelia has no registration of its own.

From the requester's side the portal responds identically whether or not the user exists, to avoid leaking account existence; the events page states no email is actually sent for a nonexistent user.

Check: request a reset, confirm the notification arrives, and confirm a link older than the lifespan fails.

## Checked

2026-11-08. Read in full: identity-validation/reset-password, first-factor/introduction, notifications/events. Corrected claim that reset email is sent for nonexistent users, removed unsupported rate-limit claim, added file-provider refresh default of always.

Method: documentation only; no commands were run.
