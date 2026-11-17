---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-transport-selection
name: pjsip-transport-selection
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, transport, udp, tcp, tls, srv, multihomed]
level: advanced
status: docs-checked
description: "Understand how PJSIP picks a transport for SIP requests and responses (URI transport parameter, SRV lookup, explicit transport) and how to lay out transports."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Transport-Selection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip transport selection
Requests: the URI is parsed and its transport parameter examined; absent means UDP, and a `sips` scheme means TLS. If the host is not an IP and has no port, DNS SRV is used for the transport type, so TCP and TLS URIs must carry the transport unless `sips` is used.

- No explicit transport: for UDP, a matching transport (type and address family) is chosen by hashing. For TCP/TLS, an open connection to the resolved address and port is reused; otherwise the first configured transport of that type and family opens a new connection.
- Explicit transport (endpoint `transport=`): UDP uses it; TCP/TLS tells it to connect, reusing an existing connection to that address and port.
- Multihomed UDP: the routing table picks the interface; if its address differs from the message source, the message is updated and a transport bound to the new address is used if one exists.

Responses: TCP/TLS reuse the connection the request arrived on if open; otherwise the first matching configured transport connects. For UDP, `rport` in the top Via sends via the receiving transport; with `maddr` or without `rport`, a matching transport is hashed.

Layout: single-interface IPv4 can use wildcard transports (`bind=0.0.0.0`, TLS on `bind=0.0.0.0:5061` with `cert_file`). With several interfaces define one transport per interface and name it on each endpoint's `transport=`. IPv6 binds use `bind=[address]`.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Transport Selection page: request steps (URI, SRV, explicit and implicit transport, multihomed UDP), response rules for rport, maddr and TCP/TLS, and the recommended layouts. Nothing changed.
Method: documentation only; no commands were run.
