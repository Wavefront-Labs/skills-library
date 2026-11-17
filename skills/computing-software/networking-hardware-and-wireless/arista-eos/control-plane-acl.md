---
id: computing-software.networking-hardware-and-wireless.arista-eos.control-plane-acl
name: control-plane-acl
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, control-plane, copp, service-acl, cpu-protection]
level: practitioner
status: draft
description: "Protect the EOS CPU with service ACLs on SSH/SNMP and review CoPP policy counters."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control-plane policing and service ACLs
Goal: limit who can reach management services and protect the CPU.

```
ip access-list MGMT-ONLY
   10 permit ip 192.0.2.0/24 any
   20 deny ip any any log
management ssh
   ip access-group MGMT-ONLY vrf MGMT in
management api http-commands
   protocol https
   ip access-group MGMT-ONLY vrf MGMT in
```

```
show policy-map copp
show policy-map interface control-plane copp-system-policy
show ip access-lists MGMT-ONLY
```

- EOS ships with a CoPP policy named `copp-system-policy`; customise with `system control-plane`.
- Service ACLs apply to SSH, SNMP, eAPI, NTP, and so on.

Gotcha: applying a service ACL without a permit for your own source locks you out; test in a configure session with a commit timer. Do not edit CoPP classes without understanding the platform defaults: confirm.

Operational tip: after changing service ACLs, open a second SSH session from an allowed source before closing the first, and keep a console path for recovery.

## Verify
- `show policy-map interface control-plane` has counters, and SSH from a disallowed host fails.
