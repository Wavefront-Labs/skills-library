---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.reindex-from-remote
name: reindex-from-remote
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, reindex-from-remote]
level: advanced
status: docs-checked
description: "Reindex from another cluster using source.remote, the host allow list setting, TLS settings, batch size and timeouts."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reindex-indices
  - https://docs.opensearch.org/latest/api-reference/document-apis/reindex/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reindex from a remote cluster

**Goal:** migrate data between clusters. Run the request on the destination cluster.
```
POST _reindex
{"source":{"remote":{"host":"https://<REMOTE_HOST>:9200","username":"<USER>","password":"<PASSWORD>"},"index":"old","size":1000},"dest":{"index":"new"}}
```
- `host` needs scheme, host and port, with an optional path (for example a proxy path).
- Allow list, set in the config file of every node that coordinates the reindex: Elasticsearch `reindex.remote.whitelist: ["otherhost:9200", "127.0.10.*:9200"]` (scheme ignored, comma-delimited host:port, wildcards allowed); OpenSearch `reindex.remote.allowlist: [...]` (explicit host:port, IP wildcards, several endpoints). The setting name differs between the two products.
- Use https with basic auth or an API key, or the credential is sent in plain text. Elasticsearch also accepts `api_key` (or an `Authorization` header under `headers`) in `source.remote`.
- TLS is configured in the node config file, not in the request body: `reindex.ssl.certificate_authorities`, `reindex.ssl.verification_mode` (OpenSearch: `full` default, `certificate` or `none`), keystore and truststore paths. OpenSearch says SSL settings need a cluster restart. Secure settings go in the Elasticsearch keystore.
- Remote reads buffer on heap with a default maximum of 100 MB: lower `source.size` (default batch 1000) for large documents.
- `remote.socket_timeout` and `remote.connect_timeout` default to 30 seconds in both products.
- Elasticsearch: reindex from remote does not support manual or automatic slicing, and there is no forward compatibility across major versions (no 7.x into 6.x). The `query` is sent to the remote host without validation or modification.
- OpenSearch retries failed remote requests with exponential backoff: `reindex.remote.retry.initial_backoff` (default 500ms) and `reindex.remote.retry.max_count` (default 15).
- The destination index must exist with its mappings first; reindex copies `_source` only.

## Verify
- [ ] Document counts and a sample of documents match across the clusters.

## Checked

Checked 2026-11-08 against the Elasticsearch Reindex indices examples page (Reindex from remote section) and the OpenSearch Reindex Documents API page. Confirmed: every setting name, default and restriction above. Removed: the claim that cross-major version support is limited to specific ranges (the Elasticsearch page says only that forward compatibility is unsupported and old clusters should work) and the page-root sources.

Method: documentation only; no commands were run.
