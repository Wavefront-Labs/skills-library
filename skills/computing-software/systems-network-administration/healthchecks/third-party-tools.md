---
id: computing-software.systems-network-administration.healthchecks.third-party-tools
name: third-party-tools
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, terraform-provider, ansible-collection, backup-integrations, dashboards-community]
level: practitioner
status: docs-checked
description: "Community tools around Healthchecks: Terraform and Ansible, API wrappers, restic and Borg backup integrations, alternative Docker images and status dashboards."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Healthchecks resources page lists third-party software projects that integrate with Healthchecks.

Command runners and wrappers: runitor, crontask.sh, task-mon (Rust), hc-monitor (Bash gist), pytocron.

Self-hosting: linuxserver/docker-healthchecks and galexrt/docker-healthchecks (alternative Docker images); Elestio is a managed platform using the linuxserver image.

API wrappers:
- Ansible: community.healthchecksio modules.
- Terraform: terraform-provider-healthchecksio, to create, update and delete checks.
- Go: go-healthchecksio, etke.cc healthchecks.
- PowerShell: HealthChecksIOStatusReport, healthchecks-pwsh.
- Python: healthchecks_wrapper, healthchecks-decorator, py-healthchecks.io.
- Rust: healthchecks-rs (Ping and Management APIs).

Backup tools with integration: backrest (restic web UI), restic-tools, borgmatic and emborg (Borg frontends).

Dashboards: healthchecks/dashboard (standalone HTML page), healthchecks-front, and KumaBar (macOS menu bar app, also supports Uptime Kuma).

## Checked

2026-11-04. Confirmed against the Healthchecks Third-Party Resources page: every project named, its category and the features noted for the Terraform provider, Rust and Go wrappers, Elestio and the dashboards. Removed the vetting remark and the closing advice about managing checks as code, which the page does not state.

Method: documentation only; no commands were run.
