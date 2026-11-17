---
id: computing-software.cybersecurity-defensive.network-defence.external-dynamic-lists
name: external-dynamic-lists
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [external-dynamic-lists, edl, threat-feeds, firewall-blocklist, fortigate-threat-feeds, ioc-blocking]
level: practitioner
status: docs-checked
description: "Use external dynamic lists and threat feeds on PAN-OS and FortiGate: list types, file format, size and update limits, connection-loss behaviour and the EDL hosting service."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/use-an-external-dynamic-list-in-policy", "https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/9463/threat-feeds", "https://docs.paloaltonetworks.com/resources/edl-hosting-service"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External dynamic lists (EDLs) and threat feeds

## What they are
- PAN-OS: an external dynamic list is a text file hosted on an external web server from which the firewall imports IP addresses, URLs and domains. The firewall re-imports at the configured interval and enforces policy on the entries without a configuration change or commit. (Formerly called a dynamic block list.)
- FortiGate: a plain-text list imported from an HTTP or HTTPS server and exposed as a threat feed, usable for long-term allow or block policy or short-term blocks of compromised locations. STIX/TAXII format is also supported.

## FortiGate feed types and file format
- Types: FortiGuard Category (URL list), IP Address, Domain Name, MAC Address, Malware Hash (plus a separate EMS threat feed from FortiClient EMS).
- Plain text, one entry per line; `#` starts a comment. The file is limited to 10 MB or 131072 (128 x 1024) entries, whichever is hit first; the entry limit also follows the per-model table size. Entries beyond the limit raise a warning and are not loaded. There is no duplicate-entry validation.
- Update period: 1 minute, hourly, daily, weekly or monthly (up to 43200 minutes).
- URL lists: the scheme is optional and truncated; wildcards allowed at the beginning or end (`*.domain.com`); IPv6 URLs in `[ ]`. IP lists: single address, subnet or range, IPv4 or IPv6. Domain lists: simple wildcards (`*.test.com`) and IDN. Malware hash lists: MD5, SHA1 or SHA256 hex, optionally followed by a description.
- URL (category) and domain feeds share category numbers 192 to 221 (30 in total).
- Each device model has a global and per-VDOM limit on the number of feeds (shown by `print tablesize`, field `system.external-resource`), also bounded by memory.
- If the FortiGate loses connectivity with the server, the feed keeps working (even across a reboot) but gets no new entries until the connection returns; a Connection Status error is shown.

## Palo Alto EDL Hosting Service
Palo Alto Networks maintains feed URLs of SaaS application endpoints, checked daily for new endpoints published by the SaaS provider. Using one as the EDL source avoids hosting your own list. Palo Alto Networks removes duplicates and aggregates addresses into contiguous ranges to shorten each list.

## Self-check
- [ ] Each list stays under the platform limits for file size, entries and feed count.
- [ ] You can see the feed's connection status and notice a failed refresh.

## Checked

Confirmed on the PAN-OS 11.1 EDL page (only its introduction and topic list render), the FortiOS 7.4.0 Threat feeds page and the Palo Alto EDL Hosting Service page. Removed because the pages do not state them: HTTPS certificate-profile and storage-access advice, a 5 minute to 1 hour refresh guidance, "keeps last good list" on PAN-OS, exception-list and validation pipeline advice, rule placement, `request system external-list show` and any Palo Alto entry or platform limits.

Method: docs-only read of cited pages, 2026-11-08
