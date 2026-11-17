---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-as-code-tooling
name: grafana-as-code-tooling
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, dashboards-as-code, grafana-terraform-provider, grafana-terraform-dashboards, terraform-grafana-folder, git-sync, grafana-git-sync, dashboard-api, dashboards-http-api]
level: practitioner
status: docs-checked
description: "Choose Grafana as-code tooling (Git Sync, file provisioning, Terraform, Ansible, Grafana Operator, Foundation SDK) and the Grafana 12 dashboard API."
sources: ["https://grafana.com/docs/grafana/latest/observability-as-code/", "https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana as code tooling

## Options (Grafana docs overview)
| Tool | What it does |
|---|---|
| Git Sync | Store dashboard files in a GitHub repository and synchronise them with Grafana (version control, branching, pull requests from Grafana) |
| On-prem file provisioning | Folders and dashboard JSON files stored on a local file system |
| Terraform | The Grafana Terraform provider manages dashboards, alerts and more |
| Ansible | The Grafana Ansible collection manages Grafana Cloud resources, including folders and cloud stacks |
| Grafana Operator | Kubernetes operator managing Grafana instances, dashboards, folders and data sources through Custom Resources |
| Foundation SDK | Define dashboards and resources in Go, TypeScript, Python, Java or PHP |

Most of these can be used with one another. Grafana 12 introduced versioned APIs and official tooling; Git Sync and
the Foundation SDK are built on them. For basic configuration provisioning see the Grafana "Provision Grafana" docs.

## Tools to avoid
- Grizzly (`grr`): the docs state it "has been removed, and is no longer deployed, enhanced, or supported"; use the
  Grafana CLI instead.
- Grafonnet (Jsonnet library): "not officially supported by Grafana"; the docs point to the Foundation SDK.

## Dashboard API
In Grafana 12 and later the Dashboard API (`/apis/dashboard.grafana.app/*`) replaces `/api/dashboards/*`, though not
every legacy endpoint has an exact match. Endpoints (v1, `:namespace` per the API overview, for example `default`):
- POST `/apis/dashboard.grafana.app/v1/namespaces/:namespace/dashboards` create
- PUT `.../dashboards/:uid` update; GET `.../dashboards/:uid` get; GET `.../dashboards` list; DELETE `.../dashboards/:uid`
- Authenticate with `Authorization: Bearer <SERVICE_ACCOUNT_TOKEN>`.
- Folder is the `grafana.app/folder` annotation under `metadata.annotations`; the dashboard model sits under `spec`;
  `grafana.app/message` is an optional commit message for the version history.
- Grafana Enterprise needs specific RBAC permissions for some endpoints (for example `dashboards:create`,
  `dashboards:write`).
The page warns it may not hold the latest version; check `dashboard.grafana.app/v2` in Swagger for current endpoints.

## Verify
- [ ] Each folder is managed by one mechanism only, so tools do not overwrite each other (your policy; the docs do not
  state a conflict rule).
- [ ] Dashboard JSON follows the JSON model documentation for the Grafana version in use.

## Checked
Checked 2026-11-08 against the Grafana "Deploy, provision and manage Grafana with as code workflows" page and the
Dashboard API page. Removed: the Terraform HCL example and resource list (the Terraform registry page returned no
readable content), the Grizzly and grafanactl commands (Grizzly is removed per the docs; grafanactl is not mentioned),
the Git Sync version and "experimental" claim, the legacy `curl` examples and the 412 and `overwrite` behaviour (the
current page documents the new API instead).
Method: documentation only; no commands were run.
