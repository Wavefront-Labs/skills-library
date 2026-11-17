---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-debug-flow
name: fortigate-debug-flow
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [debug-flow, fortios, diagnose-debug-flow, packet-flow-trace, policy-denied, reverse-path-check, flow-filter]
level: practitioner
status: draft
description: "Trace FortiGate packet processing with debug flow to see route lookups, policy matches and drop reasons."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: find why a flow is dropped.

```
diagnose debug reset
diagnose debug flow filter clear
diagnose debug flow filter addr 10.1.0.5
diagnose debug flow filter port 443
diagnose debug flow show function-name enable
diagnose debug flow show iprope enable
diagnose debug flow trace start 50
diagnose debug enable
```
Generate the traffic, then stop:
```
diagnose debug disable
diagnose debug reset
```
Reading the output
- `find a route: flow ... gw-192.0.2.1 via port1` means the route lookup chose that egress.
- `Allowed by Policy-10: SNAT` shows policy and NAT.
- `denied by forward policy check (policy 0)` means the implicit deny (no policy matched).
- `reverse path check fail, drop` means RPF failed (asymmetric or missing route).
- `no session matched` for return packets suggests asymmetric routing or timeouts.

Gotchas
- Without filters, debug flow floods the console and can hang the CLI; always filter first and limit the packet count.
- Remember to disable debug; it persists for the session.
- Offloaded flows are not traced after offload.

## Verify
The output ends with an allow or a specific drop reason for the filtered host; after the fix, the same filter shows `Allowed by Policy`.
