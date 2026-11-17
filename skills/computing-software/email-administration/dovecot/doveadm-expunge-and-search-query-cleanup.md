---
id: computing-software.email-administration.dovecot.doveadm-expunge-and-search-query-cleanup
name: doveadm-expunge-and-search-query-cleanup
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-expunge, search-query, trash-cleanup, doveadm-search, doveadm-fetch, delete-empty-mailbox]
level: practitioner
status: docs-checked
description: "Expunge old messages with doveadm expunge using a search query, test the query first with doveadm search or fetch, and scope by user."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-expunge.1.html
  - https://doc.dovecot.org/main/core/man/doveadm-search-query.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm expunge` expunges mails that match a search query. It is typically used to clear old mail from Trash or Spam. To preview which messages a query matches, run the same query through `doveadm fetch` or `doveadm search` before deleting anything.

User selection mirrors other doveadm mail commands:
- `-A`: all users. With system users from the passwd userdb this includes users below `first_valid_uid`, so it is not recommended there.
- `-F file`: users listed one per line.
- `USER` environment variable with `--no-userdb-lookup`.
- `-u user`: specific users, with `*` and `?` wildcards such as `*@example.org`.

`-d` deletes the mailbox if it is empty after expunging. `-S` selects a socket (UNIX path or `hostname:port`) to run the mail command elsewhere.

For `-A` with SQL or LDAP userdbs, make sure the iterate settings (`userdb_sql_iterate_query`, or `userdb_fields` and `userdb_ldap_iterate_fields`) match your layout, or the command cannot enumerate users.

The query uses the doveadm search query language. A mailbox parameter is required, and so is at least one key that limits the message range; use `all` if every message is wanted. A typical cleanup is a mailbox selector plus a saved-before age condition:

`doveadm expunge -u jane.doe@example.org mailbox Spam savedbefore 2w`

Search keys are case-insensitive, mostly IMAP SEARCH compatible, and combined with AND by default. When mixing AND and OR, parenthesize the OR group, and escape the parentheses for the shell: `SAVEDON 2007-04-13 \( SEEN OR FLAGGED \)`. `mailbox-guid` selects a mailbox by GUID instead of name. doveadm adds `SAVEDBEFORE`, `SAVEDON` and `SAVEDSINCE` (save date, as distinct from the internal date used by `BEFORE`, `ON` and `SINCE`, or the Date: header used by `SENT*`).

Date specifications accept `13-Apr-2007`, the IMAP date-time form, `2007-04-13`, a 10-digit Unix timestamp, or an interval such as `2w`, `7days` or `1h` (units w, d, h, m, s and their long forms). Sizes accept B, k, M, G and T suffixes, as in `larger 1M`.

Always test the query with `doveadm search` first, try one user before `-A`, and keep a backup because expunging cannot be undone.

## Checked

2026-11-08. Read doveadm-expunge(1) and doveadm-search-query(7) in full plus the shared -A, -u, -S and --no-userdb-lookup includes. Removed the unsourced lazy_expunge claim, added that a mailbox parameter and a range-limiting key are required, and added date, size, OR-grouping and save-date key details.

Method: documentation only; no commands were run.
