---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ha-failover-monitoring-and-troubleshooting
name: fortigate-ha-failover-monitoring-and-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ha-monitor, fortios, ha-failover, ha-history, link-failure, ha-sync, cluster-checksum]
level: practitioner
status: draft
description: "Monitor and troubleshoot FortiGate HA failovers using port monitoring, history logs, checksum comparison and event logs."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: understand why a failover happened and keep the cluster healthy.

```
get system ha status
diagnose sys ha history read
diagnose sys ha checksum show
diagnose sys ha checksum cluster
diagnose debug application hasync -1
diagnose debug enable
```
`diagnose sys ha history read` records the reason of each failover (monitored port failure, heartbeat loss, priority change, manual failover). Force a test: `execute ha failover set 1` then `execute ha failover unset 1` (confirm syntax).

Tune
- `monitor` should list data interfaces whose failure triggers failover.
- `pingserver-monitor-interface` plus `pingserver-failover-threshold` triggers failover when a remote IP stops answering.
- `ha-uptime-diff-margin` and `override` control preemption.
- Enable `session-pickup-connectionless` for UDP/ICMP.

Gotchas
- Out-of-sync checksums mean configuration drifted; fix with `execute ha synchronize start` after checking config on both.
- Split-brain (both active) when heartbeats fail but data links are alive; use at least two heartbeat interfaces on separate paths.
- Debug commands are chatty; always disable debugging after use.

## Verify
```
diagnose sys ha status
diagnose sys ha checksum cluster
```
Checksums equal for all VDOMs; `get system ha status` shows one primary and the secondary healthy.
