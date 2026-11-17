---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-rbac-service-accounts-and-api
name: grafana-rbac-service-accounts-and-api
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-rbac, grafana-permissions, folder-permissions, dashboard-permissions, teams, organizations, orgs, basic-roles, admin, editor, viewer, fixed-roles, custom-roles, data-source-permissions, service-accounts, service-account-tokens, api-keys, grafana-api, grafana-http-api, team-sync, folder-nesting, multi-tenancy]
level: practitioner
status: gated
description: "Model access in Grafana: orgs vs folders vs teams, basic and fixed/custom roles, folder/dashboard/data-source permissions, service accounts and tokens, and automating all of it through the HTTP API."
sources: ["https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/", "https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/access-control/", "https://grafana.com/docs/grafana/latest/administration/service-accounts/", "https://grafana.com/docs/grafana/latest/developers/http_api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC, service accounts and the HTTP API

**Goal:** teams see and edit only their own folders and data sources, automation uses
scoped service accounts instead of personal tokens, and nothing is granted by hand twice.

## 1. Units of isolation
| Unit | Isolates | Use for |
|---|---|---|
| **Organization** | everything: users, data sources, dashboards, alerting, plugins config | truly separate tenants/customers; costs duplicated setup and no cross-org dashboards |
| **Folder** (nestable) | dashboards, alert rules, library panels, permissions inherited downward | per-team ownership inside one org — the normal choice |
| **Team** | a group of users to grant permissions to | map to IdP groups via Team Sync (Enterprise/Cloud only: `POST /api/teams/<id>/groups` returned 404 on OSS 13.2.4) (gated: unconfirmed, source is paywalled or blocked) |
| **Data source permissions** (Enterprise/Cloud only: `/api/access-control/datasources/<uid>` returned 404 on OSS) | who can query a data source | tenant-scoped Mimir/Loki with per-team headers (gated: unconfirmed, source is paywalled or blocked) |
Default: one org, a top-level folder per team, team-based permissions, admin-only root.

## 2. Roles
- **Basic roles** (per org): `Admin`, `Editor`, `Viewer`, `None` (plus server-wide *Grafana
  Admin*). Set defaults in `[users] auto_assign_org_role = Viewer` and
  `[users] viewers_can_edit = false`; `[auth] ...` for role mapping from SSO.
- **Fixed roles** (RBAC, Enterprise/Cloud; OSS has the folder/dashboard permission model only; `GET /api/access-control/roles` returned 404 on OSS 13.2.4; the role names below were not checked) (gated: unconfirmed, source is paywalled or blocked):
  `fixed:dashboards:writer`, `fixed:alerting:editor`, `fixed:datasources:reader`,
  `fixed:folders:creator`, `fixed:teams:writer`, `fixed:users:reader`…
  Assign to users, teams, or basic roles.
- **Custom roles** (Enterprise/Cloud; the endpoint is absent on OSS, and the payload below was not run) (gated: unconfirmed, source is paywalled or blocked): `{"name":"custom:payments:alerts","permissions":[{"action":"alert.rules:write","scope":"folders:uid:payments"}]}` via
  `POST /api/access-control/roles` or provisioning `roles:` files. Actions follow `object:verb`,
  scopes `folders:uid:*`, `datasources:uid:*`, `teams:id:*`.

## 3. Folder and dashboard permissions (OSS model)
Permission levels `View`, `Edit`, `Admin` granted to role/team/user on a folder, inherited by
dashboards unless overridden. Pattern:
- Root: Admin role only (replace the default entries by posting a permission list without them: the list is replaced as a whole).
- `payments/` folder: team `payments` → Edit, team `sre` → Admin, role Viewer → View.
- Shared "golden" dashboards folder: everyone View, platform team Edit.
```bash
# set folder permissions (replaces the whole list)
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  https://grafana/api/folders/payments/permissions \
  -d '{"items":[{"role":"Viewer","permission":1},{"teamId":12,"permission":2},{"teamId":3,"permission":4}]}'   # 1 View, 2 Edit, 4 Admin
```
Alert rules inherit the folder's permissions; a team needs Edit on the folder to manage its rules.

## 4. Service accounts and tokens
API keys no longer exist in Grafana 13.2.4 (`GET /api/auth/keys` returns 404; they were migrated into service accounts). A service account is a non-human
user with a basic role (and RBAC roles) plus one or more tokens, each with optional expiry.
```bash
# create via API (needs Admin)
curl -X POST -H "Authorization: Bearer $ADMIN" -H 'Content-Type: application/json' https://grafana/api/serviceaccounts -d '{"name":"terraform","role":"Admin","isDisabled":false}'
curl -X POST -H "Authorization: Bearer $ADMIN" -H 'Content-Type: application/json' https://grafana/api/serviceaccounts/<id>/tokens -d '{"name":"ci-2026q4","secondsToLive":7776000}'
```
Rules: one service account per automation (Terraform, dashboard CI, alert exporter, k6
uploader), least role (on Enterprise/Cloud `Viewer` + `fixed:dashboards:writer` beats `Admin`), token expiry ≤ 90 d,
tokens in a secret manager, rotate by creating the new token before deleting the old. Token names must be unique within the org (a repeat gets `ErrTokenAlreadyExists`).
Provisioning via Terraform: `grafana_service_account` + `grafana_service_account_token` (not run here) (gated: unconfirmed, source is paywalled or blocked).

## 5. HTTP API essentials
```bash
H=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")
curl "${H[@]}" https://grafana/api/health                                  # no auth needed
curl "${H[@]}" "https://grafana/api/search?type=dash-db&query=latency"     # find dashboards
curl "${H[@]}" https://grafana/api/dashboards/uid/<uid>                    # get (dashboard + meta)
curl "${H[@]}" -X POST https://grafana/api/dashboards/db -d @payload.json  # {"dashboard":{...,"id":null,"uid":"x"},"folderUid":"payments","overwrite":true}
curl "${H[@]}" https://grafana/api/folders ; curl "${H[@]}" -X POST https://grafana/api/folders -d '{"uid":"payments","title":"Payments","parentUid":""}'
curl "${H[@]}" https://grafana/api/datasources ; curl "${H[@]}" -X POST https://grafana/api/datasources -d @ds.json
curl "${H[@]}" https://grafana/api/teams/search?query=payments ; curl "${H[@]}" -X POST https://grafana/api/teams/<id>/members -d '{"userId":7}'
curl "${H[@]}" https://grafana/api/org/users                                # org membership
curl "${H[@]}" https://grafana/api/v1/provisioning/alert-rules              # alerting provisioning API
curl "${H[@]}" "https://grafana/api/annotations?from=...&to=...&tags=deploy"
curl "${H[@]}" -X POST https://grafana/api/annotations -d '{"tags":["deploy","api"],"text":"api v2.3.1","time":1760522400000}'
curl "${H[@]}" https://grafana/api/ds/query -d '{"queries":[{"refId":"A","datasource":{"uid":"prom"},"expr":"up","instant":true}],"from":"now-5m","to":"now"}'
```
- `overwrite: true` + a stable `uid` is how CI updates dashboards idempotently; omit `id`.
- Multi-org: `X-Grafana-Org-Id: 2` header; service accounts are per org.
- Paginate `/api/search` with `limit`/`page` (`limit=5001` returned 422, so max 5000).
- Rate limits on Grafana Cloud were not checked (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- `Editor` can edit **every** dashboard it can see unless folder permissions say otherwise;
  folder permissions override basic roles only downward, so lock root.
- Viewers with `viewers_can_edit` can change panels but not save; harmless but confusing.
- Service account tokens inherit the account's role at request time; after `PATCH /api/serviceaccounts/<id>` with role `Viewer`, the Editor token got 403 on `POST /api/annotations` within about 12 s (the request sent right after the change still passed, cached).
- Team Sync requires the IdP group claim to be present in the token; see `...grafana-authentication-and-sso` (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] A member of team A cannot see folder B (`/api/search` as that user returns nothing for B).
- [ ] Every automation has its own service account with a token expiring within 90 days (`/api/serviceaccounts/search` + tokens list).
- [ ] No static admin passwords in automation (API keys cannot exist on 13.x: `/api/auth/keys` is 404).
- [ ] Root folder permissions: Admin only; `curl /api/folders/<team>/permissions` matches the documented model.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local, with a Viewer user in a team.
- Ran the section 5 calls: `/api/health` without auth, `/api/search?query=`, dashboard `POST /api/dashboards/db` with `uid` and `overwrite` (version 1 then 2; without `overwrite` the second post failed with `Dashboard already exists. Use overwrite flag to update.`), folder POST with `parentUid: ""`, teams search and add member, `/api/org/users`, annotation POST, `/api/ds/query` against Prometheus 3.15.1 (HTTP 200 frames), provisioning alert-rules list. Folder permission POST with `teamId` and levels 1/2/4 ran in the folder skill; SA token expiry and role downgrade ran as above.
- OSS check of enterprise-only endpoints: roles, team groups and data source permissions all returned 404 `Not found`.
- Docs fetched: Grafana access-control page (custom and fixed roles stated for Enterprise/Cloud). The enterprise-only rows carry the gated marker, so the skill is `gated`.
