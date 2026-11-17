---
id: computing-software.networking-hardware-and-wireless.strongswan.eap-radius-backend
name: eap-radius-backend
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, eap-radius, radius, aaa, dae, attribute-forwarding]
level: advanced
status: docs-checked
description: "Delegate EAP authentication to a RADIUS server with the strongSwan eap-radius plugin: server sections, sockets, preference, DAE, attribute forwarding and EAP identity handling."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/eap-radius.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eap radius backend
The plugin relays the EAP conversation to a RADIUS server, so the gateway needs no specific EAP method. It is disabled by default: build with `--enable-eap-radius`. Select it per connection with `remote.auth = eap-radius`. For EAP methods that produce an MSK, the server must send the MS-MPPE-Send-Key and MS-MPPE-Receive-Key attributes.

**Servers** go in named subsections of `charon.plugins.eap-radius.servers`: `address` (IP or DNS name), `secret`, `nas_identifier` (default `[strongSwan]`), `port` (default 1812), `source` (from 6.0.1), `sockets` per server (default 1; one socket authenticates one client at a time), and `preference`.

**Several servers.** One is picked randomly, with loaded servers degraded and unreachable ones degraded further. A reachable server scores 110-210 by free sockets; preference is added. 0 is fair, 50 prefers it unless half the sockets are busy, 101 always prefers it unless unreachable. Avoid 110 or more.

**Session control.** A Session-Timeout is enforced with repeated authentication. The `dae` subsection (`enable`, `listen`, `port` default 3799, `secret`) accepts Disconnect-Request and CoA-Request.

**Attributes to the client.** Framed-IP-Address, Framed-IP-Netmask, Framed-IPv6-Address, DNS-Server-IPv6-Address, Microsoft and Cisco DNS/NBNS attributes and Cisco Unity attributes map to IKE configuration attributes. Any attribute can be forwarded via private notify 40969 using `forward.ike_to_radius` and `forward.radius_to_ike` (names or numbers; `PEN:number` for vendor attributes); clients can use the radattr plugin.

**Identity.** The first EAP-Identity uses the IKEv2 identity. Override with `remote.eap_id`; `%any` triggers an EAP-Identity exchange (build `--enable-eap-identity`). `eap_start = yes` lets the RADIUS server start the conversation, not supported by all servers.

## Checked
2026-11-04. Confirmed against the eap-radius plugin page: build flag, server options and defaults, preference scoring, session control, attribute mapping and forwarding, and identity handling.

Method: documentation only; no commands were run.
