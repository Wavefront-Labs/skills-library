---
id: computing-software.cloud-infrastructure-engineering.netdata.centralize-alerts-on-parent
name: centralize-alerts-on-parent
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, central-alerts, duplicate-alerts, health-enabled]
level: advanced
status: docs-checked
description: "Run alerts for all Children on the Parent: disable health on Children, tune once on the Parent, and avoid duplicate alerts and httpcheck surprises."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On each Child, disable health in `netdata.conf`:

```
[health]
    enabled = no
```

Restart the Child. `netdatacli reload-health` reloads only `health.d/*.conf`, not `netdata.conf`.

Then tune, silence or disable alerts once on the Parent (see the override-stock-alerts skill).

Duplicates: if every Parent in a cluster runs health checks and sends alerts, you get duplicates. Netdata Cloud deduplicates notifications for Child alerts, so use it.

Local collectors (for example `httpcheck`) run only on the Parent where configured, not on streamed Child data:
- Configure on one Parent: if that Parent goes down, the check stops until it recovers.
- Configure on both: the check keeps running, and in an active-active cluster each Parent replicates its local metrics to the other.
- Each Parent alerts independently, and Cloud does not deduplicate these alerts.

Functions still work on Children when only Parents connect to Cloud: the Parent forwards requests over the streaming connection, across multiple Parent levels.

## Checked

2026-11-04: disabling health on Children, the restart versus reload-health note, tuning once on the Parent, duplicate notifications and Cloud deduplication, local collector behaviour and Functions forwarding confirmed against the Netdata Metrics Centralization Points FAQ. Removed an unsourced verify line and corrected a cross-reference to an existing skill.

Method: documentation only; no commands were run.
