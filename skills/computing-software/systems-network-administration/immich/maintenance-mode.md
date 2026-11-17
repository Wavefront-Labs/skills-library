---
id: computing-software.systems-network-administration.immich.maintenance-mode
name: maintenance-mode
category: computing-software
field: systems-network-administration
product: immich
tags: [maintenance-mode, login-url, restore, immich-admin, logs]
level: practitioner
status: docs-checked
description: "Enter and leave Immich maintenance mode for restores, and recover the maintenance login URL when you get logged out."
sources:
  - https://docs.immich.app/administration/maintenance-mode
  - https://docs.immich.app/administration/server-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: put Immich into maintenance mode to perform administrative tasks such as restoring a database backup, and get back in if you lose the session.

Enter maintenance mode either way:

- In the web UI, Administration, Maintenance tab, choose "Switch to maintenance mode".
- From the server container, run the enable command:

```bash
docker exec -it immich_server bash
immich-admin enable-maintenance-mode
```

The command prints a login URL of the form `https://my.immich.app/maintenance?token=<token>`.

Maintenance mode uses its own login system. When you enable it from settings you are logged in automatically once the server comes back up.

If you are logged out, do one of the following:

- Read the Immich server logs (`docker logs immich_server`) and look for the line "Immich is in maintenance mode, you can log in using the following URL".
- Run `immich-admin enable-maintenance-mode` again to get a fresh URL.
- Run `immich-admin disable-maintenance-mode`, then re-enter through system settings.

To leave maintenance mode when you are done:

```bash
immich-admin disable-maintenance-mode
```

Treat the token URL as a secret: it is the login URL for maintenance mode.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/maintenance-mode; administration/server-commands (Enable Maintenance Mode).
Removed or reworded: the admin-level access claim.
Method: documentation only; no commands were run.
