---
id: computing-software.collaboration-platform-administration.zulip.management-commands-usage
name: management-commands-usage
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [management-commands, manage-py-shell, list-realms, zerver-actions]
level: practitioner
status: docs-checked
description: "Run Zulip manage.py commands safely: list_realms and string_id, manage.py shell with zerver.actions, dbshell cautions, useful commands and custom commands in /etc/zulip."
sources: ["https://zulip.readthedocs.io/en/latest/production/management-commands.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip management commands

Log in as the `zulip` user, `cd ~zulip/deployments/current`, and run `./manage.py <command> --help` before `./manage.py <command> <args>`. `./manage.py help` lists everything; focus on the `[zerver]` section. Some commands suit narrow cases, and the source in `zerver/management/commands/` is short and readable.

Organizations: many commands take `-r` with the realm's numeric or string ID. `./manage.py list_realms` shows them. A single-organization server uses the empty string `''`; with subdomains use the subdomain, such as `-r it`. The `zulipinternal` realm holds system bots and is rarely relevant.

`manage.py shell` gives an IPython shell with `zerver.models` imported. Do not call `object.save()` directly: for most objects you also need cache flushes, client notifications and a `RealmAuditLog` entry. Use the matching function in `zerver.actions`, for example `do_change_user_delivery_email`.

`dbshell` opens SQL, but direct edits skip cache flushing and browser notification.

Handy commands: `send_custom_email`, `send_password_reset_email`, `change_realm_subdomain`, `change_user_email`, `change_user_role` (also grants bots `can_forge_sender`), `export_single_user`, `unarchive_channel`, `reactivate_realm`, `deactivate_user`, `delete_user` (deactivating is usually preferred), and `reset_authentication_attempt_count`.

Custom commands: do not write them inside a `deployments/` directory, because each upgrade creates a new one. Store them in `/etc/zulip`, so backups include them, and symlink them into `~zulip/deployments/current/zerver/management/` after each upgrade. Docker runs commands inside the container.

## Checked

Confirmed against the Management commands page: running commands as the zulip user, list_realms and string IDs, the manage.py shell and zerver.actions advice, the dbshell caution, the listed commands and the custom command storage advice. Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/management-commands.md in the zulip/zulip repository (main), the source of the cited page.
