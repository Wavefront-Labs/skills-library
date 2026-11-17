---
id: computing-software.systems-network-administration.keepalived.lb-kind-forwarding-methods
name: lb-kind-forwarding-methods
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, lb-kind, forwarding, nat, direct-routing, tunneling, lvs]
level: practitioner
status: docs-checked
description: "lb_kind forwarding methods NAT, DR and TUN, and when each fits, per the load-balancing techniques page (NAT bottleneck, DR ARP caveat)."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/load_balancing_techniques.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lb_kind: forwarding methods

`lb_kind` accepts NAT, DR or TUN.

- **NAT:** director has two NICs, public and private; real servers sit on the private network and replies are translated back through the director. Hides real servers and saves public IPs, but the director carries both directions and can become a bottleneck.
- **DR:** the director picks a real server by scheduler and forwards; the real server replies directly to the client. Each real server must use the VIP as the reply source address. Scales better, but the VIP/MAC sharing creates an ARP problem: clients could reach real servers directly. Workarounds add configuration and management effort.
- **TUN:** the page has only a heading with no content, so no requirements are documented.

The healthcheck and mixing case studies use NAT.

## Checked

2026-11-04: NAT, DR and TUN behaviour confirmed against the Load Balancing Techniques page (TUN section is a heading only); lb_kind values in the configuration synopsis; NAT in the two case studies. Removed an over-broad claim about all case studies and the Verify line.
Method: documentation only; no commands were run.
