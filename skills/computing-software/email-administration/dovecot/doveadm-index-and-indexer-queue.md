---
id: computing-software.email-administration.dovecot.doveadm-index-and-indexer-queue
name: doveadm-index-and-indexer-queue
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-index, doveadm-indexer, indexer-worker, fts-index, max-recent, index-queue]
level: advanced
status: docs-checked
description: "Pre-index mailboxes with doveadm index, queue the work with -q to the indexer, and inspect or remove queued requests."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-index.1.html
  - https://doc.dovecot.org/main/core/man/doveadm-indexer.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm index -u user mailbox` adds unindexed messages to the index and cache files, and to the full text search database if FTS is enabled. Caching adds only fields already in the mailbox's caching decisions, so it does little for a mailbox the client has never opened. `doveadm dump` shows a mailbox's current cache decisions.

Options:
- `-q` queues the request for the indexer process rather than doing it in the doveadm process. Some storage drivers cannot handle several processes updating indexes at once, so `-q` should usually be used in production.
- `-n max_recent` skips mailboxes that have more than that many \Recent messages, avoiding needless indexing of mailboxes that are not being used.

Indexer queue commands:
- `doveadm indexer add [-h] [-n max_recent] user mailbox`: same as `index -q`. `-h` adds to the head of the queue instead of the tail.
- `doveadm indexer list user_mask`: lists queued requests, with wildcards. Requests currently being processed by an indexer-worker are not shown; use `doveadm who` to see those.
- `doveadm indexer remove user_mask [mailbox_mask]`: removes queued requests. In-progress ones are not removed; use `doveadm kick` for them.

Messages can also be added to the FTS index automatically with `fts_autoindex = yes`. Manual indexing is a sensible step after a migration or when switching FTS backends, so a user's first search is not slow. Example: `doveadm index -u bob INBOX`.

## Checked

2026-11-08. Read doveadm-index(1) and doveadm-indexer(1) in full. Content was accurate; named the fts_autoindex setting and added the documented example.

Method: documentation only; no commands were run.
