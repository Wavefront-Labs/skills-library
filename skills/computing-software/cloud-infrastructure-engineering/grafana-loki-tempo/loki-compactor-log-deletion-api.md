---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-compactor-log-deletion-api
name: loki-compactor-log-deletion-api
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [log-deletion, loki, delete-api, compactor, deletion-mode, retention-delete, gdpr-removal]
level: practitioner
status: docs-checked
description: "Delete specific log lines from Loki through the compactor delete API with deletion mode, request lifecycle and cancel window."
sources: ["https://grafana.com/docs/loki/latest/operations/storage/logs-deletion/", "https://grafana.com/docs/loki/latest/reference/loki-http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove logs that must not remain (accidentally logged secret, privacy request) before retention expires.

Prerequisites: the compactor runs with `retention_enabled: true`, `delete_request_store` is set (it names the object store that holds delete requests), and the tenant's `deletion_mode` is `filter-only` or `filter-and-delete`. Deletion works with the TSDB index (and the deprecated BoltDB Shipper). The delete endpoints are registered only when retention is enabled.
```yaml
compactor:
  retention_enabled: true
  delete_request_store: s3   # the object store that holds delete requests
limits_config:
  deletion_mode: filter-and-delete   # disabled | filter-only | filter-and-delete (default)
```
To enable deletion without enforcing retention, set `retention_period` to `0s`. The docs strongly recommend object versioning on the bucket to recover from a mistaken setting.

Create, list and cancel requests (send `X-Scope-OrgID` when multi-tenant):
```
curl -g -X POST \
 'http://loki:3100/loki/api/v1/delete?query={app="api"} |= "secret-token"&start=1730000000&end=1730086400' \
 -H 'X-Scope-OrgID: tenant-a'
curl -H 'X-Scope-OrgID: tenant-a' http://loki:3100/loki/api/v1/delete
curl -X DELETE -H 'X-Scope-OrgID: tenant-a' 'http://loki:3100/loki/api/v1/delete?request_id=<ID>'
```
`start` and `end` take RFC3339 or Unix seconds; `start` is required. A 204 response means success.

Lifecycle
- A request can be cancelled during `delete_request_cancel_period` (default 24h). To cancel one already picked up for processing, add `force=true`; data may already be partly deleted and the request is then listed as `processed`.
- `deletion_mode` values: `disabled` rejects requests with 403; `filter-only` hides matching lines at query time without removing them from storage; `filter-and-delete` hides and removes them.
- Requests with a line filter are split into pieces of at most `delete_max_interval` (24h default). Line-filter deletion is one of the compactor's most resource-intensive operations.

Gotchas
- Test the selector with a normal query first: deletion removes data permanently.
- Listing returns both processed and unprocessed requests, not cancelled ones.

## Verify
`GET /loki/api/v1/delete` lists your request; after processing, the same selector over the deleted range returns nothing.

## Checked
2026-11-03. Confirmed against the Loki "Log entry deletion" page and the HTTP API reference (delete endpoints, parameters, 204, force, listing behaviour) and the configuration reference defaults. Removed: "confirm" marker on `delete_request_store` (the docs state it is required with retention), claims that parsers are rejected, that deletion takes hours or raises space use, and the generic authentication note.
Method: documentation only; no commands were run.
