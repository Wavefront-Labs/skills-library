---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-types-overview
name: alias-types-overview
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, alias-types, firewall, pf-tables]
level: intro
status: docs-checked
description: "OPNsense alias types and when to pick each: hosts, networks, ports, MAC, URL tables, GeoIP, network group, BGP ASN, OpenVPN group, internal and external."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alias types overview

Aliases (Firewall > Aliases) are named lists of hosts, networks or ports that you select by name in rules, NAT and other firewall sections, so one edit updates every rule that uses them. The overview page has a search box and type/category filters, plus two status columns for network and host aliases: Loaded# (entries planned for the table, useful for spotting which alias overflows when memory is short) and Last updated (timestamp of entries saved to disk). Port aliases are embedded in the rule itself, so they never show up in those tables.

Types available:

- Hosts: single IPs, ranges written like 10.0.0.1-10.0.0.10, FQDNs, or host exclusions starting with "!".
- Networks: CIDR blocks, "!" exclusions, or wildcard masks.
- Ports: single numbers or a range with a colon, such as 20:30.
- MAC addresses: full or partial (for example f4:90:ea), case insensitive.
- URL (IPs) fetched once; URL Tables (IPs) and URL Table in JSON format fetched at intervals.
- GeoIP: whole countries or continents.
- Network group: combines other host and network aliases.
- Dynamic IPv6 Host: follows a changing delegated prefix.
- BGP ASN: networks announced by an autonomous system.
- OpenVPN group: addresses of logged-in users in a group.
- Internal (automatic): product-managed, prefixed with two underscores.
- External (advanced): only a placeholder; content comes from a plugin, API call or script.

Nesting is allowed for host and network aliases, so you can name individual servers and group them (for example critical_servers containing server_a and server_b), then reference the group in rules. Inspect any alias's live contents under Firewall > Diagnostics > Aliases. Choose the narrowest type that matches the data; use Network group when you want a picker that only lists valid member aliases.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
