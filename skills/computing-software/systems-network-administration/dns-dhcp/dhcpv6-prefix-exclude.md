---
id: computing-software.systems-network-administration.dns-dhcp.dhcpv6-prefix-exclude
name: dhcpv6-prefix-exclude
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv6, pd-exclude, prefix-delegation, rfc6603, kea]
level: practitioner
status: verified
description: "Use DHCPv6 prefix exclude (RFC 6603) with prefix delegation so a delegated prefix can include the CPE's WAN link subnet, configured in Kea pd-pools."
sources:
  - https://www.rfc-editor.org/rfc/rfc6603
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#prefix-exclude-option
  - https://www.rfc-editor.org/rfc/rfc9915
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prefix exclude

With prefix delegation (IA_PD) a CPE router receives, say, a /56. Some designs number the
provider-to-CPE link from the first /64 of that delegated prefix, saving address space and
simplifying routing. RFC 6603's PD Exclude option (67) tells the CPE which /64 inside the delegation
it must not assign to its LAN interfaces.

## Kea
```json
"subnet6": [{
  "id": 10, "subnet": "2001:db8:100::/48",
  "pd-pools": [{
    "prefix": "2001:db8:200::", "prefix-len": 40, "delegated-len": 56,
    "excluded-prefix": "2001:db8:200::", "excluded-prefix-len": 64
  }]
}]
```
Kea sends the excluded prefix only to a requesting router that includes option 67 in its ORO (Kea
ARM; its own example sends `2001:db8:1:8000:cafe:80::/72`). The ARM does not spell out how the
configured value is applied to each delegated prefix, so confirm with `kea-dhcp6 -t` and a test client
that every delegated /56 gets its own excluded /64 (Kea has no Windows build, so this was not run).

## Client support
Only a requesting router that asks for option 67 and honours it benefits; support varies by CPE, so
test the actual models before deploying.
- If a CPE ignores it, it may number its LAN from the excluded /64 and break the WAN link routing.

## Without prefix exclude
Use a separate WAN link prefix (/64 from a different pool, or link-local only with an unnumbered
design). This is a simpler alternative.

## Verify
```
dhcpv6.option.type == 67
```
The filter matches the option in the server's Reply (checked to parse in tshark 4.4.1); a client's
request for it appears in the ORO as `dhcpv6.requested_option_code == 67`.
- [ ] The CPE's LAN interfaces use /64s other than the excluded one, and the WAN link works in both directions.
