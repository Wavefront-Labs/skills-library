---
id: computing-software.devops-ci-cd.semaphore-ui.disable-password-login
name: disable-password-login
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [password-login-disable, sso, authentication, lockout, semaphore-ui]
level: advanced
status: docs-checked
description: "Turn off password sign-in with password_login_disable once LDAP or OIDC works, and avoid locking yourself out."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/local
  - https://semaphoreui.com/docs/reference/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Disable password sign-in

Goal: force users through LDAP or OpenID Connect.

```json
{ "password_login_disable": true }
```

Effect: the password method is rejected entirely. LDAP and OIDC are unaffected. Existing local accounts keep roles and history but cannot authenticate.

Danger: the option is honoured immediately and applies to every local account, including yours. Recovering from a mistake means editing the configuration file on the server and restarting.

Safe procedure:
1. Configure the identity provider (see the LDAP and OIDC skills).
2. Sign in with a real user through it, not just reading the log, and confirm the right role.
3. Make sure an admin identity can sign in through SSO.
4. Only then set `password_login_disable`; it takes effect immediately.
5. Keep shell access to the server so you can revert the setting.

Gotchas:
- The local break-glass admin described in the local accounts skill stops working when this is on.

Verify: the login screen offers only the SSO buttons, and an SSO user signs in successfully.

## Checked

2026-11-04: checked against the local accounts page and the configuration reference. The option takes effect immediately, so the restart step is removed along with an unconfirmed CLI hash gotcha.

Method: documentation only; no commands were run.
