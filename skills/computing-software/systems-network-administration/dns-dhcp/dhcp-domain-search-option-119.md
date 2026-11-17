---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-domain-search-option-119
name: dhcp-domain-search-option-119
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, option-119, domain-search, dns-search-list, rfc3397]
level: practitioner
status: verified
description: "Deliver DNS search lists with DHCP option 119 (and option 15), encoding rules, client support differences on Windows, Linux and macOS, and Kea/Windows config."
sources:
  - https://www.rfc-editor.org/rfc/rfc3397
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#standard-dhcpv4-options
  - https://www.rfc-editor.org/rfc/rfc1035
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
  - https://manpages.debian.org/bookworm/isc-dhcp-common/dhcp-options.5.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain search option 119

Option 15 gives a single domain name. Option 119 gives an ordered search list in
DNS wire format with compression (RFC 3397).

## Configure
Kea:
```json
"option-data": [
  { "name": "domain-name", "data": "corp.example.com" },
  { "name": "domain-search", "data": "corp.example.com, example.com, lab.example.com" }
]
```
ISC dhcpd: `option domain-search "corp.example.com", "example.com";`.
A server without a domain-list type for option 119 needs the raw RFC 3397 wire bytes (a plain
string would send the wrong bytes). Encode properly:
`corp.example.com` -> `04 63 6f 72 70 07 65 78 61 6d 70 6c 65 03 63 6f 6d 00`.
Later names may use RFC 1035 compression pointers: `corp.example.com`, `example.com`,
`lab.example.com` encode in 26 bytes as `04636f7270076578616d706c6503636f6d00 c005 036c6162 c005` (the
pointer `c005` points at the `example` label at offset 5). Wireshark 4.4.1 decoded exactly those
bytes in a test packet as `corp.example.com,example.com,lab.example.com`.

## Client behaviour
Support differs by OS and version, so test every client type you run. Resolvers read a search list from the `search`
entry of resolv.conf (resolv.conf(5)); how a client stores option 119 is up to the client.

## Gotchas
- Long search lists multiply failed lookups (each unqualified name tried against every suffix);
  combine with sensible ndots.
- Byte array mistakes produce garbled suffixes; capture the ACK and read `dhcp.option.dhcp_dns_domain_search_list_fqdn` (the Wireshark 4.4.1 field name).

## Verify
- [ ] `resolvectl domain` (Linux) or the OS's own resolver status tool shows the full search list in order on test clients.
