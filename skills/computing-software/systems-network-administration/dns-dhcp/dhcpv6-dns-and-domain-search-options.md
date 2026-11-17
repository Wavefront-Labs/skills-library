---
id: computing-software.systems-network-administration.dns-dhcp.dhcpv6-dns-and-domain-search-options
name: dhcpv6-dns-and-domain-search-options
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv6, dhcpv6-options, dns-servers, domain-search, kea, rdnss]
level: practitioner
status: verified
description: "Deliver DNS servers and domain search lists to IPv6 clients via DHCPv6 options 23/24 and RA RDNSS/DNSSL, including stateless DHCPv6 and OS differences."
sources:
  - https://www.rfc-editor.org/rfc/rfc3646
  - https://www.rfc-editor.org/rfc/rfc8106
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#standard-dhcpv6-options
  - https://www.rfc-editor.org/rfc/rfc9915
  - https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 options (DNS servers/domain search)

## Options
| DHCPv6 option | Content |
|---------------|---------|
| 23 `dns-servers` | list of IPv6 resolver addresses |
| 24 `domain-search` (IANA name OPTION_DOMAIN_LIST) | search list |
| 56 NTP server, 31 SNTP | time |
| 17 vendor-opts | vendor specifics |

Kea:
```json
"option-data": [
  { "name": "dns-servers", "data": "2001:db8::53, 2001:db8::54" },
  { "name": "domain-search", "data": "corp.example.com, example.com" }
]
```

## Stateless DHCPv6
With SLAAC addressing, routers set the O flag (Other configuration) in RAs (RFC 4861); clients send
Information-Request and get only options. Kea supports this stateless mode: it answers
INFORMATION-REQUEST with the configured options.

## RA RDNSS/DNSSL (RFC 8106)
Routers can put DNS servers and search lists directly in RAs (RDNSS is ND option type 25 and DNSSL
type 31). A client that does not run DHCPv6 can only use these, so best practice is to send both
RDNSS in RAs and the DHCPv6 options.

## OS behaviour
Support for DHCPv6 options 23/24 and for RDNSS/DNSSL differs by OS and version, and some clients do
not run DHCPv6 at all, so send both and test each client type you run.

## Verify
```
dhcpv6.option.type == 23
icmpv6.type == 134 && icmpv6.opt.type == 25         # RDNSS in RA
```
- [ ] Clients of each OS show the IPv6 resolvers (`resolvectl status` on Linux, or the OS's own resolver status view).
