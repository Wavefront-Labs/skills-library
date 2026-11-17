---
id: creative-arts.design-for-form-and-experience.figma.figma-rest-api-file-access
name: figma-rest-api-file-access
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-rest-api, rest-api, access-token, figma-api, images-endpoint, webhooks, file-nodes, figma]
level: practitioner
status: docs-checked
description: "Use the Figma REST API: tokens and OAuth scopes, files and nodes, image export, comments, components, variables and webhooks for automation."
sources:
  - https://github.com/figma/rest-api-spec/blob/main/openapi/openapi.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Figma REST API

## Auth
- **Personal access token:** send as header **`X-Figma-Token: <token>`**. The spec lists OAuth **scopes** per endpoint (e.g. `file_content:read`, `file_comments:write`, `file_variables:read`, `library_content:read`); request the minimum. Keep the token in secrets (CI variable), never in repos.
- **OAuth 2** (authorization code flow with refresh URL) for user-facing tools; each endpoint lists the scopes it accepts.

## Key endpoints (base `https://api.figma.com/v1`)
- `GET /files/:key` the whole document tree (`depth` limits it; `geometry=paths` adds vector data); `GET /files/:key/nodes?ids=1:2,3:4` specific nodes.
- `GET /images/:key?ids=1:2&format=svg|png|jpg|pdf&scale=2` renders nodes and returns a map of node ID to image URL (`creative-arts.design-for-form-and-experience.figma.figma-export-settings`). `format` is one of `jpg`, `png` (default), `svg`, `pdf`; `scale` is 0.01 to 4; a `null` value in the map means that node failed to render; the spec says image URLs expire after 30 days.
- `GET /files/:key/components`, `/component_sets`, `/styles` list published library items of a file; `GET /teams/:team_id/components` for team library inventories.
- **Comments:** `GET/POST /files/:key/comments`.
- **Variables (Enterprise):** `GET /files/:key/variables/local` and `/variables/published` need a full member of an Enterprise org; `POST /files/:key/variables` bulk creates, updates and deletes variables and collections and needs an Enterprise Editor seat (token sync: `creative-arts.design-for-form-and-experience.design-systems.building-a-token-sync-pipeline`).
- **Dev resources, library analytics, webhooks v2** (`/v2/webhooks`; events include `FILE_UPDATE`, `FILE_VERSION_UPDATE`, `FILE_DELETE`, `LIBRARY_PUBLISH`, `FILE_COMMENT`, `DEV_MODE_STATUS_UPDATE`).

## Example
```bash
curl -H "X-Figma-Token: $FIGMA_TOKEN" "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=12:34" | jq '.nodes["12:34"].document.name'
curl -H "X-Figma-Token: $FIGMA_TOKEN" "https://api.figma.com/v1/images/$FILE_KEY?ids=12:34&format=svg" | jq '.images'
```
Node IDs use a colon (`12:34`).

## Practices
Cache results; request only the nodes you need; use webhooks rather than polling. Endpoints can return `429` when rate limited, so back off and retry; check Figma's rate-limit documentation for the current limits. Treat returned image URLs as expiring. The token user needs access to the file.

## Verify
- [ ] Token has minimal scopes and lives in a secret store.
- [ ] Calls request specific nodes and handle 429 with backoff.
- [ ] Automation uses webhooks and caches responses.

## Checked

2026-11-01. Confirmed against the Figma REST API OpenAPI spec (figma/rest-api-spec): `X-Figma-Token` header scheme, the scope names, the `/v1/files/{file_key}/nodes`, `/images`, `/components`, `/component_sets`, `/styles`, team components, comments, variables local/published and POST variables paths, `depth` and `geometry` parameters, image `format` enum and default, `scale` range, 30-day expiry, null-on-failure, Enterprise requirements for variables, `/v2/webhooks` and the webhook event enum, OAuth authorization code flow with refresh URL, and 429 responses. Removed: the Settings menu path, the "tiered per endpoint, plan and seat" rate-limit description, `Retry-After`, `next` cursor pagination, the `Authorization: Bearer` header and the file-URL `/design/` and `node-id=12-34` notes, none of which are in the spec.
Method: documentation only; no commands were run.
