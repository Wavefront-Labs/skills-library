---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-policy-routes
name: fortigate-policy-routes
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [policy-route, fortios, pbr, router-policy, policy-based-routing, source-routing]
level: practitioner
status: draft
description: "Steer selected FortiGate traffic with policy routes by source, destination, protocol and interface, and know their precedence."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: send certain traffic via a specific gateway irrespective of the routing table.

```
config router policy
    edit 1
        set input-device "port2"
        set src "10.30.0.0/255.255.255.0"
        set dst "0.0.0.0/0.0.0.0"
        set protocol 6
        set start-port 443
        set end-port 443
        set gateway 198.51.100.1
        set output-device "port3"
    next
end
```
Precedence: policy routes are evaluated before the routing table (after the session lookup), and a matching policy route with a reachable gateway wins. `set action deny` or `set action stop-policy-route` can exempt traffic.

Notes
- Prefer SD-WAN rules for modern deployments; policy routes lack health checks.
- The gateway must be reachable on the output device; if the interface goes down, the policy route is ignored and the routing table is used.

Gotchas
- A policy route with the wrong input device never matches; traffic from IPsec or VLAN interfaces needs its own device name.
- Policy routes apply to forwarded traffic and, by default, not to local-out; use `set local-out-ioc` style settings (confirm) for local traffic.
- Order matters: first match wins.

## Verify
```
diagnose firewall proute list
diagnose debug flow filter addr 10.30.0.10
```
`diagnose firewall proute list` shows the rule and hit counts; debug flow reports "Match policy routing id".
