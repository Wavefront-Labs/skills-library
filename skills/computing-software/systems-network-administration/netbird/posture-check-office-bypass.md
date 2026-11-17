---
id: computing-software.systems-network-administration.netbird.posture-check-office-bypass
name: posture-check-office-bypass
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, office-network, network-range-check, split-routing, on-site-bypass]
level: advanced
status: docs-checked
description: "Stop on-site NetBird devices tunnelling office LAN traffic using a Block peer network range posture check on the routing policy, plus the public egress IP alternative."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/access-control/posture-checks/connecting-from-the-office.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: devices already in the office use the local LAN, remote users go through NetBird.

Setup (scenario: LAN 192.168.1.0/24, routing peer router-01, group route-users):
1. Access Control > Posture Checks: add a Peer Network Range check, action Block, range `192.168.1.0/24`. Add one range per site if needed.
2. Create a Network with router-01 as routing peer and the office LAN as a resource. Resources are not in `All`, so nothing is reachable until a policy allows it.
3. Create a policy: source `route-users`, destination the office resource, protocols and ports, with the posture check attached.

Behaviour: on site, the device address falls in the subnet, the policy does not apply, the route is not distributed and traffic uses the local interface. Off site, the route returns and traffic uses the NetBird interface (`utun100` on macOS, `wt0` on Windows and Linux by default).

Limits:
- Route changes after a network switch are not instant.
- Only IP addresses are compared, so a home network using the same range is blocked too.
- Local interface address matching varies by platform.

Alternative: block the office public egress IP (/32, /128 or CIDR). Behind a proxy, forward the real client IP. A phone on office Wi-Fi is also blocked.

## Checked

2026-11-04. Confirmed against the NetBird connecting-from-the-office page: scenario, Peer Network Range check with Block action, Network and resource setup, policy with check attached, on-site and off-site behaviour, interface names, three limits, public egress IP alternative and proxy note. Nothing removed.
Method: documentation only; no commands were run.
