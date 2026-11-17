---
id: computing-software.email-administration.dovecot.doveadm-fts-optimize-rescan-and-flatcurve-check
name: doveadm-fts-optimize-rescan-and-flatcurve-check
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-fts, fts-rescan, fts-optimize, flatcurve, xapian, namespace]
level: advanced
status: docs-checked
description: "Maintain full text search indexes: optimize, rescan against real mailbox contents and check the flatcurve Xapian databases."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-fts.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm fts` commands act on the full text search index for the user's private namespace by default, or a named namespace such as a shared one. User selectors are the usual `-u`, `-A`, `-F` and `--no-userdb-lookup`. The default output formatter is flow.

- `fts optimize [namespace]`: optimizes the FTS index. Engines do this automatically; this forces it.
- `fts rescan [namespace]`: compares what the FTS index believes exists with what is really in mailboxes. It removes mails from the index that have been expunged, and makes sure the next `doveadm index` indexes any missing mails. The manual warns that most FTS drivers do not implement this properly and instead delete all the FTS indexes, so expect a full reindex afterwards.
- `fts flatcurve check [mailbox ...]`: runs a simple check on Dovecot's Xapian databases and attempts to fix basic errors, the same check as the `xapian-check` command with `-F`. Mailbox names accept `*` and `?`. For each mailbox that has FTS data it outputs mailbox, guid, errors (count reported by the Xapian library) and shards (index shards processed).
- Other flatcurve commands: `stats` (last_uid, messages, shards, version per mailbox), `rotate` (trigger an index rotation), `remove` (remove all FTS data for the mailbox).

After a rescan, run `doveadm index` so the missing mails are indexed again; use `fts optimize` to force optimization if searches are slow. The flatcurve check is a reasonable first step when a Xapian database appears corrupt.

Full text search backends are configured through their plugin pages (fts, fts_flatcurve, fts_solr). These doveadm commands do not choose a backend; they only manage what is configured.

## Checked

2026-11-08. Read doveadm-fts(1) in full plus its flatcurve include. Added the manual's warning that most FTS drivers delete all indexes on rescan, the check output fields, and the stats, rotate and remove subcommands; removed an unsourced recommended order.

Method: documentation only; no commands were run.
