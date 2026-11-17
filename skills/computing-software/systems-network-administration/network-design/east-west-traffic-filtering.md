---
id: computing-software.systems-network-administration.network-design.east-west-traffic-filtering
name: east-west-traffic-filtering
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, segmentation, east-west-filtering, microsegmentation, internal-firewall, zero-trust]
level: practitioner
status: draft
description: "Filter east-west traffic inside data centres and campuses: internal firewalls vs ACLs vs host and hypervisor microsegmentation, flow discovery and staged enforcement."
sources:
  - https://csrc.nist.gov/pubs/sp/800/207/final
  - https://www.cisa.gov/zero-trust-maturity-model
  - https://docs.vmware.com/en/VMware-NSX/index.html
  - https://learn.microsoft.com/en-us/azure/architecture/networking/guide/network-level-segmentation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# East-west traffic filtering

North-south controls (internet edge) do nothing once an attacker is inside. Ransomware moves
laterally via SMB, RDP, WinRM, SSH between internal hosts; east-west filtering limits that.

## Enforcement points
| Point | Granularity | Notes |
|---|---|---|
| Internal NGFW between zones/VRFs | zone/subnet | inspection, logging; throughput and hairpinning cost |
| Switch/router ACLs, SGT/TrustSec, VRF separation | subnet/group | line rate, coarse, stateless ACLs |
| Hypervisor distributed firewall (NSX DFW, cloud SGs/NSGs) | per VM NIC | follows workload, no hairpinning |
| Host firewall / agent-based (Windows Firewall via GPO, Illumio, Guardicore) | per process/port | works across clouds; agent lifecycle |

## Approach
1. **Discover flows**: NetFlow/flow logs, agent visibility, for weeks. Build an application
   dependency map.
2. Define groups by role/application/environment, not by IP.
3. Write allow rules per application; block known lateral protocols between peer workstations first
   (quick win: workstation-to-workstation SMB/RDP/WinRM deny).
4. Run in **monitor/log-only mode**, review hits, then enforce gradually per application.
5. Default deny between environments (prod/dev), management via jump hosts only.

## Verify
- [ ] Attempted SMB/RDP from one workstation to another is denied and logged; application owners signed off rule sets; denied-flow reports reviewed weekly.
