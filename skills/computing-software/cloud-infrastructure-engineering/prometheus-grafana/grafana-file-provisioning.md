---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-file-provisioning
name: grafana-file-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, provisioning, datasource-yaml, secure-json-data, dashboard-provider, folders-from-files-structure, alerting-provisioning-files, file-provisioned-alerts, sidecar]
level: practitioner
status: gated
description: "Provision Grafana from files: data sources with secureJsonData, dashboard providers with foldersFromFilesStructure, and file-based alert rules and policies."
sources: ["https://grafana.com/docs/grafana/latest/administration/provisioning/", "https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File provisioning

Files live in `provisioning/{datasources,dashboards,alerting,plugins}/*.yaml` (path from `[paths] provisioning`, or `GF_PATHS_PROVISIONING`).
Env vars expand: `$VAR` / `${VAR}`; use them for secrets (tested: `url: http://127.0.0.1:$GF_SERVER_HTTP_PORT` became `http://127.0.0.1:3300`). A literal `$` is written `$$`.

## Data sources
```yaml
apiVersion: 1
deleteDatasources:
  - {name: Old-Prometheus, orgId: 1}
datasources:
  - name: Prometheus
    uid: prometheus                 # fixed UID so dashboards reference it stably
    type: prometheus
    access: proxy
    url: http://prometheus-operated.monitoring:9090
    isDefault: true
    jsonData: {timeInterval: 30s, httpMethod: POST, exemplarTraceIdDestinations: [{name: trace_id, datasourceUid: tempo}]}
  - name: Mimir
    uid: mimir
    type: prometheus
    url: https://mimir.example.com/prometheus
    basicAuth: true
    basicAuthUser: grafana
    jsonData: {httpHeaderName1: X-Scope-OrgID}
    secureJsonData: {basicAuthPassword: $MIMIR_PASSWORD, httpHeaderValue1: tenant-a}
    editable: false
```
`secureJsonData` is never returned by the API (tested: the API returned `secureJsonFields: {basicAuthPassword: true, httpHeaderValue1: true}` and no values). Provisioned data sources are read-only unless `editable: true` (every data source here showed `readOnly: true`, and an API update failed with `Cannot update read-only data source`).

## Dashboards
```yaml
apiVersion: 1
providers:
  - name: default
    folder: ''                       # leave unset with foldersFromFilesStructure (the docs say to unset `folder` and `folderUid`)
    type: file
    disableDeletion: true
    allowUiUpdates: false            # UI edits can't be saved; changes go through git
    updateIntervalSeconds: 30
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true    # subdirectory name = folder
```
Kubernetes: the Helm chart's sidecar collects ConfigMaps labelled `grafana_dashboard: "1"` into that path
(`grafana_folder` annotation sets the folder) (gated: unconfirmed, source is paywalled or blocked): no Kubernetes or Helm run.

## Alerting
`provisioning/alerting/*.yaml` with `apiVersion: 1` and sections `groups` (rules, with `folder`, `interval`,
`rules[].data` queries), `contactPoints`, `policies`, `templates`, `muteTimes`, plus `deleteRules` etc.
Export existing rules as YAML with `GET /api/v1/provisioning/alert-rules/export` (tested; the UI **Export** button is not driven here (gated: unconfirmed, source is paywalled or blocked)) and commit them. Provisioned resources are locked: an API update of a file-provisioned rule returned 409 `cannot update with provided provenance 'api', needs 'file'`, a save of a provisioned dashboard returned `Cannot save provisioned dashboard`, and its delete returned `provisioned dashboard cannot be deleted`.

## Gotchas
- Changing a data source `uid` breaks every dashboard that references it.
- Provisioning runs at startup; dashboards are re-read every `updateIntervalSeconds` (a new JSON file appeared within about 40 s at 30). Other changes need a restart or an admin reload: `POST /api/admin/provisioning/datasources/reload`, `/dashboards/reload` and `/alerting/reload` all answered `... config reloaded` and applied new files.
- Two providers pointing at overlapping paths make the same dashboard UID appear twice; Grafana logged `the same UID is used more than once` and `dashboards provisioning provider has no database write permissions because of duplicates` for both providers.

## Verify
- [ ] A fresh Grafana start comes up with all data sources, dashboards and alert rules, no manual steps.
- [ ] Logs show no `provisioning` errors.

## Checked
Ran Grafana 13.2.4 (windows-amd64, own data, log and provisioning directories on localhost port 3300) with the page's provisioning files and read the results back through the HTTP API. Provisioned: data sources (Prometheus with `exemplarTraceIdDestinations`, Mimir with `basicAuth`, `httpHeaderName1` and `secureJsonData` using `$MIMIR_PASSWORD`, Tempo, Loki), `deleteDatasources`, a dashboard provider with `foldersFromFilesStructure` (two sub-directories became folders `team-a` and `team-b`), and an alerting file with `groups`, `contactPoints`, `policies`, `muteTimes`, `templates` and `deleteRules`. Confirmed through the API: `$$` handling, env expansion, `secureJsonFields`, read-only data sources, folder names, `allowUiUpdates: false` and `disableDeletion` behaviour, provenance `file` on templates and rules, the three reload endpoints, the rule export endpoint and the duplicate-UID warnings. Docs read: Grafana v13.2.4 docs source, administration/provisioning (env variables, `$$`, `updateIntervalSeconds`, `foldersFromFilesStructure`). The Helm sidecar and UI Export statements are gated as marked.
