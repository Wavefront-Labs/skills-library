---
id: computing-software.systems-network-administration.network-design.sso-nsf-stateful-switchover
name: sso-nsf-stateful-switchover
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, sso, nsf, stateful-switchover, graceful-restart, nsr, redundant-supervisor, stackwise-virtual, issu]
level: practitioner
status: docs-checked
description: "Use SSO with NSF/graceful restart (or NSR) on redundant supervisors and stacks so a control-plane failover keeps forwarding, and test it properly."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9600/software/release/17-9/configuration_guide/ha/b_179_ha_9600_cg.html
  - https://www.rfc-editor.org/rfc/rfc3623
  - https://www.rfc-editor.org/rfc/rfc4724
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSO, NSF and stateful switchover

Chassis with two supervisors or stacks/StackWise Virtual
pairs have an active and a standby control plane.
- **SSO (Stateful Switchover):** the standby is synchronised (config, L2 tables, interface
  state); on failure it takes over without resetting line cards; forwarding continues in hardware.
- But routing protocols restart on the new active. Without help, neighbours see the
  adjacency drop and withdraw routes: an outage despite SSO.
- **NSF / graceful restart** (OSPF RFC 3623, BGP RFC 4724; IS-IS has its own restart RFC): neighbours that
  are **NSF-aware** keep forwarding to the restarting router while it re-syncs.
- **NSR (non-stop routing):** the standby keeps full protocol state, neighbours do not even notice.
  Preferred where supported.

## Configure
Configuration is platform specific: follow the platform guide's SSO/NSF chapter (the Catalyst 9600
guide has "Configuring Nonstop Forwarding with Stateful Switchover"). Neighbours must be NSF-aware
(graceful restart helpers) for NSF to work.

## Design notes
- BFD with aggressive timers and graceful restart interact: BFD may declare the neighbour
  dead during switchover. Use BFD timers that tolerate the switchover time.
- FHRP: HSRP/VRRP state is synced in SSO on most platforms; verify.
- ISSU (in-service upgrade) relies on SSO; test the exact versions.
- Stacks: a member failure is not a supervisor failure; dual-attached hosts (EtherChannel
  across members) are what keeps them up.

## Verify
- [ ] The platform's redundancy status shows the standby hot in SSO mode and graceful restart enabled
  for each routing protocol.
- [ ] In a maintenance window, with continuous pings running, force a switchover: no more than a few
  pings are lost and no routing adjacencies flap at neighbours.

## Checked

2026-10-28: Confirmed: RFC 3623 (graceful OSPF restart), RFC 4724 (graceful restart mechanism for BGP), and that the Catalyst 9600 high availability guide has chapters on Nonstop Forwarding with Stateful Switchover, ISSU and StackWise Virtual. Removed: the IOS-XE configuration block, the platform list, the IS-IS RFC number, the claim that most platforms are NSF-aware by default, C-bit BFD wording and the show commands.
Method: documentation only; no commands were run.
