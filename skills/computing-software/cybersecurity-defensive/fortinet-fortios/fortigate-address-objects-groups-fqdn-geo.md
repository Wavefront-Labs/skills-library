---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-address-objects-groups-fqdn-geo
name: fortigate-address-objects-groups-fqdn-geo
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [address-object, fortios, address-group, fqdn-address, geography-address, wildcard-fqdn, fabric-connector]
level: practitioner
status: draft
description: "Define FortiGate address objects - subnets, ranges, FQDN, geography and groups - and avoid FQDN resolution pitfalls."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: readable, reusable objects instead of raw IPs in policies.

```
config firewall address
    edit "LAN-NET"
        set subnet 10.1.0.0 255.255.0.0
    next
    edit "ERP-RANGE"
        set type iprange
        set start-ip 10.1.2.10
        set end-ip 10.1.2.20
    next
    edit "SaaS-example"
        set type fqdn
        set fqdn "app.example.com"
    next
    edit "Blocked-Geo"
        set type geography
        set country "KP"
    next
end
config firewall addrgrp
    edit "SERVERS"
        set member "ERP-RANGE" "SaaS-example"
    next
end
```
FQDN objects resolve through the FortiGate's DNS settings, and cached for the DNS TTL; wildcard FQDN (`*.example.com`) works for SNI and web-filter matching only in certain policy types (confirm).

Gotchas
- Using FQDN for services behind CDNs yields rotating IPs; matching may lag. Prefer fabric-connector dynamic addresses for cloud services.
- Address objects used in policies cannot be deleted; `show full-configuration | grep -f <name>` finds users.
- Interface-bound addresses (`set associated-interface`) limit where the object is valid.

## Verify
```
diagnose firewall fqdn list
show firewall address LAN-NET
```
The FQDN list shows resolved IPs for each FQDN object.
