---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-inter-vdom-links
name: fortigate-inter-vdom-links
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [inter-vdom-link, fortios, vdom-link, npu-vlink, inter-vdom-routing, internal-vdom]
level: practitioner
status: draft
description: "Connect FortiGate VDOMs with inter-VDOM links and route traffic between them with policy on both sides."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: traffic between tenants or a hub VDOM passes through firewall policy.

```
config global
    config system vdom-link
        edit "vlink0"
            set type ethernet
        next
    end
    config system interface
        edit "vlink00"
            set vdom "root"
            set ip 169.254.100.1 255.255.255.252
            set allowaccess ping
        next
        edit "vlink01"
            set vdom "customer-a"
            set ip 169.254.100.2 255.255.255.252
            set allowaccess ping
        next
    end
end
config vdom
    edit "customer-a"
    config router static
        edit 10
            set dst 0.0.0.0 0.0.0.0
            set device "vlink01"
            set gateway 169.254.100.1
        next
    end
    next
end
```
Each VDOM needs policies for traffic entering and leaving the vlink, plus routes back. With NP6/NP7 hardware, `npu-vlink` interfaces (`npu0_vlink0`/`npu0_vlink1`) offload this traffic (confirm availability by model).

Gotchas
- Overlapping subnets across VDOMs require NAT on the inter-VDOM link.
- `type ethernet` supports VLANs and dynamic routing; `ppp` links are older.
- Forgetting the return route is the most common failure.

## Verify
```
get router info routing-table all
execute ping-options source 169.254.100.2
execute ping 169.254.100.1
diagnose sys session list
```
Run per VDOM with `config vdom` then `edit` to switch context.
