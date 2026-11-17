---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.snapshot-repository-register
name: snapshot-repository-register
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, snapshot-repository-register]
level: practitioner
status: docs-checked
description: "Register an OpenSearch fs, s3, hdfs, azure or url snapshot repository, with verification, path.repo and read-only sharing rules."
sources:
  - https://docs.opensearch.org/latest/api-reference/snapshots/create-repository/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Register a snapshot repository

**Goal:** a working backup destination. Checked against the OpenSearch page; Elasticsearch's repository settings were not checked.
- Endpoint: `PUT` or `POST _snapshot/<REPOSITORY>` with a body of `type` and `settings` (both required). `type` is `fs`, `s3`, `hdfs`, `azure` or `url`; `s3`, `hdfs` and `azure` need the corresponding repository plugin.
- fs: `location` is required, the file system must be mounted at the same path on all cluster manager and data nodes, and the location must be listed in `path.repo`. Example body: `{"type":"fs","settings":{"location":"<SNAPSHOT_DIR>"}}`. A relative path resolves against the first `path.repo` directory.
- s3: `bucket` is required (no `s3://` prefix); `base_path`, `region`, `endpoint` (falls back to `s3.client.default.*` settings in `opensearch.yml`), `chunk_size` (default 1gb), `storage_class` (do not use `glacier` or `deep_archive`), `server_side_encryption_type` (`AES256`, `aws:kms`, `bucket_default`) are optional. `server_side_encryption` was removed in OpenSearch 3.1.0.
- Common optional settings for fs and s3: `compress` (metadata only, default false), `max_snapshot_bytes_per_sec` (default 40mb), `max_restore_bytes_per_sec` (default 0, unlimited, also limited by `indices.recovery.max_bytes_per_sec`), `readonly` (default false).
- `verify` query parameter (default `true`) checks that the repository is reachable from all cluster manager and data nodes before registering; with `false` you verify later with the Verify Snapshot Repository API.
- Updating a repository needs its full definition: settings you omit reset to their defaults.
- Sharing: if one repository is registered on several clusters, only one should write; register it with `readonly: true` on the others. A `url` repository is always read-only.
- Snapshot format can change between major versions, so register a separate repository per OpenSearch major version.

## Verify
- [ ] The Verify Snapshot Repository API (or registration with `verify` true) succeeds from all nodes.

## Checked

Checked 2026-11-08 against the OpenSearch Create or Update Snapshot Repository API page. Confirmed: types, plugin requirement, fs and s3 settings and defaults, `verify`, update behaviour, read-only sharing and the major-version advice. Removed: the verify endpoint path, the exception name and the keystore-credentials claim (none stated on the page), the claim that s3 is a plugin only in older Elasticsearch versions, and the Elasticsearch source root.

Method: documentation only; no commands were run.
