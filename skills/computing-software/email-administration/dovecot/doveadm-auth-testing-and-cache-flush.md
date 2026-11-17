---
id: computing-software.email-administration.dovecot.doveadm-auth-testing-and-cache-flush
name: doveadm-auth-testing-and-cache-flush
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-auth, auth-cache-flush, auth-cache-status, auth-info, passdb-test, userdb-test]
level: practitioner
status: docs-checked
description: "Test authentication with doveadm auth, simulate service and IPs through -x auth_info, flush or inspect the auth cache and pick an output formatter."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-auth.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm auth` performs authentication-related actions. `auth test` tests authentication for a user (SASL mechanism set with `-A`, default PLAIN). `auth login` tests a full login: passdb authentication plus userdb lookup. `auth lookup` is like `doveadm user` but does a passdb lookup without authenticating (`-f field` shows one field). `auth cache flush` and `auth cache status` handle the cache.

Conditions are passed with `-x name=value`, repeated for several. Names are service (imap, pop3, smtp), session, lip, rip, lport, rport, the real_lip, real_rip, real_lport and real_rport variants (the address the client actually connected to or from on this host), and `forward_<field>` for a field to forward as `%{forward:field}` to the auth process. These let you test setups where passdb or userdb results depend on variables like protocol or local IP. The user's login name is given as an argument (for example `jane` or `john@example.com`), and the password is optional; if omitted, doveadm prompts for it.

Auth cache:
- `doveadm auth cache flush [-a master_socket_path] [user-mask ...]` flushes the cache for all users, or just those matching the masks.
- `doveadm auth cache status [-a master_socket_path] [--reset]` shows cache statistics and can reset them.
- Status reports hits, misses, hit ratio, positive and negative entry counts, and cache sizes, useful for tuning cache size and TTL. `--reset` zeroes the hit, miss and insert counters after reading them.
- The socket defaults to `auth-master` under the runtime directory (`auth-client` for test and login, `auth-userdb` for lookup) and may live elsewhere if `base_dir` was changed.

Global options common to doveadm commands:
- `-D` debug, `-v` verbose with progress.
- `-o name=value` overrides a setting; repeat to override several.
- `-c file` reads a specific config, otherwise the config socket and then /etc/dovecot/dovecot.conf.
- `-O` ignores config files and uses defaults.
- `-f formatter` selects output: flow (key=value lines), json (array of objects), pager (key: value lines, records separated by form feed), tab (header plus tab-separated lines), or table (header plus aligned lines).
- Also `-k` keeps the whole environment, and `-i instance-name` picks the config for one of several instances.

Use these after changing a passdb, such as a password or a master-user setup, so cached entries do not mask the change.

## Checked

2026-11-08. Read doveadm-auth(1) in full plus the shared global-options, formatter and -x includes. Added the test, login and lookup subcommands, the full -x name list (session, lip, rip, real_* and forward_<field>), the correct formatter names (flow, json, pager, tab, table), cache status contents and the per-subcommand default sockets.

Method: documentation only; no commands were run.
