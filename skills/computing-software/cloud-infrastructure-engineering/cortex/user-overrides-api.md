---
id: computing-software.cloud-infrastructure-engineering.cortex.user-overrides-api
name: user-overrides-api
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [overrides, runtime-config, limits, hard-limits, api]
level: advanced
status: docs-checked
description: "Manage per-tenant limits at runtime with the Cortex User Overrides API, including enabling the module and the allowed and hard limit lists."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/overrides.md
  - https://github.com/cortexproject/cortex/blob/master/docs/configuration/v1-guarantees.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The User Overrides API lets callers view, set and delete a tenant's limit overrides over HTTP, without editing the runtime config file or restarting. The Cortex v1 guarantees page lists it as an experimental feature, with no backward compatibility promise.

The `overrides` module must be enabled explicitly; it is not in the `all` target. Run it alone or alongside others, with a runtime config file:

```bash
cortex -target=overrides -runtime-config.file=runtime.yaml
cortex -target=overrides,query-frontend,querier -runtime-config.file=runtime.yaml
```

Endpoints on `/api/v1/user-overrides`, each authenticated with the `X-Scope-OrgID` header, so a tenant manages only its own overrides:

- GET returns the tenant's overrides as JSON (an empty object `{}` if there are none).
- POST with a JSON body sets or updates specific limits and merges with existing overrides: posting only `ingestion_rate` leaves the tenant's other overrides untouched.
- DELETE removes all overrides for the tenant, returning it to the global defaults.

Validation uses the runtime config. `api_allowed_limits` lists the limit names the API may change; a POST containing any other name is rejected whole with a 400, for example "the following limits cannot be modified via the overrides API: max_series_per_query". `hard_overrides` gives per-tenant maximum values, inclusive: with a hard limit of 100000, a value of 100000 is accepted and 100001 is rejected with "limit ingestion_rate exceeds hard limit: 100001 > 100000".

```yaml
overrides:
  tenant1:
    ingestion_rate: 50000
api_allowed_limits:
  - ingestion_rate
  - max_global_series_per_user
hard_overrides:
  tenant1:
    ingestion_rate: 100000
```

The module uses the same storage backend as the runtime config (filesystem by default, S3 or GCS). Several instances can run for availability, sharing that backend.

Troubleshooting: a "user not found" message when getting overrides only means the tenant has none. Changes are picked up on the runtime config reload period (`runtime-config.period`, default 10s). A "failed to validate hard limits" error indicates a problem reading or parsing the runtime config (file access, YAML syntax, storage backend), not an exceeded limit.

## Checked

Method: docs-checked 2026-11-09 against the Cortex User Overrides API guide and the v1 guarantees page (raw markdown, both read in full). The original claim that exceeding a hard limit produces "failed to validate hard limits" was wrong and has been corrected; the guide does not say the API is experimental, but the Cortex v1 guarantees page does list the Overrides API as experimental, so that note is kept below.
