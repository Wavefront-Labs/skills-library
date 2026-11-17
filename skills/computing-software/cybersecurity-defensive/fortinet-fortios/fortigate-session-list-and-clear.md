---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-session-list-and-clear
name: fortigate-session-list-and-clear
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [session-list, fortios, diagnose-sys-session, session-filter, session-clear, session-ttl, npu-offload]
level: practitioner
status: draft
description: "Inspect FortiGate sessions with filters, read flags and NAT fields, and clear specific sessions."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: confirm how a flow is processed and clear stale ones.

```
diagnose sys session filter clear
diagnose sys session filter src 10.1.0.5
diagnose sys session filter dport 443
diagnose sys session list
get system session-info statistics
diagnose sys session stat
diagnose sys session filter clear
```
Reading one entry
- `proto=6 proto_state=01` TCP established.
- `duration`/`expire` time to live.
- `policy_id`, `vd`, `dev=` ingress and egress interface indexes.
- `hook=pre dir=org act=dnat` and `hook=post dir=reply act=snat` show NAT.
- `no_ofld_reason` or `npu info` show whether the session is offloaded to the NPU.

Clear matching sessions only with the filter in place:
```
diagnose sys session filter src 10.1.0.5
diagnose sys session clear
```
Gotchas
- `diagnose sys session clear` with no filter clears every session and interrupts users; always confirm the filter with `diagnose sys session filter` first.
- Policy changes do not affect existing sessions unless `set firewall-session-dirty check-new` (global per-VDOM setting) applies.
- Session count limits per model; watch `get system performance status`.

## Verify
Re-run the list after clearing and the new session shows the updated policy id and NAT.
