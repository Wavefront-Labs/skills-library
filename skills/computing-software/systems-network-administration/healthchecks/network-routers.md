---
id: computing-software.systems-network-administration.healthchecks.network-routers
name: network-routers
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, dd-wrt, mikrotik, router-heartbeat, wan-outage]
level: practitioner
status: docs-checked
description: "Detect WAN outages by having a DD-WRT or MikroTik RouterOS router send a scheduled ping to Healthchecks every minute."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/network_routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If the router loses its WAN connection, the scheduled requests stop and Healthchecks notifies you.

DD-WRT: enable the cron daemon and edit the crontab under Administration, Management, Cron. Format is `[cron expression] [username] [command]`. Every minute:

```
* * * * * root wget <ping-url>
```

MikroTik RouterOS:
1. System, Scripts, Add New. Name `ping` (any name). Policy `read`, `test`. Source:

```
/tool fetch url="<ping-url>" output=none
```

2. System, Scheduler, Add New. Interval `00:01:00`, policy `read`, `test`, On Event `ping`.

Notes:
- `output=none` discards the response body. Without it the body is saved to a file, which needs the `write` policy.
- `tool fetch` supports HTTPS but does not verify certificates by default. `check-certificate=yes` enforces validation, but RouterOS ships without root CA certificates, so load them yourself.

## Checked

2026-11-04: confirmed against the Network Routers page (DD-WRT cron path and crontab syntax, RouterOS script and scheduler parameters, output=none, TLS certificate notes). Removed an unsourced period and grace recommendation.
Method: documentation only; no commands were run.
