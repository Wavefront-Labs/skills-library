---
id: computing-software.systems-network-administration.navidrome.navidrome-doctor-and-search-rebuild
name: navidrome-doctor-and-search-rebuild
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, doctor, integrity-check, foreign-keys, search-rebuild, fts, database-corruption, sqlite-recover]
level: advanced
status: docs-checked
description: "Diagnose a corrupt Navidrome database with navidrome doctor, decide between search rebuild, backup restore and SQLite recover, and fix search that misses items."
sources: ["https://www.navidrome.org/docs/usage/admin/cli/doctor/", "https://www.navidrome.org/docs/usage/admin/cli/search/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome doctor and search rebuild

Use `navidrome doctor` when logs show `database disk image is malformed` or every scan fails. It is read-only and takes no flags beyond the globals.

It runs:
1. Integrity check: finds file corruption. If only the full-text search index is damaged it tells you to run `navidrome search rebuild`. Other damage cannot be repaired automatically: restore with `navidrome backup restore` or try SQLite's `.recover`. The check stops after a fixed number of problems, and when it hits the limit it will not suggest a search rebuild because the damage may be larger.
2. Foreign key check: orphaned rows pointing at rows that no longer exist; not corruption. `navidrome scan -f` clears some in library data, others need manual deletion.

Healthy output ends with `Database is healthy.`. Exit status is 1 on any problem or if it cannot finish, so `navidrome doctor || exit 1` works in scripts.

`navidrome search rebuild [-f]` deletes the FTS index and rebuilds it from library data, losing nothing, and validates the new index before saving. Also try it when search misses items in the library, because doctor cannot detect an index that is out of sync but not corrupt. It asks for `YES` unless `--force`. Stop Navidrome first:

```bash
docker compose stop navidrome
docker compose run --rm navidrome search rebuild
docker compose start navidrome
```

## Checked

2026-11-04. Confirmed against the Navidrome `doctor` and `search` CLI pages: read-only behaviour, the two checks, problem limit, exit status, healthy output, rebuild behaviour, the two use cases, YES prompt and stop-first rule. Nothing removed.

Method: documentation only; no commands were run.
