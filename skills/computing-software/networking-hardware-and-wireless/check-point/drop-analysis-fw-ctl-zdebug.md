---
id: computing-software.networking-hardware-and-wireless.check-point.drop-analysis-fw-ctl-zdebug
name: drop-analysis-fw-ctl-zdebug
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, fw-ctl-zdebug, drop-analysis, packet-drops]
level: practitioner
status: draft
description: "Find why a Check Point gateway drops traffic using fw ctl zdebug drop, fw log, and dropped-packet reasons."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
  - https://support.checkpoint.com/results/sk/sk98348
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drop analysis with fw ctl zdebug and fw log

```
fw ctl zdebug + drop | grep 10.1.10.55         # live; Ctrl-C to stop
fw ctl zdebug + drop > /var/tmp/drop.txt &     # cap size; kill after
fw ctl zdebug drop                              # (old syntax)
fw log -n -t -c drop | tail
fw ctl set int fw_log_drop_rate 1               # (confirm) log rate
```
- Typical drop reasons: `Rulebase drop - cleanup rule`, `fw_handle_first_packet: Cleanup rule`, `Anti Spoofing`, `Dropped by IPS`, `policy_clean_up`, `First packet isn't SYN` (asymmetric or post-failover without sync), `Out of state`, `Dropped by fwx_ClusterXL...`, `Failed to find a NAT port`.
- `zdebug drop` is lightweight, but any kernel debugging on a busy gateway burns CPU and may fill the output buffer; always filter with `grep` and never leave it running.
- Use `fw log -c drop` for logged drops, and the SmartConsole filter `action:Drop`. For not logged drops (e.g. anti-spoofing with logging off) kernel debug is the only way.
- "First packet isn't SYN": check routing symmetry and whether traffic passes through both cluster members with sync disabled; consider `fw ctl set int fw_allow_out_of_state...`, but only temporarily (confirm).
- Turn off with Ctrl-C, then `fw ctl debug 0` to be sure all flags are reset.

Verify: reproduce a drop and see the `;[vs_0];[cpu_x];[fw_x];` line with the reason; after fixing the rule/routing, the same test shows no `drop` line.
