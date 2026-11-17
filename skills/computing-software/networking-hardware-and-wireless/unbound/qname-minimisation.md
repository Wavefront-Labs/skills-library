---
id: computing-software.networking-hardware-and-wireless.unbound.qname-minimisation
name: qname-minimisation
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, qname-minimisation, privacy, strict-mode, query-privacy]
level: practitioner
status: docs-checked
description: "Reduce what Unbound reveals to upstream servers with qname-minimisation, and when strict mode breaks resolution."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/use-cases/home-resolver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# qname minimisation
`qname-minimisation: yes` (manual default yes) sends only the minimum labels of the QNAME to each server and sets QTYPE to A when possible. It is best-effort: the full QNAME and original QTYPE are sent when an upstream reply has an RCODE other than NOERROR, except NXDOMAIN from a DNSSEC-signed zone. The home-resolver guide's minimal config sets it explicitly to send minimal information upstream.

`qname-minimisation-strict: yes` (default no) stops the fallback to the full QNAME for potentially broken nameservers. The manual warns many domains will not resolve and says to use it only if you know what you are doing; it only has effect when qname-minimisation is on.

Other options listed in the manual:
- `hide-http-user-agent` (default no) omits the User-Agent on outgoing HTTP, which some servers may reject; `http-user-agent` sets it explicitly.
- `pad-queries` (default yes) pads queries to TLS upstreams to a multiple of `pad-queries-block-size` (default 128).
- `use-caps-for-id` (default no) applies 0x20-encoded random casing to foil spoofing; the manual calls it experimental, so it is anti-spoofing, not privacy.

Forwarding to an upstream resolver exposes full queries to that resolver regardless of this option (general inference; the pages do not state it directly).

## Checked
Method: 2026-11-08 read the unbound.conf manual (first 100k characters, covering these entries) and the home-resolver guide. Added the best-effort fallback rule, defaults and block size; the forwarding caveat is inference and flagged as such.
