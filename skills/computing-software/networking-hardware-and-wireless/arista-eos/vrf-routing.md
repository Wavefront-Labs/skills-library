---
id: computing-software.networking-hardware-and-wireless.arista-eos.vrf-routing
name: vrf-routing
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, vrf, ip-routing, vrf-instance, management-vrf]
level: practitioner
status: draft
description: "Create EOS VRFs, enable ip routing, put interfaces in VRFs and run commands with vrf."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRFs and routing
Goal: separate routing tables and enable routing.

```
ip routing
ip routing vrf TENANT-A
vrf instance TENANT-A
interface Vlan100
   vrf TENANT-A
   ip address 192.0.2.1/24
ip route vrf TENANT-A 0.0.0.0/0 198.51.100.2
vrf instance MGMT
interface Management1
   vrf MGMT
   ip address 203.0.113.10/24
```

```
show ip route vrf TENANT-A
ping vrf TENANT-A 192.0.2.50
show vrf
```

- Global `ip routing` is off by default on many EOS L2 images; a VRF needs its own `ip routing vrf`.
- Assigning `vrf` to an interface removes existing IP address; set the VRF first.
- Management uses `vrf MGMT`; `ssh`, `copy`, `ntp` need `vrf MGMT` to use it (`ntp server vrf MGMT`).

Gotcha: forgetting `ip routing vrf X` means routes are not installed. Also copying files over the management VRF requires `copy scp: ... vrf MGMT` syntax.

Operational tip: use `show ip route vrf all summary` to catch VRFs with missing default routes, and give each VRF a naming convention that matches your EVPN tenant and VNI plan.

## Verify
- `show ip route vrf TENANT-A` lists connected and static routes; `ping vrf` succeeds.
