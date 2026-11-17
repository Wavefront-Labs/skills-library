---
id: computing-software.networking-hardware-and-wireless.kea.ha-modes-and-peer-configuration
name: ha-modes-and-peer-configuration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, high-availability, libdhcp-ha, load-balancing, hot-standby, passive-backup]
level: advanced
status: docs-checked
description: "Choose a Kea high availability mode (load-balancing, hot-standby, passive-backup) and set this-server-name, peers, heartbeat and failure-detection parameters."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea HA modes and peer configuration
The `libdhcp_ha.so` hook is Kea's own HA design (not the failover protocol), with the same features for DHCPv4 and DHCPv6. It is configured under `high-availability` in the library parameters, and the docs load `libdhcp_lease_cmds.so` alongside it.

Modes:
- `load-balancing`: both servers answer (about half each, RFC 3074) and send each other lease updates. Pools must be split between them with client classification so they never allocate the same address.
- `hot-standby`: only the primary answers; the standby receives updates and takes over when it considers the primary offline. No pool split needed.
- `passive-backup`: one active server plus backups.
- Optional `backup` role servers get lease updates but are not waited for before replying.

Key parameters: `this-server-name` (must match a peers entry), `mode`, `peers` (each with `name`, `url`, `role`, `auto-failover`, optional `basic-auth-user`/`basic-auth-password`), `heartbeat-delay` (default 10000 ms), `max-response-delay` (default 60000 ms), `max-ack-delay` (default 10000), `max-unacked-clients` (default 10; 0 disables failure detection), `max-rejected-lease-updates` (default 10), `delayed-updates-limit` (0 never enters communication-recovery), `wait-backup-ack` for passive-backup.

The same configuration goes on every peer except for `this-server-name`.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (Hook Libraries chapter, libdhcp_ha.so). Removed: the claim that each server uses the partner's pool fragments only when the partner is down.
Method: documentation only; no commands were run.
