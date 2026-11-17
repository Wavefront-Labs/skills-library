---
id: computing-software.systems-network-administration.immich.immich-admin-commands
name: immich-admin-commands
category: computing-software
field: systems-network-administration
product: immich
tags: [immich-admin, grant-admin, list-users, revoke-admin, version]
level: practitioner
status: docs-checked
description: "Run the immich-admin CLI inside the immich_server container to list users, grant or revoke admin, toggle login methods and check schema drift."
sources:
  - https://docs.immich.app/administration/server-commands
  - https://docs.immich.app/guides/docker-help
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: perform server-side admin actions from the command line.

The `immich-server` image ships an administrative CLI, `immich-admin`. Attach to the container, then run a command:

```bash
docker exec -it immich_server bash
immich-admin <command>
```

Commands:

| Command | Effect |
| --- | --- |
| `help` | Display help |
| `list-users` | List Immich users as objects (id, email, storageLabel, isAdmin) |
| `grant-admin` | Grant admin to a user, prompts for email |
| `revoke-admin` | Revoke admin from a user, prompts for email |
| `reset-admin-password` | Reset the admin password |
| `enable-password-login` / `disable-password-login` | Toggle password login |
| `enable-oauth-login` / `disable-oauth-login` | Toggle OAuth login |
| `enable-maintenance-mode` / `disable-maintenance-mode` | Toggle maintenance mode |
| `change-media-location` | Rewrite database file paths for a new media location |
| `schema-check` | Verify migrations and detect schema drift |
| `version` | Print the Immich version |

Example:

```bash
immich-admin grant-admin
? Please enter the user email: user@example.com
Admin access has been granted to user@example.com
```

`schema-check` reports "Migrations are up to date" and "No schema drift detected" on a healthy database. If password or OAuth login gets switched off, the matching enable command turns it back on.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/server-commands; guides/docker-help.
Removed or reworded: the claim about a common lockout and the web-UI-cannot statement.
Method: documentation only; no commands were run.
