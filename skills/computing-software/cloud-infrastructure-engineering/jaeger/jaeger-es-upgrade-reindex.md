---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-upgrade-reindex
name: jaeger-es-upgrade-reindex
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, elasticsearch-upgrade, reindex-api, index-compatibility, painless-script]
level: sme
status: docs-checked
description: "Upgrade Elasticsearch under Jaeger and reindex jaeger-span indices from 6.x data when going through 7 to 8."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand index compatibility during upgrades.

Elasticsearch defines wire and index compatibility; index compatibility is the minimum version a node can read from. Elasticsearch 8 can read indices created by 7, so 7 to 8 needs no data migration. It cannot read indices created by 6, so 6 to 8 must go through 7 and either wait until the 6.x indices are removed or reindex them. Versions are retrievable from the root/ping endpoint.

Manual reindex, 6.x data (span indices; repeat for the other Jaeger indices): reindex into temporary indices with suffix -1, delete the old ones, reindex back without the suffix, remove the suffixed ones:
1. `curl -ivX POST -H "Content-Type: application/json" http://localhost:9200/_reindex -d @reindex.json` with source `jaeger-span-*`, dest `jaeger-span`, and a painless script appending `-1` to `ctx._index`.
2. `curl -ivX DELETE http://localhost:9200/jaeger-span-\*,-\*-1`
3. Reindex again with a script that strips the last 2 characters of the suffix.
4. `curl -ivX DELETE http://localhost:9200/jaeger-span-\*-1`

The docs note there may be a more effective migration procedure and invite sharing findings with the community.

## Checked

2026-11-03. Confirmed against the Elasticsearch page, Upgrading and Reindex sections: wire versus index compatibility, 7 to 8 needing no migration, 6 to 8 only via 7, the four reindex and delete steps with the painless scripts, the -1 suffix, and the note about a possibly more effective procedure. Nothing removed.
Method: documentation only; no commands were run.
