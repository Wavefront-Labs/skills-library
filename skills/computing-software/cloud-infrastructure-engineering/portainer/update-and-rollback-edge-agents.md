---
id: computing-software.cloud-infrastructure-engineering.portainer.update-and-rollback-edge-agents
name: update-and-rollback-edge-agents
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [edge-agent, update, rollback, schedule, edge-groups]
level: advanced
status: docs-checked
description: "Schedule Edge Agent upgrades and rollbacks from the Portainer UI, with the beta, Business Edition and Docker Standalone limits."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/update.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Update and Rollback upgrades Edge Agent deployments from Portainer without logging into each remote environment. It is Business Edition only, currently in beta, and only supports Edge Agents on Docker Standalone.

Find it under Environment-related, Update & Rollback. The list shows pending and completed updates and rollbacks with schedule time, the Edge groups included, creation date, and status indicators counting environments in each state. Click a schedule name for details, and expand an individual environment to see its status within the schedule. Edit or remove schedules with the row icons.

To schedule, click Schedule update or rollback and fill in the form. Portainer must hold a snapshot of every environment you want to upgrade, so make sure snapshots exist first. The form takes a Name, the Edge Groups containing the devices (configured under Edge Groups), and the Version chosen on the Update tab; a rollback is scheduled from its own tab. The form also takes a schedule date and time (unavailable when upgrading from a version before 2.17, where the upgrade runs immediately) and optional Registry, Agent Image and Updater Image fields, useful in air-gapped environments.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the generic staged-rollout tip; added the remaining form fields.

Method: documentation only; no commands were run.
