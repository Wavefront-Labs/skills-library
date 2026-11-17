---
id: computing-software.cloud-infrastructure-engineering.graylog.cluster-configuration-page
name: cluster-configuration-page
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [cluster-configuration, load-balancer-status, pause-processing, thread-dump, node-health]
level: practitioner
status: docs-checked
description: "Use System > Cluster Configuration to view Graylog, Data and MongoDB nodes, mark a node DEAD for the load balancer and pause processing."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/cluster_configuration.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cluster configuration page

Open **System > Cluster Configuration**. Requires administrator or the Cluster Configuration Reader role. Separate tables show Graylog Nodes, Data Nodes and MongoDB Nodes; use Columns to choose metrics and the search field or toggles to filter.

Statuses, CPU, memory and storage show red (warning) or yellow (caution) banners when thresholds pass.

Graylog node Actions: view running inputs, thread dump, process-buffer dump, recent system logs.
Graylog node More menu:
- **Pause message processing**: process buffers stop accepting messages. With the message journal enabled (default) incoming messages still persist to disk, so nothing is lost.
- **Set load balancer status to DEAD**: the load balancer stops sending log messages to that node.

MongoDB table: Profiling Level defaults to Off; Enable Profiling gives more detail. Showing MongoDB node metrics needs matching MongoDB roles.

## Checked

2026-11-04. Confirmed against the Cluster Configuration page. Removed: "Use for maintenance", which the page does not state.

Method: documentation only; no commands were run.
