---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-nested-folders-and-permission-inheritance
name: grafana-nested-folders-and-permission-inheritance
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [nested-folders, folder-permission-inheritance, folder-permissions, grafana-rbac, folder-api]
level: practitioner
status: gated
description: "Organise Grafana dashboards and alert rules in nested folders, understand inherited permissions, and create/move folders via API and Terraform."
sources: ["https://grafana.com/docs/grafana/latest/dashboards/manage-dashboards/#folders", "https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/#folder-permissions", "https://grafana.com/docs/grafana/latest/developers/http_api/folder/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested folders and permission inheritance

Nested folders let folders contain subfolders (they are on by default in Grafana 13.2.4). Permissions granted on a parent apply to all descendants (dashboards, alert rules, library panels, subfolders).

## Design
```
Teams/
  Payments/            Payments team: Editor
    Services/
    SLOs/
  Platform/            Platform team: Editor
Shared/                Viewers: Viewer, Platform: Admin
```
- Grant at the highest folder that matches ownership; add exceptions lower down (more access only).
- Inherited permissions cannot be removed on a child; to restrict, move the content to a folder outside the parent. Tested: a team with Edit on `payments` and only View set on its child `pay-sub` could still create a dashboard in `pay-sub`.
- There is a maximum nesting depth: under a top-level folder, four levels of subfolders were created and the fifth failed with `[folder.maximum-depth-reached] folder max depth exceeded, max depth is 4`. Keep trees shallow.

## API
```bash
# create a subfolder
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  "$GRAFANA/api/folders" -d '{"uid":"payments-slos","title":"SLOs","parentUid":"payments"}'
# move a folder
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  "$GRAFANA/api/folders/payments-slos/move" -d '{"parentUid":"shared"}'
# set permissions (replaces the list, including the default Editor/Viewer role entries)
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  "$GRAFANA/api/folders/payments/permissions" -d '{"items":[{"teamId":12,"permission":2}]}'
```
Permission values: 1 View, 2 Edit, 4 Admin. List children with `GET /api/folders?parentUid=<uid>`. Terraform resources `grafana_folder` (with `parent_folder_uid`) and `grafana_folder_permission` were not run here (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Alert rules inherit folder permissions too: a user with Edit on `payments` (through a team) created a rule group in it through `POST /api/ruler/grafana/api/v1/rules/payments` (202) and in its child, but got 403 on a folder where they only had View.
- Permission changes are cached: right after `POST .../permissions` a new team member still got `access denied` on the folder; it worked about a minute later (`[rbac] permission_cache = true` is the default).
- File-provisioned dashboards with `foldersFromFilesStructure` create folders from directories; mixing with API-created folders of the same title can duplicate (not run here) (gated: unconfirmed, source is paywalled or blocked).
- Moving a folder changes who can see everything inside it, instantly.

## Verify
- [ ] A user from another team cannot see Payments dashboards; Payments editors can edit rules in their folders only.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local, admin basic auth plus a Viewer user in a team.
- Ran the three curl calls: create subfolder (`parentUid`), move (`/move` with `parentUid`, version bumped, `parentUid` changed), set permissions with `teamId` and permission 2 (stored as `Edit`); `GET /api/folders?parentUid=`.
- Inheritance and cache behaviour, the depth limit (error text above) and the alert-rule permission were exercised as a real user in a team. The GET permissions list on a child did not show inherited entries.
- Terraform resources and `foldersFromFilesStructure` were not run: gated markers, so the skill is `gated`.
