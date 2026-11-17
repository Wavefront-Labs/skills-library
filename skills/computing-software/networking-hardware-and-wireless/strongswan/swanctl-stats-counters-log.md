---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-stats-counters-log
name: swanctl-stats-counters-log
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl, stats, counters, log, redirect, reload-settings]
level: practitioner
status: docs-checked
description: "Monitor charon with swanctl --stats, --counters and --log, redirect an IKE SA to another gateway with --redirect, and reload strongswan.conf with --reload-settings."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlStats.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlCounters.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlLog.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlRedirect.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl stats counters log
**Stats.** `swanctl --stats` shows uptime, worker threads (total and idle), job queues, scheduled jobs, IKE_SA totals and half-open count, memory info and the loaded plugins.

**Counters.** `swanctl --counters [--name <name>|--all] [--reset]` lists IKE message counters such as `ike-rekey-init`, `child-rekey`, `invalid`, `invalid-spi`, and in/out request and response counts for ike-init, ike-auth, create-child and info. It requires the counters plugin. Omit `--name` for global counters; `--all` covers all tracked connections; `--reset` (`-R`) resets.

**Log.** `swanctl --log` traces charon logging via vici, but only receives levels 0 and 1; use other logging backends for more.

**Redirect.** `swanctl --redirect` moves an IKE SA to another gateway. Select with `--ike`, `--ike-id`, `--peer-ip <ip|subnet|range>` or `--peer-id <id|wildcards>`, and give `--gateway <ip|fqdn>`:

```
swanctl --redirect --peer-ip 192.168.0.100 --gateway 192.168.0.1
```

**Reload settings.** `swanctl --reload-settings` (`-r`) reloads the strongswan.conf configuration.

## Checked
2026-11-04. Confirmed against the swanctl --stats, --counters, --log, --redirect and swanctl tool pages: output fields, counters options and plugin requirement, the level 0 and 1 limit of --log, redirect selectors and the example.

Method: documentation only; no commands were run.
