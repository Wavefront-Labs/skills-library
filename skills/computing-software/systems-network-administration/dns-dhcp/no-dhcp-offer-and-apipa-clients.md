---
id: computing-software.systems-network-administration.dns-dhcp.no-dhcp-offer-and-apipa-clients
name: no-dhcp-offer-and-apipa-clients
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp-troubleshooting, no-dhcp-offer, apipa, 169-254, dhcp-relay, dhcp-snooping, pool-exhaustion]
level: practitioner
status: docs-checked
description: "Fix clients that never get an address and fall back to a 169.254 link-local address: check client, relay, server scope, pool and capture the DORA exchange."
sources:
  - https://www.rfc-editor.org/rfc/rfc3927
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-dhcp-guidance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No DHCP offer / APIPA clients

A client that cannot get a DHCP lease may configure an IPv4 link-local address in 169.254.0.0/16 (RFC 3927). Seeing one means DORA did not complete. Establish first: when it started, whether it affects all clients or one scope, whether the server is standalone or highly available (split scope, failover), and what changed.

## Client checks
- Cable/link up, adapter enabled, correct and current adapter driver.
- DHCP Client service running (`net start`, look for DHCP Client).
- No firewall on the client blocking UDP 67 and 68.
- MAC filtering on the switch the client uses.

## Server checks (Windows DHCP Server)
- DHCP Server service running and the server authorised.
- The scope for the client's subnet has free leases (scope statistics); look for BAD_ADDRESS entries in Address Leases.
- Static addresses on the network that are not excluded from the scope.
- With no relay agent, the server's bound address must be in the scope's subnet: `Get-DhcpServerv4Binding` / `Get-DhcpServerv6Binding`.
- Only the DHCP server is listening on UDP 67 and 68 (`netstat -anb`); WDS or PXE services must not hold the ports.
- IPsec environments: the DHCP server IPsec exemption is present.
- The relay agent address can be pinged from the server.
- Review configured DHCP policies and filters.

## Network path
- Clients in another subnet need a DHCP relay agent (IP helper) on their router or VLAN switch.
- Intermediate features known to cause problems: VRRP/HSRP, Dynamic ARP Inspection and DHCP snooping.

## Capture the exchange
Capture on both client and server (for example Wireshark, run as administrator), reproduce with `ipconfig /renew`, filter `dhcp` on the client and `dhcp.id == <Transaction ID>` on the server using the transaction ID from the client capture. Where the exchange breaks:
- DISCOVER on the client but not the server: dropped in the network.
- Server sent OFFER but the client never saw it: dropped on the way back.
- Client shows DISCOVER, OFFER, REQUEST but the server only DISCOVER and OFFER: REQUEST dropped.
- Server completed all four but the client saw no ACK: ACK dropped.
Once drops are confirmed, involve the network team.

Also check the System and DHCP-Server event logs (Applications and Services Logs > Microsoft > Windows > DHCP-Server); DHCP server debug logs default to `%windir%\System32\Dhcp`.

## Verify
- [ ] Client completes DORA in a capture and gets an address from the expected scope.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Microsoft Learn "DHCP troubleshooting guidance" page in full and RFC 3927 as the source for the link-local range (169.254.0.0/16). Removed as unsupported by those pages: Linux client commands, PortFast and 802.1X notes, vendor snooping and helper-address commands, Kea log names and statistics, client-class and pool-exhaustion detail, and the root-cause list.
