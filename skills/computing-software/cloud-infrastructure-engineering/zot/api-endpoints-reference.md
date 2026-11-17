---
id: computing-software.cloud-infrastructure-engineering.zot.api-endpoints-reference
name: api-endpoints-reference
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, rest-api, oci-endpoints, extension-endpoints, swagger, mgmt-endpoint]
level: practitioner
status: docs-checked
description: "Map Zot's REST endpoints: OCI distribution routes, zot extension and auth endpoints, metrics, ORAS referrers, pprof and Swagger, with their prerequisites."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/developer-guide/api-user-guide.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/developer-guide/api-reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The API shares URL and port with the GUI and datapath tools. If authentication is not configured, anyone can use it. Authenticate with `curl -u <user>:<password>` or an API key.

OCI endpoints: `GET /v2/`, `GET /v2/_catalog`, `GET /v2/_oci/ext/discover` (lists enabled extensions), blobs `/v2/{repo}/blobs/{digest}` (DELETE, GET, HEAD), uploads `/v2/{repo}/blobs/uploads` and `/{session_id}`, manifests `/v2/{repo}/manifests/{reference}`, `GET /v2/{repo}/referrers/{digest}`, `GET /v2/{repo}/tags/list` (`n`, `last` paging).

Zot extensions:
- `GET /v2/_zot/ext/mgmt`: needs `mgmt` label and search extension; returns server configuration.
- `/v2/_zot/ext/search`: GraphQL search.
- `POST /v2/_zot/ext/cosign` and `/ext/notation`: key and certificate upload (`imagetrust` label, trust extension).
- `PUT /v2/_zot/ext/userprefs`: needs `userprefs` label plus search and ui.

Auth: `/zot/auth/apikey` (needs `"apikey": true`), `/zot/auth/login`, `/zot/auth/logout`, `/zot/auth/callback/<provider>` (OpenID provider required).

Other: `GET /metrics` (metrics extension), `GET /oras/artifacts/v1/{repo}/manifests/{digest}/referrers` (always on), `GET /v2/_zot/pprof/` (always on), `/swagger/v2/` and the GraphQL playground (debug build only).

Swagger JSON is `swagger/swagger.json` in the repo; `npx open-swagger-ui swagger.json` serves it at `localhost:3355`.

## Checked

Endpoint tables and API key section confirmed; tags/list paging confirmed on the reference page.

Method: docs-checked 2026-11-09 against zot docs developer-guide/api-user-guide.md (read in full) and api-reference.md (tags/list section).
