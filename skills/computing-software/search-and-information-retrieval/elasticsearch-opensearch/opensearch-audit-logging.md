---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.opensearch-audit-logging
name: opensearch-audit-logging
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, opensearch-audit-logging]
level: advanced
status: docs-checked
description: "Enable OpenSearch security audit logs: storage type, audit.yml categories, ignore_users, body logging, sensitive headers and storage sinks, avoiding noise and sensitive data."
sources:
  - https://docs.opensearch.org/latest/security/audit-logs/index/
  - https://docs.opensearch.org/latest/security/audit-logs/storage-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch security audit logging

**Goal:** traceable access with the Security plugin's audit logs, without flooding storage or leaking data.

## Enable (standard mode)
- Standard mode needs the Security plugin with fine-grained access control and is configured through `audit.yml` (in the security index), Dashboards (Security, Audit logs) and the REST API. Standalone mode (SSL-only or security disabled) is configured in `opensearch.yml` and dynamic cluster settings.
- Audit logging is disabled by default. Add `plugins.security.audit.type: internal_opensearch` to `opensearch.yml` on each node and restart. It needs both a storage type and `config.enabled: true` in `audit.yml`; the shipped `audit.yml` already sets `config.enabled` to true, so until you set a storage type nothing is recorded and a startup warning is logged.
- Storage types (`plugins.security.audit.type`): `debug` (stdout), `internal_opensearch`, `internal_opensearch_data_stream`, `external_opensearch`, `webhook`, `log4j`. The default index is a daily rolling `security-auditlog-YYYY.MM.dd` (override with `plugins.security.audit.config.index`). Audit logs can use a lot of space.
- To disable: remove the audit type setting, or switch off audit logging in Dashboards.

## Categories (tracked events)
FAILED_LOGIN, AUTHENTICATED, MISSING_PRIVILEGES (transport only), GRANTED_PRIVILEGES (transport only), SSL_EXCEPTION, `opensearch_SECURITY_INDEX_ATTEMPT`, BAD_HEADERS. CLUSTER_SETTINGS_CHANGED and INDEX_SETTINGS_CHANGED are disabled by default; REQUEST_AUDIT and TRANSPORT_AUDIT are generated in standalone mode only.
- Exclude categories in `audit.yml` under `config.audit` with `disabled_categories` (both layers); `disabled_rest_categories` and `disabled_transport_categories` are the layer-specific forms (deprecated in `opensearch.yml`). `NONE` logs everything.
- `enable_rest` and `enable_transport` can switch a layer off.

## Reduce noise and protect data
- `log_request_body: false` stops request bodies being logged (default is to include them). `body_logging_exclusions` suppresses bodies for chosen actions or REST paths only (for example bulk) and applies only when `log_request_body` is true; its action groups are static and need a restart.
- `exclude_sensitive_headers: true` removes sensitive headers such as `Authorization`.
- `ignore_users` excludes users (default excludes only `kibanaserver`; `NONE` logs all); `ignore_requests` excludes actions or paths such as `indices:data/read/*`.
- `resolve_bulk_requests: true` logs each bulk operation separately and can create a very large number of events; the docs advise against it with frequent `_bulk` use.
- Audit events are written asynchronously with a thread pool (default size 10).
- Compliance settings (`compliance:` section) can log changes to the security index (`internal_config`) and watched indices.

## Shipping
Write to a separate system with `external_opensearch` (needs `http_endpoints`, TLS settings and credentials), `webhook` (format `URL_PARAMETER_GET`, `URL_PARAMETER_POST`, `TEXT`, `JSON` or `SLACK`) or `log4j` (any Log4j appender; logger name `audit`, level `INFO` by default). Whether a separate system can be edited by cluster admins is a deployment choice outside these pages.

## Verify
- [ ] A failed login appears in the audit index (or sink) with category FAILED_LOGIN.

## Notes
- Try every change on a test cluster first; defaults and settings differ between OpenSearch versions.

## Checked
2026-11-08. Confirmed against the OpenSearch "Audit logs" and "Audit log storage types" pages. Removed: Elasticsearch reference link (unrelated to this OpenSearch feature) and the unreferenced "READ events" claim.
Method: documentation only; no commands were run.
