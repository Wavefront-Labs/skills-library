---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-rbac-roles-permissions-and-teams
name: grafana-rbac-roles-permissions-and-teams
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-rbac, custom-roles-api, rbac-api, datasource-permissions-config, query-permissions, teams-api, team-sync-config, folder-permissions]
level: advanced
status: gated
description: "Model Grafana access with teams, folder permissions, data source query permissions, custom RBAC roles via API/provisioning, and team sync from the identity provider."
sources: ["https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/access-control/", "https://grafana.com/docs/grafana/latest/developers/http_api/access_control/", "https://grafana.com/docs/grafana/latest/administration/data-source-management/#data-source-permissions", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-team-sync/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC, permissions and teams

## Layering
1. Basic roles: Viewer / Editor / Admin per org (+ Grafana server admin).
2. **Teams** get folder permissions (View/Edit/Admin) -> team members inherit.
3. **Data source permissions** (Enterprise/Cloud): who can Query / Edit / Admin a data source. Remove the default
   "Viewer can query" and grant teams explicitly to isolate tenants (gated: unconfirmed, source is paywalled or blocked). On OSS 13.2.4 `/api/access-control/datasources/<uid>` returned 404.
4. **Fixed and custom RBAC roles** (Enterprise/Cloud) for fine-grained actions (`dashboards:write`,
   `alert.rules:read`, `datasources:query` scoped to `datasources:uid:prom-payments`) (gated: unconfirmed, source is paywalled or blocked). The Grafana access-control docs state custom and fixed roles are for Enterprise or Cloud; `GET /api/access-control/roles` returned 404 on OSS.

## Teams API
```bash
curl -s -XPOST $G/api/teams -H "$AUTH" -H 'Content-Type: application/json' -d '{"name":"payments"}'   # -> teamId
curl -s -XPOST $G/api/teams/7/members -H "$AUTH" -d '{"userId": 42}' -H 'Content-Type: application/json'
curl -s -XPOST $G/api/folders/<folderUid>/permissions -H "$AUTH" -H 'Content-Type: application/json' \
  -d '{"items":[{"teamId":7,"permission":2}]}'           # 1 view, 2 edit, 4 admin (replaces the full list)
```
**Team sync** (Enterprise/Cloud): link a team to IdP groups (`external group id`), so membership follows
LDAP/SAML/OAuth groups on login: Team -> External group sync, or `POST /api/teams/:id/groups` (404 on OSS; the Enterprise behaviour was not run) (gated: unconfirmed, source is paywalled or blocked).

## Custom roles
Enterprise/Cloud only; the payloads below were not run (the endpoint is 404 on OSS) (gated: unconfirmed, source is paywalled or blocked).
```bash
curl -s -XPOST $G/api/access-control/roles -H "$AUTH" -H 'Content-Type: application/json' -d '{
  "name":"custom:alert-silencer","displayName":"Alert silencer","version":1,"global":false,
  "permissions":[{"action":"alert.silences:create","scope":"folders:*"},{"action":"alert.silences:read","scope":"folders:*"}]}'
curl -s -XPOST $G/api/access-control/teams/7/roles -H "$AUTH" -d '{"roleUid":"<uid>"}' -H 'Content-Type: application/json'
```
Or provision in `provisioning/access-control/*.yaml` (`roles:` and `teams:` assignments). Bump `version` on change.

## Gotchas
- Folder permission POST replaces all entries (including the default Editor and Viewer role rows: a Viewer lost sight of the folder after a team-only list was posted); GET first and merge. Changes can take about a minute to apply because of the permission cache.
- Editors can create dashboards in any folder they can edit; lock the General folder (not run) (gated: unconfirmed, source is paywalled or blocked).
- Data source permissions don't stop a user with Explore access to *another* data source pointing at the same backend (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] A user in team A can't see team B's folders or query B's data source.
- [ ] Removing a user from an IdP group removes team membership at next login.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local.
- Ran the Teams API calls (`POST /api/teams` returned `teamId` and `uid`; add member; folder permissions with `teamId`/permission 2 stored as Edit and replacing the whole list).
- Enterprise-only parts (data source permissions, fixed/custom roles, team sync, access-control provisioning) cannot run on OSS (all three endpoints returned 404); docs fetched for the edition statement. Those parts carry the gated marker, so the skill is `gated`.
