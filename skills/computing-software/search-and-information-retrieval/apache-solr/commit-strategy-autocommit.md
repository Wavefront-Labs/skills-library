---
id: computing-software.search-and-information-retrieval.apache-solr.commit-strategy-autocommit
name: commit-strategy-autocommit
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [commits, autocommit, soft-commit, hard-commit, transaction-log]
level: practitioner
status: docs-checked
description: "Tune Solr hard and soft commits: autoCommit maxTime, maxDocs, maxSize, openSearcher=false, autoSoftCommit, explicit commit and softCommit, and commitPollInterval."
sources:
  - https://solr.apache.org/guide/solr/latest/configuration-guide/commits-transaction-logs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# commit-strategy-autocommit

Data is not searchable until a commit. Configure in `<updateHandler class="solr.DirectUpdateHandler2">` in `solrconfig.xml`.

- Hard commit: fsyncs index files, closes the current transaction log and opens a new one. Can optionally open a searcher.
- Soft commit: only makes changes visible; no fsync, new segment or new tlog. Not free, so set it as long as requirements allow.

`autoCommit` triggers (first reached wins): `maxDocs`, `maxTime` (ms since oldest uncommitted update; preferred for large batches), `maxSize` (tlog size, with k, m, g suffix). `openSearcher` defaults to true; set false so hard commits flush to disk without exposing changes. If `autoCommit` is absent, only explicit commits update the index.

The guide's NRT example: hard commit every 60 s with `openSearcher=false`, `autoSoftCommit` every 10 s, using `${solr.autoCommit.maxTime:60000}` style properties so they can be overridden at runtime.

Explicit: `commit=true` on an update request, plus `softCommit=true` for soft.

For TLOG and PULL replicas the commit setup also affects leader polling; set `commitPollInterval` as `hh:mm:ss`.

## Checked

2026-11-04. Confirmed against the Commits and Transaction Logs page: hard and soft commit semantics, `maxDocs`, `maxTime`, `maxSize`, `openSearcher`, NRT example, explicit commit parameters, `commitPollInterval`. Removed an unsourced sentence about shipped defaults.

Method: documentation only; no commands were run.
