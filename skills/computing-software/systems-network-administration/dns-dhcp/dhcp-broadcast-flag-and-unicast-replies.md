---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-broadcast-flag-and-unicast-replies
name: dhcp-broadcast-flag-and-unicast-replies
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, broadcast-flag, dhcpv4, relay-agent, unicast-offer]
level: practitioner
status: verified
description: "Understand the DHCPv4 broadcast flag: when servers and relays unicast vs broadcast OFFER/ACK, clients that need broadcast, and diagnosing lost replies."
sources:
  - https://www.rfc-editor.org/rfc/rfc2131#section-4.1
  - https://www.rfc-editor.org/rfc/rfc1542
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broadcast flag and unicast replies

A client without an IP address cannot always receive unicast IP packets. The BOOTP flags field's
**broadcast bit** (0x8000) tells the server or relay how to reply.

## RFC 2131 delivery rules (server/relay to client)
1. `giaddr` set (relayed): send to the relay (unicast port 67); the relay then delivers on the
   client segment.
2. `ciaddr` set (renewing client): unicast to ciaddr.
3. Broadcast bit set: broadcast to 255.255.255.255.
4. Otherwise: unicast to `yiaddr` using the client's MAC (`chaddr`) directly, without ARP.
In all cases, when `giaddr` is zero the server broadcasts any DHCPNAK.

## Why it matters
- A client that cannot receive unicast IP datagrams before it is configured SHOULD set the BROADCAST
  bit in its DISCOVER and REQUEST (RFC 2131 section 4.1); stacks with that limitation set the flag.
- Where DHCP snooping, ARP inspection or filters drop unicast OFFERs to an address that is not yet in
  their tables, clients that do not set the flag never get the OFFER.

## Wireshark
```
dhcp.flags.bc == 1
dhcp.option.dhcp == 2 && eth.dst == ff:ff:ff:ff:ff:ff
```
Compare Discover's flag with how the Offer was delivered (Ethernet/IP destination).

## Fixes
- Fix on the client where possible: systemd-networkd `RequestBroadcast=yes` in the `[DHCPv4]`
  section (its manual says not to enable it where broadcasts are filtered). Other clients have their
  own switches; ISC dhclient's man pages (dhclient(8), dhclient.conf(5)) list none for this flag.
- On the network: make sure DHCP snooping/ARP inspection and firewalls permit server-to-client
  unicast on UDP 68, and that relays deliver replies (relay platforms differ; check their docs for a
  broadcast-reply option).
- Server side, Kea follows the RFC 2131 delivery rules. It uses raw sockets by default, which receive
  broadcasts from directly connected clients; with `"dhcp-socket-type": "udp"` it cannot receive
  broadcasts from directly connected clients and serves relayed traffic only (Kea ARM).

## Verify
- [ ] Captures on the client segment show the Offer/ACK delivered in the mode the client requested, and the client binds.
