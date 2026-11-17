---
id: computing-software.cloud-infrastructure-engineering.google-cloud.backup-appliance-and-management-console
name: backup-appliance-and-management-console
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, backup-and-dr, backup-appliance, management-console, deprecation]
level: advanced
status: docs-checked
description: "Decide whether the Backup and DR management console and backup/recovery appliance are needed, and plan an appliance deployment; note the legacy console deprecation."
sources: ["https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr", "https://cloud.google.com/backup-disaster-recovery/docs/deployment/deployment-plan", "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-plan-policy-template"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup appliance and management console

**Check first:** the deployment plan page carries a caution that support for backing up and restoring workloads
managed with the **legacy appliance management console is deprecated** (see the "Feature deprecations" page).
Backup and DR can back up Cloud SQL instances, AlloyDB clusters, and Compute Engine instances and disks directly
from the Google Cloud console; if all your workloads fit those categories you do not need a backup/recovery appliance.

## Components (from the deployment plan page)
- **Appliance management console**: the management plane. Each deployment has a single console managing any
  number of appliances; it lives in the backup administration project, is highly available within its region,
  and is activated into a service producer VPC network that communicates with your project using Private Google Access.
- **Backup/recovery appliance**: the data mover that captures, moves and manages the lifecycle of backup data,
  deployed in the Workload entity for cloud workloads. With several appliances, each needs a unique service account.
- Console-to-appliance, appliance-to-appliance and appliance-to-host-agent traffic uses mutual TLS.

## Rules
- Do not change an appliance's machine type or CPU/memory without consulting Support, and do not rename it
  after deployment (renaming is unsupported and can make it unusable).
- For ports, firewall rules, agent installation, templates and profiles, follow the current Backup and DR docs for
  your version; this skill no longer lists them because they could not be confirmed.

## Verify
- [ ] The workloads genuinely need an appliance (not just Cloud SQL, AlloyDB, VMs or disks).
- [ ] The deprecation notice was read and a migration path planned.
- [ ] A restore or mount test succeeds for each critical workload.

## Checked
2026-10-28. Confirmed on the deployment plan page: legacy console deprecation caution, supported direct backup
sources, console and appliance components, unique service account per appliance, mTLS, do-not-resize/rename warnings.
Removed (not on the pages or unconfirmed): /23 range, TCP ports 5106 and 3260, appliance types, template retention
example values, OnVault bucket class advice, agent install steps (the cited install page 404s), agentless-model
description and version compatibility claim.
Method: documentation only; no commands were run.
