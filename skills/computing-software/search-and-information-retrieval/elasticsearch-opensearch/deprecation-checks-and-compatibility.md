---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.deprecation-checks-and-compatibility
name: deprecation-checks-and-compatibility
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, deprecation-checks-and-compatibility]
level: advanced
status: docs-checked
description: "Run deprecation info APIs and the upgrade assistant to fix removed settings and mappings before upgrading."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-migration-deprecations
  - https://www.elastic.co/docs/deploy-manage/upgrade/deployment-or-cluster
  - https://docs.opensearch.org/latest/migration-assistant/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecation checks before a major upgrade

**Goal:** no surprises on the new version.
- Elasticsearch: `GET _migration/deprecations` (or `GET /{index}/_migration/deprecations` for named indices or data streams; wildcards allowed). It needs the `manage` cluster privilege. Elastic says the API is designed for indirect use by the Upgrade Assistant and recommends using the Upgrade Assistant instead of calling it directly.
- Each issue has a `level`: `info`, `warning` (you can upgrade directly but a feature goes away or changes in the next major) or `critical` (you cannot upgrade without fixing it).
- Before upgrading, follow Elastic's Plan your upgrade and Prepare to upgrade guidance. Only upgrade to a release that has a higher version number and a later release date than the one you run (out-of-order releases), and never from a release candidate.
- OpenSearch: the Migration Assistant moves data, metadata and live traffic from Elasticsearch, OpenSearch or Solr to OpenSearch; for OpenSearch-to-OpenSearch upgrades see its upgrade guide (not read here).
- Failure mode: `critical` issues left unfixed block the upgrade.

## Verify
- [ ] The deprecation API returns no `critical` issues for the planned target.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch Get deprecation information API page, the Elasticsearch deployment and cluster upgrades page and the OpenSearch Migration Assistant page. Removed the Warning-header and log-review advice, the old-index reindex rule, the client compatibility and 7.10 fork remarks (none on the pages read). The OpenSearch upgrade guide page returned only a stub.
Method: documentation only; no commands were run.
