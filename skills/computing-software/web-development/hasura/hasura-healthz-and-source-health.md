---
id: computing-software.web-development.hasura.hasura-healthz-and-source-health
name: hasura-healthz-and-source-health
category: computing-software
field: web-development
product: hasura
tags: [hasura, health-check, healthz, source-health, deployment]
level: practitioner
status: docs-checked
description: "Use the Hasura /healthz endpoint, with strict mode for inconsistent metadata, and configure per-source health_check settings for Postgres and MS SQL."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/health-checks/healthz-check.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/health-checks/source-health-check.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reliable probes for load balancers and orchestration.

Endpoint: `GET /healthz` (available on all Hasura projects including the OSS engine). The optional `strict` parameter is `true` or `false` and defaults to `false`.
- `200, OK`: everything works.
- Inconsistent metadata objects: `strict=false` or omitted gives `200, WARN, inconsistent objects in schema`; `strict=true` gives `500, ERROR, inconsistent objects in schema`. Review the metadata; this usually follows a `metadata apply` that contained inconsistent objects.
- `500, ERROR`: the API is not working; check the logs (the `health-check-log` type).

Source health check (Postgres and MS SQL Server; badge lists Free, Enterprise and self-hosted) goes in the source entry of the `/metadata/databases/database.yaml` file, beside `configuration`:

```yaml
health_check:
  test:
    sql: SELECT 1
  interval: 10
  retries: 3
  retry_interval: 5
  timeout: 5
```
Hasura re-runs the check on the source at the configured interval. Apply with `hasura metadata apply`, or use the `pg_update_source` Metadata API with a `health_check` object. Reports: `GET /healthz/sources` on demand, or the `health-check-log` log type when enabled.

Gotcha: Console support for the source health check is not available yet; use the CLI metadata or the API.

## Checked

2026-11-04. Confirmed against the cited pages: healthz-check and source-health-check pages: strict parameter and its default, response codes and texts, health_check keys, pg_update_source, /healthz/sources, health-check-log. Removed or corrected: the `/hasura/healthz` path, the Console path, the orchestrator-restart gotcha, the claim that all five fields are in seconds (the page does not state units) and the Verify step.

Method: documentation only; no commands were run.
