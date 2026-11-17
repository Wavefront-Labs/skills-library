---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-message-types-nak-decline-release-inform
name: dhcp-message-types-nak-decline-release-inform
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcp-message-types, dhcpnak, dhcpinform, dhcpdecline, dhcprelease, init-reboot, option-53, dhcp-decline]
level: practitioner
status: verified
description: "Understand every DHCPv4 message beyond DORA: NAK, DECLINE, RELEASE, INFORM, INIT-REBOOT and renew/rebind flows, and what each tells you when it shows up in logs or captures."
sources:
  - https://www.rfc-editor.org/rfc/rfc2131#section-3
  - https://www.rfc-editor.org/rfc/rfc2132#section-9.6
  - https://www.rfc-editor.org/rfc/rfc2132
  - https://github.com/isc-projects/kea
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DHCP message types

Option 53 carries the message type.
| Type | Name | Sent by | Meaning |
|---|---|---|---|
| 1 | DISCOVER | client | broadcast: who can give me an address |
| 2 | OFFER | server | here is an address |
| 3 | REQUEST | client | I take this one (selecting), or renew/confirm (renewing, rebinding, init-reboot) |
| 4 | DECLINE | client | the offered address is already in use (ARP probe got a reply) |
| 5 | ACK | server | confirmed, with lease time and options |
| 6 | NAK | server | your requested address is wrong for this network |
| 7 | RELEASE | client | I am done with the address |
| 8 | INFORM | client | I have an address (static); give me options only |

## Client states that matter
- INIT-REBOOT: client remembers its last address and broadcasts REQUEST for it after reboot or
  link up (no DISCOVER). Server ACKs if valid, NAKs if wrong network, or stays silent if it has no
  record (client times out and starts over).
- RENEWING at T1 (50 % of lease): unicast REQUEST to the leasing server.
- REBINDING at T2 (87.5 %): broadcast REQUEST to any server.

## What to read into them
- NAK after moving a laptop between VLANs: normal (INIT-REBOOT for the old subnet's address). NAKs
  storming for the same subnet: two servers with overlapping scopes disagreeing, or a relay
  forwarding to the wrong scope (giaddr mismatch).
- DECLINE: duplicate address (static IP inside the pool, or another DHCP server). The server marks
  the address as declined/abandoned for a while (Kea: `declined-addresses` statistic,
  `decline-probation-period`). Many declines shrink the usable pool.
- RELEASE: rarely sent (most clients just disappear); do not rely on it for capacity.
- INFORM: from statically addressed hosts asking for options only. Servers answer with ACK and no
  lease (RFC 2131 section 3.4).

## In captures and logs
```
dhcp.option.dhcp == 6          # Wireshark (field bootp.option.dhcp in old versions)
dhcp.option.dhcp == 4
```
Kea logs (dhcp4_messages.mes): `DHCP4_PACKET_NAK_0001` (no subnet could be selected for the packet),
`DHCP4_PACKET_NAK_0002` (invalid address requested by INIT-REBOOT), `DHCP4_DECLINE_LEASE`.

## Verify
- [ ] For a client fault you can sequence its messages and name which state it was in.
