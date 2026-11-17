---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ipv4-firewall-policy
name: fortigate-ipv4-firewall-policy
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [firewall-policy, fortios, policy-id, nat-enable, logtraffic, utm-status, policy-lookup]
level: practitioner
status: draft
description: "Create FortiGate IPv4 firewall policies with interfaces, objects, NAT, security profiles and logging, and test with policy lookup."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: explicit allow rules with inspection and logging; implicit deny at the bottom.

```
config firewall policy
    edit 10
        set name "lan-to-internet"
        set srcintf "INTERNAL"
        set dstintf "port1"
        set srcaddr "LAN-NET"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "HTTP" "HTTPS" "DNS"
        set nat enable
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set av-profile "av-std"
        set webfilter-profile "wf-std"
        set logtraffic all
    next
end
```
Policies are matched top-down; first match wins; the implicit deny at the end is not logged unless you add an explicit deny policy with logging.

Practice: use named policies, avoid `service ALL` and `srcaddr all`, set `logtraffic all` for troubleshooting or `utm` for security events only, and use policy IDs in change tickets.

Gotchas
- Moving a policy with `move 10 before 5` changes behaviour, not just display.
- ID 0 or unspecified chooses the next free ID; scripts should set it.
- Profiles need the right inspection mode (flow vs proxy) set in the policy/profile combination.

## Verify
```
diagnose firewall iprope lookup 10.1.0.5 12345 203.0.113.80 443 tcp port2
diagnose firewall iprope list 100004
```
The lookup returns the matching policy id; the GUI hit counter increments with traffic.
