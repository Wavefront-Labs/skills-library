---
id: computing-software.messaging-and-integration.prosody.default-ports
name: default-ports
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, ports, firewall, networking]
level: intro
status: docs-checked
description: "Prosody default TCP ports: 5222 c2s, 5269 s2s, 5281 HTTPS, 5000 proxy65, and private ports 5280, 5347 and 5582, with which are public."
sources:
  - https://prosody.im/doc/ports
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default ports

Prosody uses almost exclusively TCP.

| Port | Exposure | Service |
|---|---|---|
| 5000 | public | file transfer proxy (mod_proxy65) |
| 5222 | public | client connections (mod_c2s) |
| 5269 | public | server-to-server (mod_s2s) |
| 5280 | private | unencrypted HTTP |
| 5281 | public | HTTPS |
| 5347 | private | external components |
| 5582 | private | telnet console |

Open the public ports in the firewall. The page marks 5280, 5347 and 5582 private; external components and the telnet console only ever listen on a local interface. Port 5280 was public before Prosody 0.12.0.

Verify: from outside, 5222 and 5269 accept connections while 5347 and 5582 do not.

## Checked

2026-11-04. Read the Prosody port and network configuration page: the seven default ports with their public or private marking, mostly TCP, and 5280 changing from public to private in Prosody 0.12.0 all match. Replaced the claim that every private port listens on loopback with the page's narrower statement, and dropped 5280 from the verify step because the page does not say it is loopback-only.

Method: documentation only; no commands were run.
