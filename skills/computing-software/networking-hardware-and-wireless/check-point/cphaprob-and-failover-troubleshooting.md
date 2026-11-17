---
id: computing-software.networking-hardware-and-wireless.check-point.cphaprob-and-failover-troubleshooting
name: cphaprob-and-failover-troubleshooting
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cphaprob, failover, critical-devices]
level: practitioner
status: draft
description: "Read cphaprob state, list critical devices (pnotes) and find why a Check Point cluster member goes Down or Active Attention."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ClusterXL_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cphaprob and ClusterXL failover troubleshooting

```
cphaprob stat
cphaprob list                       # pnotes (critical devices) and their state
cphaprob -ia list
cphaprob -l list
cphaprob -a if
cphaprob syncstat
cphaprob show_failover              # failover history (confirm)
grep -i "state change" /var/log/messages
clusterXL_admin down                # manual failover test
```
- States: `Active`, `Standby`, `Ready`, `Down`, `Active Attention` (the member is active but a critical device is problematic), `Initializing`, `ClusterXL inactive`.
- **Critical devices** (pnotes) include `Interface Active Check`, `FIB`, `fwd`, `cphad`, `routed`, `Synchronization`, `Filter`, `Recovery Delay`, and custom ones (`cphaprob -d name -t 10 -s ok register`). A pnote in problem state causes failover.
- `cphaprob -a if` showing an interface `DOWN` means no CCP (Cluster Control Protocol) packets are seen; check switch ports, VLANs, and the CCP mode (broadcast vs. multicast) and MAC filters.
- `Synchronization` not OK means sync interface down or the peer unreachable; connections will not be synchronized so failover drops sessions.
- After a real failover, the cause is often `fwd` death, `routed` crash, or `Interface Active Check` from a link flap. Check `/var/log/messages` and `$FWDIR/log`.
- Gotcha: `cphaprob stat` showing both members `Active` indicates a sync/CCP break (split brain); fix the network before anything else.

Verify: after the fix, `cphaprob stat` shows one Active, one Standby and `cphaprob list` shows no problem pnotes; test with `clusterXL_admin down` then `up`.
