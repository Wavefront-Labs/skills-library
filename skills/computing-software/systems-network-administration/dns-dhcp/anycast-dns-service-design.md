---
id: computing-software.systems-network-administration.dns-dhcp.anycast-dns-service-design
name: anycast-dns-service-design
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-security, anycast-dns, anycast, bgp, exabgp, bird, health-check-withdraw, internal-resolver-anycast, ecmp, catchment, nsid, resiliency]
level: advanced
status: docs-checked
description: "Design anycast DNS service: one address from many nodes, availability-coupled route withdrawal, ECMP and TCP risks, NSID for debugging."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4786
  - https://datatracker.ietf.org/doc/html/rfc5001
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anycast DNS service design

Anycast announces the same Service Address from several Anycast Nodes. Routing delivers each client's packets to one of them, so a node that stops serving can withdraw its route and traffic moves to the others without client changes.

## Couple routing to service health
- Packets start arriving at a node as soon as its route is advertised, so the node must be ready first. Advertise when the service is available and withdraw when it is not (RFC 4786 section 4.4.1).
- This can be done by running a routing protocol implementation on the same server as the DNS service, configured to advertise and withdraw in step with the health of the DNS software.
- If one advertisement covers two or more Service Addresses, withdrawing for one failing service may be wrong; the RFC points to routing requests to another node instead (its section 4.8).
- Avoid rapid advertise/withdraw oscillation, for example with a minimum delay after a withdrawal before re-advertising. Route flaps can be dampened by remote routers (section 4.4.4).
- Check that the service answers, not only that the process exists (the RFC speaks of the health of the software that processes requests).

## Routing pitfalls
- Over BGP on the global Internet a host route may not propagate; advertise a covering prefix that is short enough to pass common import policies. For IPv4 that is often a 24-bit prefix, but some policies filter on RIR allocation boundaries, so test.
- Equal-cost paths to different nodes can split the packets of one multi-packet transaction across nodes. TCP always has several request packets (the handshake), so it is exposed. Mitigate with careful IGP metrics or flow-hash ECMP that picks one node per transaction.
- Per-packet load balancing across links to different neighbour ASes that chose different nodes can make the service unavailable to clients behind that router, and the reordering it causes also hurts TCP.
- Flap dampening may key on AS_PATH: use the same origin AS for all nodes but diverse upstream ASes, so one unstable node does not get stable nodes dampened.

## Find out which node answered
- Anycast hides which node replied. The NSID option (RFC 5001) lets a client ask a name server to identify itself: the client sends an empty NSID option in an EDNS OPT record, and a server that honours it returns identifying data in the same option. Set a distinct identifier per node.
- NSID is not transitive: a request to a recursive server asks that server to identify itself, not the servers behind it.

## Verify
- [ ] Stopping DNS on a node withdraws its route and clients keep resolving through other nodes, with no flapping when it returns.
- [ ] NSID responses from clients at different sites show the nodes you expect.

## Checked

Confirmed against RFC 4786 (sections 4.4.1 to 4.4.4 in full, plus search for monitoring and identification text) and RFC 5001 (NSID request and response behaviour). Removed as not in the cited pages: BIRD, FRR and ExaBGP specifics and the shell health-check example, loopback address commands, the two-anycast-address resolver design, the /48 IPv6 prefix size, the provider-independent prefix requirement, BIND `server-id`, Unbound `identity:`, `id.server` and `dig +nsid` syntax, and the claim that a working-DNS node with broken recursion needs a recursive test. The bird.network.cz landing-page source was dropped.

Method: docs-checked 2026-11-09 against RFC 4786 and RFC 5001 (plain text from rfc-editor.org).
