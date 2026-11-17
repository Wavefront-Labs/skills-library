---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ip-pools-source-nat
name: fortigate-ip-pools-source-nat
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ip-pool, fortios, source-nat, overload-pool, fixed-port-range, port-block-allocation, one-to-one]
level: practitioner
status: draft
description: "Configure FortiGate IP pools for source NAT - overload, one-to-one, fixed port range and port block allocation - and apply in policy."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: predictable source addresses for outbound traffic.

```
config firewall ippool
    edit "pool-out"
        set type overload
        set startip 203.0.113.20
        set endip 203.0.113.23
    next
end
config firewall policy
    edit 10
        set nat enable
        set ippool enable
        set poolname "pool-out"
    next
end
```
Types
- overload: many clients per address, ports translated (default behaviour with interface address).
- one-to-one: each internal IP to a dedicated external IP.
- fixed-port-range: deterministic internal-to-external port mapping for logging compliance.
- port-block-allocation (PBA): blocks of ports per client, with logging per block.

Interface-address NAT (`set nat enable` with no pool) uses the egress interface IP.

Gotchas
- A pool address must be routed to the FortiGate by the upstream; add ARP replies via `set arp-reply enable` (default) when the pool is on the same subnet as the interface.
- One-to-one pools exhaust fast; the policy then drops new sessions.
- Fixed port range depends on knowing the internal IP range; keep documentation current.

## Verify
```
diagnose firewall ippool-all list
diagnose firewall ippool-all stats
diagnose sys session list
```
The session shows `hook=post dir=org act=snat` with the pool address.
