---
id: computing-software.networking-hardware-and-wireless.juniper-junos.traceoptions
name: traceoptions
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, traceoptions, debug-logging, trace-file, flag]
level: practitioner
status: draft
description: "Enable and safely scope Junos traceoptions on protocols to diagnose issues, then remove them."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Traceoptions for protocol troubleshooting
Goal: see protocol events in a log file.

```
set protocols bgp traceoptions file bgp-trace size 5m files 3
set protocols bgp traceoptions flag open detail
set protocols bgp traceoptions flag update detail
set protocols bgp traceoptions flag keepalive
commit
```

```
user@host> show log bgp-trace | last 50
user@host> monitor start bgp-trace
user@host> monitor stop
```

```
delete protocols bgp traceoptions
commit
```

- Traces go to `/var/log/<file>`; size and file count bound disk use.
- Use `match "regex"` to filter by peer or prefix.
- `flag all` is expensive.

Gotcha: leaving verbose traceoptions enabled on a production BGP speaker loads the CPU and fills `/var`. Always add size limits and delete after.

Operational tip: use per-neighbor filtering with `match` and the `detail` flag only for the specific message type you need, and note the time you enabled and removed tracing in the change record.

## Verify
- `show log bgp-trace` shows entries after `clear bgp neighbor`; after cleanup `show configuration protocols bgp | display set | match trace` is empty.
