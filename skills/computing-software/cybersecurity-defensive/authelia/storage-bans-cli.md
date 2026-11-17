---
id: computing-software.cybersecurity-defensive.authelia.storage-bans-cli
name: storage-bans-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, storage-bans, cli, regulation, ip-ban, user-ban, unban]
level: practitioner
status: docs-checked
description: "Add, list and revoke Authelia user and IP bans from the command line, including duration, permanent bans and reasons."
sources:
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_bans_ip_add/
  - https://www.authelia.com/configuration/security/regulation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bans are rows in the Authelia database, and the CLI can read and edit them.

The command tree is `authelia storage bans`, with `ip` and `user` branches, each having `add`, `list` and `revoke`.

```bash
authelia storage bans ip add 192.0.2.50 --duration '1 day' --reason 'abusive client' \
  --config /path/to/configuration.yml

authelia storage bans ip add 192.0.2.51 --permanent

authelia storage bans ip list
authelia storage bans ip revoke 192.0.2.50

authelia storage bans user add john --duration '1 day'
```

Flags of `ip add`:

- `-d, --duration`: length of the ban, default `1 day`.
- `-p, --permanent`: makes the ban effectively permanent.
- `-r, --reason`: free text recorded with the ban.

The storage commands inherit connection flags such as `--encryption-key`, `--postgres.address`, `--postgres.password` and `--mysql.address`, so you can point the CLI at a database without a configuration file. Prefer `--config` and keep credentials out of shell history.

Because stored bans apply whatever regulation modes are currently configured, `revoke` is how you lift a ban that regulation created; editing `regulation` alone will not. The `user` branch works the same way using a username: `user add <user>` takes the same `--duration`, `--permanent` and `--reason` flags, and `user list` and `user revoke [user]` mirror the ip commands. The `-c, --config` flag defaults to `configuration.yml`. Regulation itself defaults to `max_retries` 3, `find_time` 2 minutes, `ban_time` 5 minutes and mode `user`; `max_retries: 0` disables regulation, and the documentation recommends the `ip` mode.

Check: add a short ban, confirm the address is rejected at login, revoke it and confirm access returns.

## Checked

2026-11-08. Read in full: reference CLI pages for storage bans, bans ip, ip add, ip list, ip revoke, user add, user list, user revoke; configuration/security/regulation. Verified flags and argument forms; added regulation defaults.

Method: documentation only; no commands were run.
