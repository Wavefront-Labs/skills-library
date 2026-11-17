---
id: computing-software.email-administration.dovecot.dsync-sync-algorithms-and-options
name: dsync-sync-algorithms-and-options
category: computing-software
field: email-administration
product: dovecot
tags: [dsync-fast-sync, dsync-full-sync, stateful-sync, dsync-state, remote-sync, namespace-sync]
level: advanced
status: docs-checked
description: "Pick dsync fast, full or stateful synchronization, reverse sync direction and remote targets, plus userdb iteration pitfalls."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-sync.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three algorithms:
- Full sync (`-f`) scans every message in every mailbox. It guarantees everything is synchronized but is slow for incremental runs.
- Fast sync (the default) finds changed mailboxes by metadata (`NEXTUID` and `HIGHESTMODSEQ`) and syncs only those. This usually works well, especially one-way.
- Stateful sync (`-s state`) is the most efficient. It saves the earlier run's state and passes it to the next run, so only changes since then are sent.

Useful options:
- `-1`: one-way sync preserving destination changes.
- `-R`: reverse sync, pulling from the remote instead of pushing.
- `-P`: run `doveadm purge` on the destination storage afterward (relevant to mdbox).
- `-N`: sync all namespaces; by default only the `inbox=yes` namespace is synchronized.
- `-n namespace`, `-m mailbox`, `-x exclude`: limit scope.
- `-S socket_path`: either an absolute UNIX socket path or `hostname:port` for a TCP connection to a remote doveadm.
- `--no-userdb-lookup`: use the `USER` environment variable instead of a userdb lookup.
- `-t` and `-e` bound messages by date.

Iterating users with `-A` needs a working user list. For SQL userdb, `userdb_sql_iterate_query` must match your layout; for LDAP, `userdb_fields` and `userdb_ldap_iterate_fields` must match your schema. Otherwise doveadm cannot iterate. `-F file` reads one username per line instead.

## Checked

2026-11-03. Confirmed on the doveadm-sync(1) page: full (-f), fast (default, NEXTUID and HIGHESTMODSEQ) and stateful (-s) algorithms, -1, -R, -P, -N (default only the inbox=yes namespace), -n/-m/-x, -S as UNIX socket path or hostname:port, --no-userdb-lookup, -t/-e date limits, and the -A/-F user iteration notes (userdb_sql_iterate_query, userdb_fields, userdb_ldap_iterate_fields). Nothing removed.

Method: documentation only; no commands were run.
