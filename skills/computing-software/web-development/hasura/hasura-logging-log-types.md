---
id: computing-software.web-development.hasura.hasura-logging-log-types
name: hasura-logging-log-types
category: computing-software
field: web-development
product: hasura
tags: [hasura, logging, observability, log-types, enabled-log-types]
level: practitioner
status: docs-checked
description: "Choose which Hasura log types are emitted with HASURA_GRAPHQL_ENABLED_LOG_TYPES, and add query tags as SQL comments for tracing."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/logging.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/observability/overview.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/observability/query-tags.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get the logs needed without noise.

Env var `HASURA_GRAPHQL_ENABLED_LOG_TYPES` (flag `--enabled-log-types`) takes a comma separated list. Community Edition defaults: `startup, http-log, webhook-log, websocket-log, jwk-refresh-log`. Other configurable types: `query-log`, `execution-log`, `livequery-poller-log`, `action-handler-log`, `data-connector-log`, `validate-input-log`. Enterprise Edition adds configurable `http-response-log`, `api-limit-log`, `response-caching-log`, `tracing-log`, `metrics` and `health-check-log`; the page lists `api-limit-log` as the Enterprise default. Internal types such as `event-trigger`, `scheduled-trigger` and `metadata` cannot be configured.

Severity is separate: `HASURA_GRAPHQL_LOG_LEVEL` (flag `--log-level`, default `info`, order `debug > info > warn > error`). With `warn`, an enabled `query-log` (an `info` log) is not printed. Requests carry a request id (the `x-request-id` header if sent, else a UUID) that correlates `http-log` and `query-log`.

Example:

```bash
HASURA_GRAPHQL_ENABLED_LOG_TYPES=startup,http-log,webhook-log,websocket-log,query-log
```
Query tags (Pro, Enterprise and self-hosted) are SQL comments of `key=value` pairs appended to the generated SQL, such as `field_name`, `operation_name` and `parameterized_query_hash`; `request_id` is controlled by `omit_request_id`. Formats: `standard` (default), `standard_prepended` and `sqlcommenter`. They are enabled by default for all sources. Per source, set `query_tags` with `disabled`, `format` and `omit_request_id`, or call the `set_query_tags` Metadata API.

Notes:
Gotchas:
- Query tags are largely incompatible with `use_prepared_statements` because identical GraphQL queries can produce different SQL text; if both are on, set `omit_request_id` to `true`.
- Google Cloud SQL drops tag keys that are not in its prescribed list.

## Checked

2026-11-04. Confirmed against the cited pages: logging and query-tags pages: env var and flag, default Community and Enterprise types, configurable and internal types, log-level default and hierarchy, request id correlation, query-tag formats, metadata spec, set_query_tags, prepared-statement and Cloud SQL notes. Removed or corrected: the OpenTelemetry version claims (the overview page gives none), the partly-read self-correction gotcha and the Verify step.

Method: documentation only; no commands were run.
