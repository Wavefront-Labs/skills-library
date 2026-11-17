---
id: computing-software.cloud-infrastructure-engineering.netdata.disable-or-silence-alerts
name: disable-or-silence-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, enabled-alarms, to-silent, health-disable]
level: practitioner
status: docs-checked
description: "Disable all or specific Netdata alerts with enabled alarms patterns, silence notifications with to: silent, and avoid the pattern-order and reload traps."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/REFERENCE.md
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/overriding-stock-alerts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Methods:

| Goal | Method | Apply |
|---|---|---|
| All health checks off | `[health] enabled = no` | restart |
| Specific alerts off | `enabled alarms = !oom_kill *` | restart |
| Only listed alerts | `enabled alarms = oom_kill disk_space_usage` | restart |
| Silence notifications | `to: silent` in the alert file | reload-health |
| One alert off | comment it out in its file | reload-health |

```
[health]
    enabled alarms = !oom_kill !disk_space_usage *
```

Another per-alert option: an override containing `host labels: _hostname=!*`. A `to: silent` alert still shows on the dashboard without notifying.

Gotchas:
- Put all `!` exclusions first and one trailing `*`; patterns evaluate in order and the first match wins.
- A whitelist without a trailing `*` leaves alerts added by future upgrades disabled.
- `sudo netdatacli reload-health` does not reload `netdata.conf`; `[health]` changes need an Agent restart.
- Runtime, temporary control is available through the health management API with no config change.

## Checked

2026-11-04: the enabled and enabled alarms settings, pattern order, whitelist behaviour, `to: silent`, `host labels: _hostname=!*`, restart versus reload-health and the runtime health API note confirmed against the Netdata health REFERENCE and overriding-stock-alerts pages. Removed an unsourced verify step.

Method: documentation only; no commands were run.
