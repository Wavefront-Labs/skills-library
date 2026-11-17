---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-session-table-management
name: pan-os-session-table-management
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [session-table, pan-os, show-session, clear-session, session-timeouts, offload, tcp-reject]
level: practitioner
status: draft
description: "Inspect, filter and clear PAN-OS sessions and understand state, timeouts and discard sessions safely."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/use-the-cli-to-view-sessions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: see exactly how a flow is handled and clear stale sessions without disruption.

```
show session info
show session all filter source 10.1.1.5 destination 198.51.100.7
show session all filter application ssl state active
show session id 12345
clear session id 12345
clear session all filter source 10.1.1.5
show session all filter state discard
```
`show session id` shows rule, NAT, ingress and egress interface, application, state and timeout, whether the session is decrypted and offloaded.

Timeouts: defaults per protocol (TCP 3600s, UDP 30s, ICMP 6s, TCP handshake 10s, confirm) under Device > Setup > Session; app-specific timeouts override defaults. Changes affect only new sessions.

Why clear sessions: after a policy or NAT change, existing sessions keep the old decision. Clearing the specific session forces a re-evaluation.

Gotchas
- `clear session all` without a filter drops every connection (including your management traffic if it passes the firewall).
- A session in `discard` state means policy or a threat verdict denied it; do not clear it as a fix, find the cause.
- Session table full: check `show session info` against the max sessions for the model and review DoS protection.

## Verify
```
show session id <ID>
```
After clearing and reconnecting, the new session shows the updated rule, NAT and egress interface.
