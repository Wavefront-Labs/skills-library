---
id: computing-software.devops-ci-cd.verdaccio.web-registration-and-password-change
name: web-registration-and-password-change
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [user-registration, change-password, createuser-flag, createuser, changepassword, reset-password, self-registration]
level: practitioner
status: docs-checked
description: "Turn on web UI sign-up (createUser) and self-service password change (changePassword) flags, and why max_users -1 is needed to really close registration."
sources:
  - https://verdaccio.org/docs/user-registration/
  - https://verdaccio.org/docs/change-password/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
flags:
  createUser: true
  changePassword: true
```
Both flags are experimental and default to false. Restart; with a flag off the screens and endpoints do not exist.

createUser: adds a sign-up form to the web UI. It governs web registration only. `npm adduser` is decided by the auth plugin; with htpasswd set `max_users: -1` to refuse every registration. A new user is only authenticated: what they reach depends on package rules, so avoid `publish: $authenticated` on private scopes before opening registration.

changePassword: registers `PUT /-/verdaccio/sec/reset_password` and the form at `/-/web/change-password`.
- The account comes from the session token, not the form (the username field has no effect).
- The current password is verified first.
- The new password must satisfy `server.passwordValidationRegex` if set; otherwise the registry answers 401 with a password-too-short error.
- You must be signed in. The "change password" link in the login dialog is shown only to signed-out visitors and leads to an anonymous request that fails with 401.
- The auth plugin does the change: htpasswd supports it; LDAP or identity-provider plugins typically do not.

## Checked

Method: docs-checked 2026-11-09 against the Verdaccio user-registration and change-password pages (website source, read in full); documentation only, no commands were run.
