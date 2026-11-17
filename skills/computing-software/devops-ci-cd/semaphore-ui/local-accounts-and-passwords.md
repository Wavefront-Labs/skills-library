---
id: computing-software.devops-ci-cd.semaphore-ui.local-accounts-and-passwords
name: local-accounts-and-passwords
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [local-accounts, argon2id, password, authentication, semaphore-ui]
level: practitioner
status: docs-checked
description: "How local Semaphore accounts store passwords (Argon2id since 2.20) and why to keep a local admin."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/local
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local accounts and password storage

Goal: understand password sign-in against the Semaphore database.

Every install starts with a local account, created by `semaphore setup` or the `SEMAPHORE_ADMIN_*` variables. Keep at least one local administrator even after single sign-on works; it is the only way back in if the identity provider is unreachable.

Storage:
- Passwords are hashed with Argon2id using OWASP minimum-strength parameters, recorded with each hash in PHC string format.
- Releases before 2.20 used bcrypt. Old hashes still work and are replaced with Argon2id on the owner's next successful sign-in. Accounts that never sign in again keep bcrypt, so reset those passwords to upgrade.
- There is no password policy: no minimum length, complexity or expiry. Use a directory or identity provider for that.

Manage accounts in the web UI, or from the CLI when nobody can sign in:

```bash
semaphore users add --admin --login jane --name "Jane Doe" \
  --email jane@example.com --password 's3cret'
semaphore users change-by-login --login jane --password 'new-s3cret'
semaphore users list
```

Warning: a password on the command line lands in shell history and the process list. Use it for the first admin or recovery, then change it in the web UI.

Verify: `semaphore users list` shows the account and the user can sign in.

## Checked

2026-11-04: checked against the local accounts page. Every claim is stated there.

Method: documentation only; no commands were run.
