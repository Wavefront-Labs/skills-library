---
id: computing-software.systems-network-administration.cisco-networking.extended-ping-and-traceroute
name: extended-ping-and-traceroute
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, extended-ping, extended-traceroute, df-bit, ping-sweep, source-interface, troubleshooting]
level: practitioner
status: draft
description: "Use IOS extended ping and traceroute: source interface, DF bit with size sweeps for MTU, repeat counts, VRFs, and reading the result characters."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13730-ext-ping-trace.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extended ping and traceroute on IOS

Plain `ping x` sources from the egress interface. That proves little about whether a LAN
behind the router is reachable. Extended options fix that.

## One-line forms
```
ping 10.2.0.10 source Vlan10 repeat 100 size 1500 df-bit
ping vrf CUSTOMER-A 10.2.0.10 source Loopback10
ping 10.2.0.10 timeout 1 repeat 1000          ! quick loss sampling
traceroute 10.2.0.10 source Vlan10 numeric probe 1 timeout 1 ttl 1 15
traceroute vrf CUSTOMER-A 10.2.0.10
```
## Interactive (just `ping` then Enter)
Prompts for protocol, target, repeat, size, timeout, extended commands (source, ToS, DF,
data pattern), and **sweep range of sizes**: sweep 1400-1520 step 4 with DF set finds the
exact path MTU in one run.

## Reading results
| Char | Meaning |
|---|---|
| `!` | reply |
| `.` | timeout |
| `U` | destination unreachable received |
| `M` | could not fragment (DF set, MTU too small) |
| `Q` | source quench |
| `&` | TTL exceeded |

Traceroute: `*` = no reply at that hop (often just ICMP rate-limit or filtering), `!A`
administratively prohibited, `!H` host unreachable, `!N` network unreachable.

## Patterns
- Source from the LAN SVI to test the return route: success from the WAN IP but failure from
  the SVI = the far end has no route back to your LAN.
- ToS 184 (DSCP EF) tests QoS policies that match marking.
- `data 0x0000` / `0xffff` patterns expose bit-pattern sensitive links (old serial/T1 issues).
- Pings to the router itself are punted to CPU and may be policed by CoPP; loss there is not
  necessarily transit loss.

## Verify
- [ ] Test sourced from the correct interface/VRF; MTU sweep shows the max DF size that passes.
