---
id: computing-software.cloud-infrastructure-engineering.netdata.optimize-agent-performance
name: optimize-agent-performance
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, resource-usage, ram-mode, ml-disable]
level: practitioner
status: docs-checked
description: "Reduce Netdata Agent CPU, RAM and disk use: Parent-Child layout, disabling unused collectors, slower collection, shorter retention, RAM mode and ML placement."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/optimize-the-netdata-agents-performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Levers, in the order the docs suggest:
1. Decide whether you have a resource constraint or an architecture problem.
2. Monitoring many systems? Set up Parent-Child first: Children stream to a Parent that does aggregation, storage and dashboard queries.
3. Tune each Agent by role.

Tuning options:
- Disable collectors you do not need. Only running collectors cost resources, so disabling inactive ones saves nothing.
- Collect less often if you do not need per-second precision or CPU is high while dashboards are idle.
- Shorten metric retention to cut RAM and disk.
- Put Children and IoT devices in RAM mode to remove disk I/O for metric storage.
- Enable ML on Parents, disable it on Children:

```
[ml]
   enabled = no
```

Edit with `sudo ./edit-config netdata.conf`. Afterwards use the dashboards to confirm monitoring visibility has not dropped.

Gotcha: the page names no specific values for collection frequency or retention; consult the collector and database configuration docs for the exact settings.

## Checked

2026-11-04: default features, the strategies and their order, the inactive-collector warning, collection interval, retention, RAM mode, ML placement and the `[ml]` example confirmed against the Netdata Agent Performance Optimization Guide. Removed an unsourced restart instruction.

Method: documentation only; no commands were run.
