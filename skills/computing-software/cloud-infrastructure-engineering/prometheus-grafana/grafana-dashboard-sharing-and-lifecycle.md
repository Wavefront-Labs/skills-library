---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-dashboard-sharing-and-lifecycle
name: grafana-dashboard-sharing-and-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, dashboard-snapshots, dashboard-export-import, public-dashboards-setup, shared-dashboards, dashboard-versions, json-model, playlists, grafana-reporting]
level: practitioner
status: gated
description: "Share and manage Grafana dashboards: export/import JSON for portability, snapshots, externally shared (public) dashboards, version history/restore, playlists and PDF reports."
sources: ["https://grafana.com/docs/grafana/latest/dashboards/share-dashboards-panels/", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/modify-dashboard-settings/#dashboard-versions", "https://grafana.com/docs/grafana/latest/dashboards/create-reports/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboard sharing and lifecycle

## Export / import
- Export -> JSON with **"Export for sharing externally"** replaces data source UIDs with `${DS_PROMETHEUS}` inputs
  (`__inputs` section) so the importer picks their own data source. Without it, imports break on other instances. These are UI features (not exercised here); the API's `GET /api/dashboards/uid/<uid>` returns the dashboard with data source uids as stored (gated: unconfirmed, source is paywalled or blocked).
- Import: Dashboards -> New -> Import (JSON, file, or grafana.com dashboard ID); choose folder and data sources (UI, not run); the API equivalent `POST /api/dashboards/db` with `overwrite: true` ran.
- JSON model essentials: `uid` (stable identity, used in URLs), `title`, `version` (bumps on each save: 1, then 2 on an overwrite; saving without `overwrite` got `Dashboard already exists. Use overwrite flag to update.`), `panels[]`, `templating.list[]`, `annotations.list[]`, `schemaVersion` (all present in saved dashboards read back from the API).

## Versions
Settings -> Versions keeps history per save (`versions_to_keep` in `[dashboards]`, default 20 per `defaults.ini`). Diff two versions
(JSON diff view, UI) and **Restore** creates a new version from an old one: `POST /api/dashboards/uid/<uid>/restore` with `{"version":1}` on a dashboard at version 2 returned version 3. API: `GET /api/dashboards/uid/<uid>/versions` returns `{"continueToken":"","versions":[{...,"version":1,"message":"Initial save","data":{...}}]}`.

## Snapshots
Point-in-time copy of the rendered data (no live queries). Local snapshots live in the Grafana DB; set an
expiry (`POST /api/snapshots` with `expires: 3600` returned `key`, `deleteKey`, `url` and `deleteUrl`). Useful for incident docs. Disable external snapshot publishing (`[snapshots] external_enabled = false`; `defaults.ini` has `enabled = true`, `external_enabled = true`)
if data is sensitive.

## Externally shared (public) dashboards
Share -> Share externally (formerly Public dashboards): anonymous read-only URL with live data, time picker
optional. Limits (Grafana docs, shared-dashboards page): variables and queries using variables are not supported, only some data sources are supported (Prometheus and Loki are on the confirmed list, Tempo and Graphite are not), queries run with the dashboard's settings. Manage all shared ones under Dashboards -> Shared dashboards; revoke centrally. `[public_dashboards] enabled = true` is the default in `defaults.ini`. API run: `POST /api/dashboards/uid/<uid>/public-dashboards` with `{"isEnabled":true,"timeSelectionEnabled":false,"share":"public"}` returned an `accessToken`, and an unauthenticated `GET /api/public/dashboards/<token>` returned the dashboard and a panel query returned data frames.

## Playlists and reporting
- Playlists: rotate dashboards (by list or tag) on TV screens (not run) (gated: unconfirmed, source is paywalled or blocked); kiosk mode `?kiosk` hides chrome (the URL became `kiosk=true` and only panels rendered).
- Reporting (Enterprise/Cloud): scheduled PDF/CSV/image emails of a dashboard with a time range and variables;
  needs the image renderer and SMTP (not available on OSS, not run) (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] A dashboard exported "for sharing externally" imports into a second instance with no broken panels.
- [ ] Restoring an older version works and is itself recorded as a new version.
- [ ] Shared-externally list reviewed; nothing sensitive exposed.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local (API plus a Playwright browser for kiosk).
- Ran dashboard save with and without `overwrite`, version listing, restore, snapshot create, public dashboard create and anonymous read; read config defaults from `conf/defaults.ini`. Docs fetched: Grafana shared-dashboards page (limits and naming).
- UI export/import and reporting/playlists were not run: gated markers, so the skill is `gated`.
