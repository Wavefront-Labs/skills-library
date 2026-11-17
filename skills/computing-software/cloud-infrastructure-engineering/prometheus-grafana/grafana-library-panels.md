---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-library-panels
name: grafana-library-panels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [library-panel-management, library-panels, grafana-dashboards, grafana-api, terraform-grafana]
level: practitioner
status: gated
description: "Create, reuse, update and unlink Grafana library panels, find which dashboards use them, and manage them via API or Terraform since file provisioning lacks them."
sources: ["https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/manage-library-panels/", "https://grafana.com/docs/grafana/latest/developers/http_api/library_element/", "https://registry.terraform.io/providers/grafana/grafana/latest/docs/resources/library_panel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library panels

A library panel is a reusable panel stored once; every dashboard linking it shows the same definition, and editing it updates all of them.

## UI workflow
- Create: panel menu > More > New library panel; choose a folder (permissions follow the folder).
- Reuse: Add > Import from library.
- Update: edit from any dashboard, "Save library panel" (affects all connected dashboards).
- Unlink: panel menu > Unlink library panel, to customise one copy.
- Dashboards > Library panels lists them with connection counts.

## API
```bash
# list (response shape: `{"result":{"totalCount","elements","page","perPage"}}`)
curl -s -H "Authorization: Bearer $TOKEN" "$GRAFANA/api/library-elements?perPage=100" | jq '.result.elements[] | {uid,name,folderUid}'
# which dashboards use one
curl -s -H "Authorization: Bearer $TOKEN" "$GRAFANA/api/library-elements/<uid>/connections"
```
In dashboard JSON a linked panel appears as `{"id": 3, "gridPos": {...}, "libraryPanel": {"uid": "...", "name": "..."}}`; the model lives in the library element. Create one with `POST /api/library-elements` and body `{"uid":"lp1","name":"CPU","folderUid":"payments","kind":1,"model":{...}}` (`kind` 1 is a panel); lookup by name: `GET /api/library-elements/name/<name>`.

## As code
- File-provisioned dashboards can reference library panel uids, but the library panel itself must exist (created via API/Terraform) first. Saving a dashboard through `POST /api/dashboards/db` that references a non-existent library panel uid still returned `status: success` (no validation), so a missing panel shows up only when the dashboard is opened.
- Terraform: `grafana_library_panel` with `model_json` is the provider resource named in the sources (resource page not re-read this session) (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Deleting a library panel with connections is blocked: `DELETE /api/library-elements/<uid>` returned `the library element has connections`; unlink first.
- Variables used in the panel must exist on every dashboard that uses it (same names).
- Exporting a dashboard "for sharing externally" can inline library panels; plain JSON export keeps references.

## Verify
- [ ] Changing a library panel's threshold updates it on all dashboards listed under connections.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 (local).
- Created a library element via the API, saved a dashboard linking it, then `GET /api/library-elements/<uid>/connections` listed the dashboard (`connectionUid`), the dashboard JSON kept `{"libraryPanel":{"name","uid"}}`, `DELETE` was refused with the message above, and the list endpoint returned `result.elements[]` with `uid`, `name`, `folderUid`. A dashboard referencing an unknown uid saved without error.
- The UI menu paths and the Terraform resource were not exercised here; the Terraform line carries the gated marker, so the skill is `gated`.
