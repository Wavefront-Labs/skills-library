---
id: computing-software.cloud-infrastructure-engineering.netdata.dynamic-configuration-manager
name: dynamic-configuration-manager
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, dynamic-configuration, collector-jobs, dyncfg]
level: practitioner
status: docs-checked
description: "Configure collectors and alerts from Netdata Cloud without editing files: plan limits, modules versus jobs, job actions and discovered-job secret handling."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/dynamic-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: nodes connected to Netdata Cloud. Creating, editing, testing, enabling, disabling or removing needs a paid plan; Community plans can only list.

Where: bell icon on a chart, Alerts tab, Integrations (Configure button, go.d collectors only), Space Settings, Configurations.

Concepts:
- A module is a collector template; a job is a configured instance.
- Disabling a module stops its jobs and blocks new ones.
- Job sources: Stock, User, Discovered, Dynamic Configuration.
- Job actions: Edit, Test (before applying), Enable/Disable, Restart (failed jobs), Remove (only Dynamic Configuration jobs).

Changes take effect on the node immediately. Each alert change is stored as a dynamic configuration that overrides stock definitions; stock files are untouched. One submission can target multiple nodes.

Secrets gotcha: saving an edited discovered job adopts it as a dynamic configuration, enabling `${env:...}`, `${file:...}`, `${cmd:...}`, `${store:...}` across the whole submission, including fields you did not edit. Review everything. Enabling or restarting a discovered job does not adopt it. Discovered jobs treat secret references literally unless the pipeline sets `trust_discovered_targets`; enable only if every target is trusted.

## Checked

2026-11-04: plan requirement, access methods, module and job concepts, job actions, immediate application with stock files untouched, multi-node submission and the discovered-job secret handling confirmed against the Netdata Dynamic Configuration Manager page.

Method: documentation only; no commands were run.
