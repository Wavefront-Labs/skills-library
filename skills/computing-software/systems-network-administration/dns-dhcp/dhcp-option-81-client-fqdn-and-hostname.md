---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-option-81-client-fqdn-and-hostname
name: dhcp-option-81-client-fqdn-and-hostname
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcp-options, option-81, option-12, client-fqdn, ddns, kea, hostname]
level: practitioner
status: gated
description: "Control who registers DNS names for DHCP clients: option 12 hostname vs option 81 client FQDN flags (S, O, N), server overrides in Kea and Windows, and sanitising bad hostnames."
sources:
  - https://www.rfc-editor.org/rfc/rfc4702
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#ddns-for-dhcpv4
  - https://www.rfc-editor.org/rfc/rfc4703
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option 12 hostname and option 81 client FQDN

## Options
- Option 12 (Host Name, RFC 2132): the client's short name (`LAPTOP-7F3K`).
- Option 81 (Client FQDN, RFC 4702): name plus flags that negotiate who updates DNS:
  - `S` = 1: client asks the server to update the A record.
  - `O` = 1 (server sets): server overrode the client's preference.
  - `N` = 1: no DNS updates by the server.
  Windows sends option 81 with S=0 (I will update my A record, you do the PTR) by default. (gated: unconfirmed, source is paywalled or blocked)

## Server policies
Kea (dhcp4, global or per subnet):
```json
"ddns-send-updates": true,
"ddns-override-client-update": true,       // server updates A even if client wants to
"ddns-override-no-update": false,
"ddns-replace-client-name": "when-not-present",  // or always / never
"ddns-generated-prefix": "dhcp",
"ddns-qualifying-suffix": "clients.example.net.",
"hostname-char-set": "[^A-Za-z0-9.-]",
"hostname-char-replacement": "-"
```
`ddns-replace-client-name: always` with a generated prefix gives predictable names
(`dhcp-10-0-5-23.clients.example.net`; Kea builds them as prefix, dashed address, suffix, e.g.
`myhost-172-16-1-10.example.com` with the default prefix) for guest/IoT networks. `when-not-present`
generates a name only if the client sent none; `when-present` replaces only names the client sent;
`never` (the default) keeps the client's name. With `ddns-override-client-update` true the server
ignores a client's request to update its own A record and sends the N-S-O flags 0-1-1 (Kea ARM).

Windows DHCP: scope or server properties > DNS tab: "Always dynamically update DNS records",
"Discard A and PTR records when lease is deleted", "Dynamically update DNS records for DHCP clients
that do not request updates" (for option-12-only clients like printers and Linux). (gated: unconfirmed, source is paywalled or blocked)

## Why it matters
- Which identity owns the record: if clients update their own A record in AD DNS, the record is
  owned by the computer account; if the DHCP server updates it, by the server (use DnsUpdateProxy
  or a dedicated account to avoid ownership fights). (gated: unconfirmed, source is paywalled or blocked)
- Name collisions: two devices sending the same hostname (cloned images) overwrite each other; Kea
  D2 conflict resolution (DHCID records, RFC 4703) prevents a second client stealing a name.
- Garbage names (spaces, underscores, Unicode) need sanitising before DNS will accept them.

## Verify
- [ ] In a capture or Kea log, option 81 flags in the ACK show the intended policy, and the A/PTR
  records appear in DNS with the expected owner and suffix.
