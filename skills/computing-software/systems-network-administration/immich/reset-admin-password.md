---
id: computing-software.systems-network-administration.immich.reset-admin-password
name: reset-admin-password
category: computing-software
field: systems-network-administration
product: immich
tags: [reset-admin-password, password-login, lockout, oauth-login, sessions]
level: practitioner
status: docs-checked
description: "Recover a locked-out Immich admin account with immich-admin reset-admin-password, and re-enable password or OAuth login from the server container."
sources:
  - https://docs.immich.app/administration/server-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: regain admin access when the admin password is lost or a login method was disabled.

1. Open a shell in the server container:

```bash
docker exec -it immich_server bash
```

2. Reset the password:

```bash
immich-admin reset-admin-password
```

The tool prints the admin it found (ID, OAuth ID, Email, Name), then prompts "Please choose a new password (optional)" and "Invalidate existing sessions?". Answer Yes to log out every existing session, which is the safe choice if the account may be compromised. It ends with "The admin password has been updated."

If password login itself was switched off, turn it back on:

```bash
immich-admin enable-password-login
```

If OAuth login was switched off and you rely on it:

```bash
immich-admin enable-oauth-login
```

The matching `disable-password-login` and `disable-oauth-login` commands do the reverse. Only disable password login after you have confirmed OAuth sign-in works for an admin user.

To check who holds admin rights afterwards, run `immich-admin list-users` and look at the `isAdmin` field, or use `grant-admin` with the user's email to promote another account as a backup.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/server-commands (command table and examples).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
