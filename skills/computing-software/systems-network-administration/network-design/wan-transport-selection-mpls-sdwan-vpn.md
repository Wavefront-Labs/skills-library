---
id: computing-software.systems-network-administration.network-design.wan-transport-selection-mpls-sdwan-vpn
name: wan-transport-selection-mpls-sdwan-vpn
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wan, mpls, wan-selection, sd-wan, internet-vpn, dia, transport-independence]
level: practitioner
status: docs-checked
description: "Choose WAN transport for sites: MPLS L3VPN, SD-WAN over broadband/DIA, plain IPsec VPN, or a mix, weighing SLAs, cost, cloud traffic and operational model."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html
  - https://www.rfc-editor.org/rfc/rfc4364
  - https://www.mef.net/mef-3-0-sd-wan/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAN transport selection: MPLS vs SD-WAN vs internet VPN

## Options
| | MPLS L3VPN (RFC 4364) | SD-WAN over internet/DIA (+/- MPLS) | Site-to-site IPsec over internet |
|---|---|---|---|
| Performance guarantee | set by the provider's SLA | best effort per path; app-aware steering across paths | best effort |
| Cloud/SaaS access | backhaul via hub or cloud on-ramp | local breakout per site | local breakout |
| Operations | provider runs the core; change via tickets | central controller, templates, visibility | per-device configs, scales poorly |
| Encryption | none by default (private, not encrypted) | built in | built in |

## Decision drivers
1. **Traffic pattern:** mostly SaaS/IaaS -> local internet breakout (SD-WAN). Mostly to a
   data centre -> MPLS or SD-WAN hub design both work.
2. **Application sensitivity:** voice/video and real-time OT benefit from MPLS QoS or from
   SD-WAN with two diverse paths.
3. **Site count and change rate:** dozens+ of sites changing often -> SD-WAN controller value.
4. **Compliance:** "private" MPLS is not encryption; check whether your standards require encryption on top (RFC 4364 does not itself encrypt the data).
5. **Diversity:** two transports from different carriers, different last-mile media (for example fibre and wireless) beat two circuits from one carrier sharing a duct.

## Common answer today
Hybrid: SD-WAN overlay across DIA/broadband + cellular backup, keeping MPLS only at sites
or for apps that need its SLA, then retiring it at renewal.

## Verify
- [ ] Decision record with traffic profile, per-site transport, diversity, cost model and exit plan for each contract.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 4364: the BGP/MPLS VPN methods do not by themselves encrypt data; Cisco SD-WAN design guide: backhauled internet traffic issues and Secure Direct Internet Access for local offload.
- Removed: cost-per-Mbps and lead-time rows, FEC/per-packet claim, 5G wording.
Method: documentation only; no commands were run.
