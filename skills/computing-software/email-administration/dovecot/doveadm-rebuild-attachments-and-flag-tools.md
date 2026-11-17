---
id: computing-software.email-administration.dovecot.doveadm-rebuild-attachments-and-flag-tools
name: doveadm-rebuild-attachments-and-flag-tools
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-rebuild, attachment-flags, search-query, rebuild-attachments]
level: intro
status: docs-checked
description: "Recompute attachment indicators with doveadm rebuild attachments using a search query, and how its output and user selectors work."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-rebuild.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm rebuild attachments` rebuilds the attachment presence indicator for messages matching a search query. It prints each matching message UID; with `-A` or a wildcard `-u` it prints username and UID. Default output formatter is flow without the `key=` prefix.

Selection forms: all users with `-A`, users listed in a file with `-F`, the `USER` environment variable with `--no-userdb-lookup`, or specific users with `-u`. The final argument is the search query that picks the messages to reset, for example `doveadm rebuild attachments -u bob ALL` rebuilds user bob's attachment status for every message.

Use it when attachment indicators are stale, for example after changing attachment-related settings. The search query argument uses the doveadm search query language (the manual page's own example is `ALL`).

Scope any bulk change with a mailbox criterion and test the query with `doveadm search` first. `-A` runs require a userdb that can iterate users, so SQL and LDAP iterate settings (`userdb_sql_iterate_query`, `userdb_fields`, `userdb_ldap_iterate_fields`) need to match your schema. `-S` runs the command through a UNIX socket or `hostname:port`.

## Checked

2026-11-08. Read doveadm-rebuild(1) in full. Removed claims about doveadm flags, move and copy that the cited page does not cover, and adjusted tags to match.

Method: documentation only; no commands were run.
