---
id: computing-software.cloud-infrastructure-engineering.netdata.standalone-vs-cloud-deployment
name: standalone-vs-cloud-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, standalone-deployment, cloud-connected, claim-token]
level: intro
status: docs-checked
description: "Pick between Cloud-connected and standalone Netdata deployments: how to get the connection command, what Cloud does and does not centralize, and trade-offs."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/deployment-guides/standalone-deployment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cloud-connected (recommended):
1. Sign up for Netdata Cloud.
2. Get the connection command from Space Settings, Nodes, "+"; or the Nodes tab, Add nodes; or the Integrations page for your OS.
3. Run it. It detects your OS, installs the latest Agent, connects to your Space with the claim token and room info, and starts streaming charts.

Optional hardening: disable local Agent notifications (Cloud handles them) and restrict local dashboard access.

Standalone (no Cloud):
1. Install on each system (check Version and Platform docs first).
2. Open each dashboard at `http://agent-ip:19999`.
3. Configure alerts per Agent.

Gotchas:
- Cloud does not centralize alert configuration; each Agent still manages its alerts and Cloud handles notifications.
- Without Cloud you check multiple dashboards, configure alerts per system and get no mobile notifications.
- The page does not give the exact install or claim command; use the "Connect Agent to Cloud" guide.

## Checked

2026-11-04: the three ways to get the connection command, what the command does, optional optimizations, standalone steps and the Cloud trade-offs confirmed against the Netdata Single Agent Deployment page. Removed an unsourced verify line.

Method: documentation only; no commands were run.
