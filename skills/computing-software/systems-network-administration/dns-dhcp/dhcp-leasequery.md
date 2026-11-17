---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-leasequery
name: dhcp-leasequery
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, leasequery, rfc4388, bulk-leasequery, relay-agent, kea]
level: practitioner
status: verified
description: "Use DHCP Leasequery (RFC 4388/5007) and Bulk Leasequery so relays and access concentrators recover lease state, with Kea lease_query hook configuration."
sources:
  - https://www.rfc-editor.org/rfc/rfc4388
  - https://www.rfc-editor.org/rfc/rfc5007
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-lease-query-so-leasequery-support
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leasequery

Access concentrators (CMTS, BNG, DSLAM relays) build forwarding and anti-spoofing tables by snooping
DHCP. After a reboot they lose that state; Leasequery lets them ask the server who holds an address.

## Protocols
- DHCPv4 Leasequery (RFC 4388): DHCPLEASEQUERY by IP, MAC or client-id; replies DHCPLEASEACTIVE,
  DHCPLEASEUNASSIGNED, DHCPLEASEUNKNOWN (option 53 values 10 to 13, see Test).
- DHCPv6 Leasequery (RFC 5007): LEASEQUERY by address or client ID, LEASEQUERY-REPLY.
- Bulk Leasequery (RFC 6926 v4, RFC 5460 v6): over TCP, all leases for a relay ID or link in one stream.

## Kea (`libdhcp_lease_query.so`, open source and available to every Kea user; it was previously ISC-support only)
```json
"hooks-libraries": [{
  "library": "libdhcp_lease_query.so",
  "parameters": {
    "requesters": [ "192.0.2.1", "192.0.2.2" ],
    "advanced": { "bulk-query-enabled": true, "active-query-enabled": false, "lease-query-tcp-port": 67 }
  }
}]
```
`requesters` must list the relay addresses allowed to query; queries from unknown requesters are logged and dropped (Kea
ARM). The library can only be loaded by kea-dhcp4 or kea-dhcp6. Under `advanced`, `bulk-query-enabled` defaults to
false, `active-query-enabled` must stay false if set, the TCP port defaults to 67 (DHCPv4) or 547 (DHCPv6), and
max-requester-connections 10, max-requester-idle-time 300, max-leases-per-fetch 100 are the documented defaults. The ARM
is inconsistent about the port key (the parameter list says `lease-query-port`, the examples use `lease-query-tcp-port`),
so check the documentation of your Kea version. Extended lease info (`store-extended-info`) is what lets queries by
relay ID or remote ID work.

## Test
Relays typically trigger it automatically after reload. Capture filter `dhcp.option.dhcp == 10` (LEASEQUERY); 11, 12 and 13
are the replies. Tested: scapy-built packets with option 53 = 10, 11, 12, 13 were shown by TShark 4.4.1 as `DHCP Lease query`,
`DHCP Lease Unassigned`, `DHCP Lease Unknown` and `DHCP Lease Active`, and the filter `dhcp.option.dhcp == 10` matched only the
first (scapy's `DHCPTypes` names them `lease_query`, `lease_unassigned`, `lease_unknown`, `lease_active`). perfdhcp's documented
exchanges are DORA and SARR style scenarios, so use the relay or scapy as a lab client.

## Verify
- [ ] After reloading the relay, it rebuilds its table via leasequery replies and existing clients keep working without renewing.
