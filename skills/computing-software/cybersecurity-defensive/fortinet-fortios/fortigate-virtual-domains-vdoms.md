---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-virtual-domains-vdoms
name: fortigate-virtual-domains-vdoms
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [vdom, fortios, multi-vdom, split-task-vdom, vdom-admin, management-vdom, vdom-resource-limits]
level: practitioner
status: draft
description: "Enable and manage FortiGate VDOMs with interface assignment, per-VDOM admins and resource limits."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: logical firewalls with separate policies and routing.

```
config system global
    set vdom-mode multi-vdom
end
config vdom
    edit "customer-a"
    next
end
config global
    config system interface
        edit "port5"
            set vdom "customer-a"
        next
    end
    config system admin
        edit "ca-admin"
            set accprofile "prof_admin"
            set vdom "customer-a"
            set password <PASSWORD>
        next
    end
end
config vdom
    edit "customer-a"
    config system vdom-property
        set session 100000
        set ipsec-phase1 20
    end
```
Resource limits are global (`config global; config system vdom-property`) per VDOM. Everything under `config global` is system-wide (interfaces, HA, admin, firmware, FortiGuard); policies, routing, VPN are per-VDOM.

Gotchas
- Enabling multi-vdom logs you out and moves existing config into `root`.
- Management VDOM defaults to `root`; the VDOM holding FortiGuard and DNS needs internet access.
- VPN licensing and some security profiles are per VDOM; check feature support.
- A VDOM that has no interface/IP cannot be deleted until its objects are removed.

## Verify
```
diagnose sys vd list
get system status
config global
get system vdom-property
```
Each VDOM lists its interfaces and resource usage.
