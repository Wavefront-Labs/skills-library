---
id: computing-software.devops-ci-cd.semaphore-ui.totp-two-factor-auth
name: totp-two-factor-auth
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [totp, two-factor, mfa, authentication, recovery, semaphore-ui]
level: practitioner
status: docs-checked
description: "Enable TOTP two-factor authentication with the mfa.totp options and manage lost devices from the CLI."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/local
  - https://semaphoreui.com/docs/admin-guide/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TOTP two-factor authentication

Goal: let users add authenticator-app codes to their accounts.

TOTP (Google Authenticator, Aegis, 1Password) is off by default and applies only to accounts that enrol.

```json
{
  "mfa": {
    "totp": {
      "enabled": true,
      "allow_recovery": true,
      "app_name": "Semaphore"
    }
  }
}
```

| Option | Effect |
|---|---|
| `mfa.totp.enabled` | Users can enrol; without it nobody can. |
| `mfa.totp.allow_recovery` | Issues one recovery code at enrolment. Using it removes the TOTP enrolment and signs the user in; they enrol again. |
| `mfa.totp.app_name` | Issuer label shown in the app; set it when you run several Semaphores. |

Users enrol from their account page. Administrators can help someone who lost a device:

```bash
semaphore users totp show --login jane
semaphore users totp disable --login jane
```

Turning `mfa.totp.enabled` off later does not delete enrolments; it only stops the second factor being asked, and turning it back on restores them.

The older example config shows an `auth.totp` block; use the `mfa.totp` keys documented on the local accounts page for current versions.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/authentication/local.md and admin-guide/configuration/config-file.md. Confirmed: TOTP off by default and per-account, the mfa.totp block and all three options, the recovery code behaviour, the two semaphore users totp commands, the effect of turning enabled off and on, and the older auth.totp block in the config file example. Removed: the sign-out and sign-in Verify step.
Method: documentation only; no commands were run.
