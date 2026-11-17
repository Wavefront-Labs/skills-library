---
id: computing-software.collaboration-platform-administration.vikunja.paradedb-search
name: paradedb-search
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, paradedb, pg-search-extension, bm25-index, fuzzy-search, typesense-migration]
level: practitioner
status: docs-checked
description: "Enable fuzzy full-text task search in Vikunja with ParadeDB on PostgreSQL: requirements, Docker image swap, existing server setup and Typesense migration."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/paradedb.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ParadeDB is a PostgreSQL extension (`pg_search`) giving fast fuzzy full-text search without a separate service. It does not work with MySQL or SQLite.

Docker: replace the postgres image with `paradedb/paradedb:latest` using the same `POSTGRES_PASSWORD`, `POSTGRES_USER` and `POSTGRES_DB` variables and a `./db:/var/lib/postgresql` volume. No Vikunja config changes: it detects ParadeDB automatically.

Own PostgreSQL: install `pg_search` per the ParadeDB self-hosted extension guide, make sure the extension is available in the Vikunja database, restart Vikunja.

Migrating from Typesense: set up PostgreSQL with ParadeDB (migrate your database to PostgreSQL first if needed), remove the Typesense configuration, restart. Existing tasks are indexed automatically.

How it works: Vikunja creates a BM25 index on the tasks table, giving full-text search over titles and descriptions, typo tolerance and relevance ranking. The index follows task creates, updates and deletes automatically.

## Checked

2026-11-04. Confirmed against the Vikunja Full-text Search with ParadeDB page (setup/paradedb) and Full docker example: PostgreSQL-only requirement, pg_search, the Docker image and environment variables, automatic detection, existing server steps, Typesense migration steps and the BM25 index behaviour. Nothing removed.

Method: documentation only; no commands were run.
