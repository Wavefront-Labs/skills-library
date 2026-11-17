---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-relay-troubleshooting
name: dhcp-relay-troubleshooting
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcp-troubleshooting, relay-troubleshooting, dhcp-relay, ip-helper-address, giaddr, option-82, relay-agent, link-selection]
level: practitioner
status: docs-checked
description: "Fix clients that get no address via a DHCP relay: giaddr subnet selection, return path, relay agent information (option 82) and link selection."
sources:
  - https://datatracker.ietf.org/doc/html/rfc1542
  - https://datatracker.ietf.org/doc/html/rfc3046
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcpv4-relay-agent-information-option
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP relay troubleshooting

## How relaying works
1. The client broadcasts its request on its own link and sets `giaddr` to 0.0.0.0 (RFC 1542: a client MUST set giaddr to zero in requests).
2. The relay agent, with an interface on the client's link, forwards the request to the server on a different network and fills `giaddr` with its own address on that link. RFC 1542 describes giaddr as existing to carry requests via relay agents to servers on other networks, and replies back through them; it is not a router address for the client.
3. The server uses giaddr to choose the subnet. Kea: the relay normally has an address in the subnet from which the server assigns addresses, and the server uses the giaddr to pick that subnet.
4. The reply goes back through the relay to the client.

## Checklist
| Check | Why |
|---|---|
| The relay interface facing the clients carries the relay config and has an address in the client subnet | giaddr comes from it |
| The server has a subnet/scope matching giaddr | otherwise no subnet is selected and the server cannot answer |
| The server can reach giaddr and replies can return | replies go back through the relay |
| Firewalls between relay and server pass the DHCP server traffic | you can confirm with a capture on the server |
| Option 82 handling | RFC 3046 defines the Relay Agent Information option; a packet already carrying a non-zero giaddr from an untrusted source may be discarded by a relay (RFC 3046 requires discarding packets whose giaddr spoofs the relay's own) |
| Link selection | Kea supports the link-selection sub-option (RFC 3527) and uses it to choose the subnet when present; Kea has a `compatibility` setting `ignore-rai-link-selection` to ignore it |

## Captures
- Client VLAN: are DISCOVER broadcasts present and do OFFERs return?
- Server: is the relayed DISCOVER seen and what giaddr does it carry? No answer suggests a scope or configuration problem; an answer the client never sees suggests the return path, firewall or relay.

## Common gotchas
- Two relay targets without failover can produce duplicate offers and conflicts (practitioner experience; the cited pages do not state it).
- If an interface carries several subnets, confirm which address the relay uses as giaddr and that the server has a matching subnet.

## Verify
- [ ] Server log shows the request arriving via the relay's giaddr and an OFFER/ACK sent.
- [ ] Client receives an address in the correct scope.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 1542 section 3.4, RFC 3046 and the Kea DHCPv4 relay agent information sections. Removed as not in those pages: vendor commands (ip helper-address, ping source, tcpdump), the UDP 67 source-port rule, VRF relay syntax, secondary-address and snooping behaviours, and the Kea log message text. Packet-capture advice is kept as general practice.
