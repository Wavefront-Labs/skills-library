---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-ddns-request-generation
name: dhcp4-ddns-request-generation
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, ddns, fqdn-option, ddns-override-client-update, client-delegation]
level: advanced
status: docs-checked
description: "When kea-dhcp4 sends DDNS requests (new lease, renewal with changed FQDN, release) and how FQDN N/S flags and override settings change them."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# when kea-dhcp4 generates DDNS requests
Prerequisites: `enable-updates` and `ddns-send-updates` both true. kea-dhcp4 decides what to update and sends NCRs to D2; D2 does the DNS work and conflict resolution.

Requests are generated when:
- a new lease is granted in response to a DHCPREQUEST that has the FQDN option (81) or Host Name option (12); if both, FQDN is used;
- a lease is renewed and its FQDN changed (two requests: remove old, add new);
- a lease is released (one request to remove entries).

Default handling of the FQDN N and S flags: client wants to do forward updates itself (client delegation), so the server sends a reverse-only request; client asks the server for both directions, so a request updates both; client wants no updates, so no request is generated. N=1 with S=1 is prohibited by RFC 4702 and the packet is dropped.

`ddns-override-client-update`: when true, client delegation is disregarded and both directions are updated; the server response flags N-S-O are 0-1-1. `ddns-override-no-update`: when true, requests are generated even if the client asked for no updates; response flags are 0-1-1. If a request carries only the Host Name option, kea-dhcp4 always generates requests and returns an FQDN option with N-S-O 0-1-0.

Since Kea 3.3.3, `ddns-reverse-zone` is included in each NCR to build the PTR name; unspecified or empty uses `in-addr.arpa.` (for 172.16.1.10 the PTR is `10.1.16.172.in-addr.arpa.`). Set to `example.com.` the name becomes `10.1.16.172.example.com.`; useful when parts of a reverse zone are delegated with CNAME records.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter section When Does the kea-dhcp4 Server Generate a DDNS Request, the FQDN flag table, and the ddns-reverse-zone paragraph (Kea 3.3.3). Added the ddns-override-no-update and Host Name only behaviour from the same section.
