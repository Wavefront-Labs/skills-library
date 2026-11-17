---
id: computing-software.systems-network-administration.healthchecks.api-authentication
name: api-authentication
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-key, x-api-key, read-only-key, management-api]
level: practitioner
status: docs-checked
description: "Authenticate to the Healthchecks Management API v3: per-project read-write and read-only keys, the X-Api-Key header, JSON bodies and the request rate limit."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Management API (v3 base path `/api/v3/`) manages checks and integrations.

Keys are per project. There are no account-wide keys, and a project has none by default. Create read-write and read-only keys on the Project Settings page.
- Read-write: full access to all documented endpoints.
- Read-only: works only with list checks, get a single check, list status changes and list badges. Responses omit sensitive fields (`uuid`, `ping_url`, `update_url`, `pause_url`, `resume_url`, `channels`) and add a stable `unique_key`.

Send the key as a header, or for POST requests with a JSON body, as an `api_key` field:

```
curl --header "X-Api-Key: <your-api-key>" <site-root>/api/v3/checks/
```

Conventions:
- POST bodies must be JSON, not `multipart/form-data`.
- 2xx success, 4xx client error, 5xx server error.
- Avoid more than 100 API requests per minute; beyond it you will eventually see HTTP 429.
- For empty POSTs, `--data ""` makes curl send a `Content-Length` header, which some proxies require.

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): per-project keys, no account-wide keys, read-write and read-only key scope, omitted fields and unique_key, X-Api-Key header and api_key JSON field, JSON-only POST bodies, 100 requests per minute and HTTP 429, Content-Length note. Removed: the deprecation claim for v1 and v2, the Project Settings sub-section name and the team-member key access line, none of which the page states.

Method: documentation only; no commands were run.
