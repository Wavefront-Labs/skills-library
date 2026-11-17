---
id: computing-software.networking-hardware-and-wireless.kea.control-commands-service-and-status
name: control-commands-service-and-status
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, control-channel, dhcp-disable, status-get, maintenance]
level: practitioner
status: docs-checked
description: "Use dhcp-disable and dhcp-enable for maintenance and status-get to read pid, uptime, reload age, HA state and threading from a running Kea server."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service control and status commands
`dhcp-disable` globally disables DHCP service. The server keeps running but drops all received DHCP messages. Use it when maintenance needs the server to stop allocating new leases and renewing existing ones, or in failover-style setups during lease database synchronization or recovery. Optional `max-period` is the number of seconds after which service re-enables automatically if `dhcp-enable` has not been sent. Since Kea 1.9.4 an `origin` parameter names the command source; administrators should typically omit it (default "user"). Kea 2.5.8 added `origin-id` (1 means a user command; 2000 and up are HA partner services) and it takes precedence if both are given. `dhcp-enable` turns service back on and takes the same origin parameters.

`status-get` returns runtime information:
- `pid` and `uptime` (seconds since start);
- `reload`: seconds since the last configuration (re)load;
- `high-availability`: for HA servers, the `local` state, role (primary, secondary and so on) and scopes, and the `remote` server's last known state, scopes and role;
- `multi-threading-enabled`, `thread-pool-size` (DHCP service threads), `packet-queue-size` (maximum queue size, one queue for all threads) and `packet-queue-statistics` (average queue size for the last 10, 100 and 1000 packets). The thread and queue values are returned only for DHCP servers with multi-threading enabled; `high-availability` only for servers in an HA setup. None of these is returned by the DDNS daemon.

Other commands in the same list include `list-commands`, `version-get`, `shutdown`, `leases-reclaim`, `interface-add`, `interface-list`, `interface-redetect`, `server-tag-get`, `config-backend-pull` and `kea-lfc-start`.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM control channel chapter (sections 18.4.7-18.4.20: dhcp-disable, dhcp-enable, status-get and the listed command names). Removed the unsupported remark about D2's command set. Added origin-id and the packet-queue-statistics field from the same sections.
