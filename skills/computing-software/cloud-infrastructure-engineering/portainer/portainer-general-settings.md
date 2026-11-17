---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-general-settings
name: portainer-general-settings
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [settings, snapshot-interval, app-templates, backup, s3]
level: practitioner
status: docs-checked
description: "Tour Portainer general settings: snapshot interval, edge poll frequency, app templates, HTTPS enforcement, S3 backups and the support bundle."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/general.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Under Settings you will find:

- Snapshot interval: how often an environment snapshot is taken (the data shown on the home page plus basic information). Default is every 5 minutes.
- Edge agent default poll frequency: default check-in interval for Edge Agents.
- Custom logo (recommended 155px by 55px) and a Login screen banner (Business Edition).
- App Templates: supply the URL to your own JSON template definitions instead of the built-in set.
- Automatic Portainer patch updates (beta, Business Edition, admin only): suited to standalone instances where immediate patching beats manual maintenance. It deviates from version-controlled deployments, so avoid it with a strict GitOps or IaC workflow where the running version could drift from your manifests.
- Kubernetes settings: Helm repository, kubeconfig, KubeShell and deployment options, plus a CA file for Helm repositories.
- SSL certificate, and Force HTTPS only.
- Hidden containers, SSRF protection, experimental features.
- Back up Portainer to local disk or S3 (with scheduled backups), and restore from a local file or S3.
- Support: a support bundle and a debug log toggle.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
