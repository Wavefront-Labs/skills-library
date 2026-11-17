---
id: computing-software.networking-hardware-and-wireless.kea.kea-dhcp-ddns-overview-and-startup
name: kea-dhcp-ddns-overview-and-startup
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp-ddns, d2, ddns, ncr, conflict-resolution, dhcid]
level: intro
status: docs-checked
description: "What the Kea DHCP-DDNS server (D2) does, how it matches requests to DNS servers, RFC 4703 conflict resolution, and how to start it."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ddns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kea-dhcp-ddns (D2) overview and startup
D2 performs the client side of RFC 2136 dynamic DNS for kea-dhcp4 and kea-dhcp6. The DHCP servers build NameChangeRequests (NCRs) from lease events and post them to D2, which matches each to DNS servers and carries out the updates.

Server selection: D2 holds separate forward and reverse catalogs of DDNS domains, each with one or more DNS servers. The domain whose name matches the longest portion of the FQDN wins (with `sample.example.com.` and `example.com.`, the former is best for `myhost.sample.example.com.`); no match rejects the request. With no forward domains defined, forward updates are ignored. Reverse matching builds the reverse name from the lease address.

Conflict resolution (RFC 4703): forward entries carry a DHCID record identifying the owning client, and only that client may change them. Enabled by default; the DHCP servers' `ddns-use-conflict-resolution` sets a flag in each NCR. When disabled, D2 still adds DHCID records but does not enforce ownership; do so only after careful consideration.

Running: it is a separate binary, normally controlled by keactrl. Switches: `-c file` (mandatory), `-d`, `-t file` (check config; exit 0 OK, 1 error), `-v`, `-V`, `-W`. The libdhcp_ddns_tuning.so hook adds procedural host names and per-client skipping.

## Checked

2026-11-08. Read the DHCP-DDNS Server chapter sections 13.1 to 13.3.1 in full: D2 role and NCRs, longest-match forward and reverse domain selection, RFC 4703 conflict resolution and the ddns-use-conflict-resolution flag, the command-line switches -c, -d, -t, -v, -V, -W and the libdhcp_ddns_tuning.so mention. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
