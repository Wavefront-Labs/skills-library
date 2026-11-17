---
id: computing-software.cloud-infrastructure-engineering.graylog.health-module-and-notifications
name: health-module-and-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [health-module, system-notifications, cluster-health, troubleshooting, health-checks]
level: practitioner
status: docs-checked
description: "Use System > Overview Health and Notifications tabs to find cluster problems: health tree, subsystems and urgent versus info alerts."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/health_module.htm
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/system_notifications.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# health module and notifications

**Health Module** at **System > Overview > Health** (administrators). A tree: Cluster Health at top summarizes three branches, one per major component (Server, Search Cluster and MongoDB). The Server branch has six subsystems: Node, Input, Processing, Output, Archiving and Data Lake. Each exposes checks such as Input Failures, Report Generation or Shard Count.

**Notifications** at **System > Overview > Notifications**; the tab label and bell icon show the active count. Each row has Title, Severity (Urgent needs immediate action; Info is worth reviewing), Triggered time, Node ID and Type. Graylog raises one per affected node and clears it when the issue resolves or when you dismiss it. Dismissing does not fix the problem and it may return.

If several notifications share a node ID, check that node first. Notifications complement the Health Module, which shows current status.

## Checked

2026-11-04. Confirmed against the Health page. Fixed: the three branches are Server, Search Cluster and MongoDB, and the six Server subsystems are Node, Input, Processing, Output, Archiving and Data Lake.

Method: documentation only; no commands were run.
