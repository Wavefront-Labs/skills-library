---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-dns-filter-profiles
name: fortigate-dns-filter-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [dns-filter, fortios, dnsfilter, botnet-domains, safe-dns, domain-filter, dns-sinkhole]
level: practitioner
status: draft
description: "Apply FortiGate DNS filter profiles to block malicious or unwanted domains by category or domain list, including botnet C&C domains."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop bad domains at resolution time regardless of port or SNI.

```
config dnsfilter profile
    edit "dns-std"
        config domain-filter
            set domain-filter-table 1
        end
        config ftgd-dns
            config filters
                edit 1
                    set category 26
                    set action block
                next
            end
        end
        set block-botnet enable
        set safe-search enable
    next
end
config firewall policy
    edit 10
        set dnsfilter-profile "dns-std"
    next
end
```
The profile applies to DNS requests that pass through the FortiGate (clients use external resolvers), or to the FortiGate's own DNS server if enabled as a DNS server on an interface (`config system dns-server`).

Gotchas
- Encrypted DNS (DoT/DoH) bypasses the filter unless DoT is deep-inspected or DoH is blocked by application control.
- Redirected block page sends clients to a Fortinet-hosted or local IP; ensure reachability or the user sees a timeout.
- The policy needs the DNS service in scope.

## Verify
```
diagnose test application dnsproxy 3
```
(confirm number per release.) From a client, `nslookup` a blocked test domain should resolve to the block-page address, and the DNS log records the action.
