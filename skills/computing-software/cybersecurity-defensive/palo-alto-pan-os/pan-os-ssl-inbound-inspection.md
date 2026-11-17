---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ssl-inbound-inspection
name: pan-os-ssl-inbound-inspection
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ssl-inbound-inspection, pan-os, inbound-decryption, server-certificate, ssh-proxy, protect-servers]
level: practitioner
status: draft
description: "Inspect TLS to your own servers with PAN-OS SSL inbound inspection using the server certificate and key, and compare with forward proxy."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/decryption/configure-ssl-inbound-inspection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: see threats inside TLS sessions that terminate on servers you own.

```
configure
set rulebase decryption rules inbound-web from untrust to dmz source any destination web-public service any action decrypt type ssl-inbound-inspection web-server-cert profile DP-STD
commit
```
Requirements: import the server certificate and private key onto the firewall (Device > Certificate Management) as an ordinary certificate with its private key, referenced by name as above. The firewall passively decrypts using the key, so it does not terminate the session; this works only when key exchange allows it.

Limits
- Perfect forward secrecy ciphers (ECDHE, DHE) and TLS 1.3 cannot be decrypted by key-only inspection; terminate TLS on the firewall with forward proxy style, or put a reverse proxy / load balancer in front. Confirm cipher support for your release.
- Where a WAF or load balancer already terminates TLS, inspect plain HTTP behind it instead.

Gotchas
- A key rotation on the server needs the same rotation on the firewall, or the decryption silently stops.
- Exporting a private key to the firewall widens your key custody risk; use a dedicated key if possible.

## Verify
```
show session all filter destination 203.0.113.10
```
Traffic log Decrypted = yes, and the application should be identified beyond ssl; if it remains ssl, decryption did not apply.
