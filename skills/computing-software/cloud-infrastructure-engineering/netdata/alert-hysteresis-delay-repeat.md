---
id: computing-software.cloud-infrastructure-engineering.netdata.alert-hysteresis-delay-repeat
name: alert-hysteresis-delay-repeat
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, alert-flapping, delay-line, repeat-line]
level: advanced
status: docs-checked
description: "Stop Netdata alert flapping and tune notification timing with status-dependent thresholds, the delay line and repeat intervals."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/REFERENCE.md
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hysteresis (status-dependent thresholds):

```
    warn: $this > (($status >= $WARNING)  ? (60) : (75))
    crit: $this > (($status == $CRITICAL) ? (75) : (85))
```

The alert needs a higher value to raise than to clear.

`delay` controls notification hysteresis only; it does not change alert status:

```
delay: [[[up U] [down D] multiplier M] max X]
```

- `up U`: CLEAR to WARNING and WARNING to CRITICAL.
- `down D`: decreases.
- `multiplier M`: multiplies delays if state changes during a pending delay.
- `max X`: caps total delay.

`repeat` overrides the `netdata.conf` repeat defaults:

```
repeat: [off] [warning DURATION] [critical DURATION]
```

Use `0s` to disable repeating for one state.

Other anti-flapping tools: require a duration via a `lookup` window (for example `average -10m of used`).

Facts to remember:
- Alerts can jump straight from CLEAR to CRITICAL; CRITICAL wins if both conditions are true.
- Notifications use exponential backoff, while dashboards update immediately.
- Alerts cannot run faster than the collection interval.

Apply with `sudo netdatacli reload-health`.

## Checked

2026-11-04: the hysteresis expressions, `delay` syntax and parameter meanings, `repeat` syntax and `0s` behaviour, CLEAR to CRITICAL jumps, CRITICAL precedence, notification backoff and the collection-interval limit confirmed against the Netdata health REFERENCE and README pages. Changed the lookup window example to the page's `average -10m of used`.

Method: documentation only; no commands were run.
