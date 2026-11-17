---
id: computing-software.email-administration.mailcow.mailcow-dovecot-flatcurve-full-text-search
name: mailcow-dovecot-flatcurve-full-text-search
category: computing-software
field: email-administration
product: mailcow
tags: [full-text-search, flatcurve, fts-procs, fts-heap, fts-reindex, vmail-index, solr-removal]
level: advanced
status: docs-checked
description: "Operate the Flatcurve full-text search engine that replaced Solr in mailcow (January 2025): sizing variables, reindexing, repair and removal commands."
sources: ["https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-fts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dovecot Flatcurve full-text search in mailcow

As of January 2025 Flatcurve replaced Solr. Old Solr indices are obsolete (mailcow prompts to remove `solr-vol-1` during updates) and the two engines are not compatible, so a full reindex is needed. Flatcurve needs no extra volume; each IMAP folder gets an `fts-flatcurve` directory inside the `vmail-index` volume.

Indexing starts automatically once 20 or more mails arrive or a full-text search is run. Manual reindexing should be supervised because load can still spike.

Commands run in `dovecot-mailcow` via `docker compose exec`:
- repair an existing index (drops entries for deleted mail, does not reindex): `doveadm fts rescan -u user@domain` or `-A`
- reindex now: `doveadm index -u user@domain '*'` or `doveadm index -A '*'`
- delete the index: `doveadm fts-flatcurve remove -u user@domain '*'` or `-A '*'`

`mailcow.conf` options: `SKIP_FTS=y` disables search (default `n`; advised for low-end systems, dual-core and single-core machines). `FTS_PROCS` sets concurrent indexing processes (default 1); each fully uses a CPU thread, so plan about half your threads. `FTS_HEAP` is memory per process (default 128 MB; 512 MB ideal; with under 8 GB RAM stay at 128 or 256 MB and use fewer processes).

Substring search can be enabled with `fts_flatcurve_substring_search=yes` in the `plugin` block of `data/conf/dovecot/conf.d/fts.conf` (then `docker compose restart dovecot-mailcow`) for more detailed matches at the cost of storage and indexing time.

## Checked

2026-11-04. Confirmed on the Full-Text Search page: Flatcurve replaced Solr in January 2025, solr-vol-1 prompt, no extra volume, vmail-index fts-flatcurve folders, reindex needed after Solr, automatic indexing at 20 or more mails, the rescan, index and fts-flatcurve remove commands, SKIP_FTS default n, FTS_PROCS default 1 and the half-threads advice, FTS_HEAP default 128 MB with 512 MB ideal and the under-8 GB advice. Added the exact substring-search setting and restart from the page.

Method: documentation only; no commands were run.
