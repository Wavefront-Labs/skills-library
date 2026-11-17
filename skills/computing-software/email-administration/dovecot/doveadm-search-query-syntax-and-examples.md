---
id: computing-software.email-administration.dovecot.doveadm-search-query-syntax-and-examples
name: doveadm-search-query-syntax-and-examples
category: computing-software
field: email-administration
product: dovecot
tags: [search-query, doveadm-search, search-keys, saved-on, mailbox-guid, imap-search]
level: practitioner
status: docs-checked
description: "Write doveadm search queries: ALL, AND by default, parenthesised OR, mailbox and mailbox-guid selectors and key examples."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-search-query.7.html
  - https://doc.dovecot.org/main/core/man/doveadm-search.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Several doveadm commands (search, fetch, expunge, move, copy, flags) take a search query to act only on matching messages. It is mostly compatible with IMAP SEARCH. All keys are case-insensitive, and the shortest valid query is `ALL`.

Combination rules:
- Multiple terms are ANDed by default: `doveadm search NEW LARGER 50k`.
- OR must be written in parentheses when mixed with ANDs, and shells need the parentheses escaped: `SAVEDON 2007-04-13 \( SEEN OR FLAGGED \)`.
- Restrict to a mailbox with `mailbox Trash` or `mailbox-guid <guid>`; for example `doveadm search mailbox Trash DELETED` lists deleted messages in Trash.

Sample keys: sequence sets (`1:100`, `1,5,*`; use `UID` for unique IDs), `ANSWERED`, `DELETED`, `DRAFT`, `FLAGGED`, `NEW`, `SEEN`, `KEYWORD $Forwarded`, `LARGER`/`SMALLER`, `FROM`, `TO`, `CC`, `BCC` (matching envelope fields), `HEADER field string` (empty string tests presence), `BODY`, `BEFORE`/`ON`/`SINCE` for internal date, `SAVEDON` and related saved-date keys, and `NOT key`.

Test destructive queries with `doveadm search` or `doveadm fetch` before running `expunge`, `move` or `flags`. For `-A` runs, search prints username and mailbox GUID with UID per match, which makes it useful for impact estimates across many accounts.

## Checked

2026-11-03. Confirmed against the doveadm-search-query(7) and doveadm-search(1) manual pages: case-insensitive keys, ALL as shortest query, AND by default, parenthesised OR with shell escaping, mailbox and mailbox-guid selectors, the example queries, sequence sets and UID, flag keys, KEYWORD, LARGER/SMALLER, envelope keys, HEADER with empty string, BODY, BEFORE/ON/SINCE (internal date), SAVEDON and the other saved-date keys, NOT, and the -A/-u output of username, mailbox-guid and uid. The earlier "missing" phrases were only differences in case or spacing. Nothing removed.

Method: documentation only; no commands were run.
