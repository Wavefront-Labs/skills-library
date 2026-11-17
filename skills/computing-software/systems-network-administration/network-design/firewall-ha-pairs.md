---
id: computing-software.systems-network-administration.network-design.firewall-ha-pairs
name: firewall-ha-pairs
category: computing-software
field: systems-network-administration
product: network-design
tags: [firewall, firewall-ha, active-passive-firewall, state-sync, failover-testing, cluster, high-availability]
level: practitioner
status: docs-checked
description: "Design and operate firewall HA: active/passive vs active/active, state and session sync links, monitored interfaces and path monitoring, upgrades, and failover testing."
sources:
  - https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/high-availability
  - https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/62403/high-availability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall HA pairs

## Modes
| Mode | Behaviour | Use |
|---|---|---|
| Active/passive | one unit forwards, the peer mirrors config and sessions | default choice; simplest to reason about |
| Active/active | both forward (different VSYS/contexts or asymmetric with session ownership) | only when throughput demands; asymmetric flows add complexity |
| Clustering (vendor specific) | N units as one | scale-out DCs |

## Links
- HA control/heartbeat: dedicated ports, ideally two on separate paths.
- State/session sync: carries session tables so established flows survive failover. Size it
  for the session setup rate; a congested sync link loses sessions on failover.
- Connect back to back where possible; through switches, isolate in its own VLAN and avoid STP
  delays (PortFast).

## What triggers failover
- Unit failure (heartbeats lost).
- Link monitoring: if a monitored interface goes down. Monitor only interfaces that matter
  (outside, inside), not spare ports.
- Path monitoring: ping an upstream gateway; catches a dead next hop with the link up.
- Preemption: usually off for firewalls (avoid a second outage when the primary returns); fail back
  manually in a window.

## Addressing
Both units share virtual IPs/MACs on data interfaces (switches see a MAC move on failover; the new
active sends gratuitous ARPs). Give each unit its own management IP so you can reach the passive one.

## Upgrades
Upgrade passive -> fail over -> upgrade the former active -> (optionally) fail back. Check the vendor's
supported version skew between peers; sessions may not sync across major versions.

## Testing
- On a schedule: suspend the active unit or trigger a manual failover with the vendor's documented
  command, during a window with continuous pings and a long-running TCP session.
- Pass criteria: pings lose a few packets at most, established SSH/RDP sessions survive.

## Verify
- [ ] Both units show synchronised config and sessions; failover test result recorded with outage
  time.

## Checked

2026-10-28: Confirmed: the Palo Alto HA overview names active/passive and active/active HA, and the FortiGate HA page documents FGCP. The Cisco FTD HA page is a 404. Removed: PAN-OS, FortiGate and ASA failover commands, the HA1/HA2 port names, the spanned EtherChannel and FGSP clustering names and the quarterly test interval; the remaining text is design guidance.
Method: documentation only; no commands were run.
