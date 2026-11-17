---
id: computing-software.networking-hardware-and-wireless.strongswan.nat-traversal-and-mobike
name: nat-traversal-and-mobike
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, nat-traversal, mobike, udp-encapsulation, keepalive, port-nat-t]
level: practitioner
status: docs-checked
description: "NAT-T and MOBIKE in strongSwan: automatic port floating to 4500, encap = yes, NAT-T keepalives, mobike = no, non-ESP markers and custom server ports with charon.port_nat_t."
sources:
  - https://docs.strongswan.org/docs/latest/features/natTraversal.html
  - https://docs.strongswan.org/docs/latest/features/mobike.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nat traversal and mobike
**NAT-T** works without configuration and cannot be disabled. When NAT_DETECTION_SOURCE_IP / DESTINATION_IP hashes in IKE_SA_INIT reveal NAT, IKE moves to UDP 4500 and ESP is wrapped in UDP (RFC 3948): an 8-byte UDP header sits between the IP and ESP headers. A four-byte all-zero Non-ESP Marker after the UDP header distinguishes IKE packets (sent to charon) from ESP (handled by the kernel).

`encap = yes` on a connection sends a manipulated NAT_DETECTION_SOURCE_IP so the peer believes NAT exists, forcing ESP-in-UDP.

**Keepalives.** A peer behind NAT sends 0xff UDP packets to refresh the NAT mapping. `charon.keep_alive` defaults to 20s; set 0 to disable (e.g. behind static DNAT).

**MOBIKE** (RFC 4555) lets an initiator change its attachment point. strongSwan watches interfaces, addresses and routes and uses UPDATE_SA_ADDRESS to switch path. It is on by default; disable per connection with `mobike = no`. As initiator it switches to port 4500 from the IKE_INTERMEDIATE or IKE_AUTH request even without NAT, because MOBIKE_SUPPORTED is only exchanged in IKE_AUTH, so open UDP/4500 on firewalls.

**Custom server ports.** Use a single `remote_port` on the client. The server must accept UDP-encapsulated ESP on that port, so configure `charon.port_nat_t` (not `charon.port`; port 500 may then be blocked). The client must add a non-ESP marker to IKE packets sent to 4500 or a custom port; strongSwan adds one when neither port is 500, so it cannot send from port 500. The page notes this is handled automatically from 6.0.1.

## Checked
2026-11-04. Confirmed against the NAT Traversal and MOBIKE pages: NAT detection, encap, the Non-ESP Marker, the keepalive default and `charon.keep_alive`, MOBIKE behaviour, and the custom server port rules.

Method: documentation only; no commands were run.
