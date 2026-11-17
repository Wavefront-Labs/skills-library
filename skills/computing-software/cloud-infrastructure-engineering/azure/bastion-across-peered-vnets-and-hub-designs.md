---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-across-peered-vnets-and-hub-designs
name: bastion-across-peered-vnets-and-hub-designs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, bastion-peering, bastion-hub, hub-and-spoke, virtual-wan, vnet-peering]
level: practitioner
status: docs-checked
description: "Use one Bastion in the hub for all peered spokes: peering requirements, RBAC on spoke VMs, NSG rules, Virtual WAN alternatives and cross-subscription access."
sources: ["https://learn.microsoft.com/azure/bastion/vnet-peering", "https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke", "https://learn.microsoft.com/azure/bastion/bastion-faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bastion across peered VNets and hub designs

**Goal:** a single Bastion (per region) in the hub reaches every spoke VM, including spokes in
other subscriptions, with access controlled by RBAC.

## How it works
Bastion connects to VMs in **directly peered** VNets (local or global peering). It does not
traverse transitively: hub Bastion → spoke VM works; spoke A Bastion → spoke B via hub doesn't.
Both local and global VNet peering are supported. Subscriptions in two different tenants are not supported.

## Connecting from the portal
The portal discovers Bastion by looking at peered VNets of the VM's VNet — the user needs
Reader on the VM, on the NIC with the VM's private IP, on the Bastion resource and on the VNets of the target VM.
Native client: specify the hub Bastion explicitly (`az network bastion ssh -n bas-hub -g rg-hub --target-resource-id <spoke-vm-id>`).

## NSGs
Spoke VM/subnet NSG: allow 22/3389 from the **hub AzureBastionSubnet prefix** (e.g. 10.0.1.0/26).
If spoke traffic is forced through a hub firewall with UDRs (e.g. 10.0.0.0/8 → firewall), the
return path from VM to the Bastion subnet becomes asymmetric and sessions drop. Add a more
specific UDR in the spoke route table for the Bastion subnet prefix with next hop
*VirtualNetwork* (peering), or exclude that prefix from the firewall route.

## Virtual WAN
Bastion can't be deployed inside a vWAN hub. Options:
- Bastion in a **spoke VNet** and the IP-based connection feature to reach VMs in other VNets across the vWAN hub (the documented option); `az network bastion rdp|ssh` take `--target-ip-address`. Validate routing and NSGs for each target.
- Bastion per spoke instead of one shared host.

## Region design
Global peering lets one Bastion reach VMs in other regions, but sessions then cross regions; prefer a Bastion per region for production.

## Gotchas
- Spoke owners can't see the hub Bastion without Reader → "Bastion not found" confusion; grant at hub VNet/Bastion scope via a group.
- Overlapping address spaces across spokes break IP-based connect.

## Verify
- [ ] Portal Connect on a spoke VM in another subscription offers the hub Bastion.
- [ ] Bastion audit logs show sessions to spoke IPs; spoke NSG allows only the Bastion prefix for 22/3389.

## Checked

2026-10-28. Confirmed on the Bastion VNet peering page, Bastion FAQ and az network bastion reference: local and global peering, Reader roles (VM, NIC, Bastion, target VNets), Bastion is not supported in a Virtual WAN hub (deploy in a spoke and use IP-based connection), cross-subscription works within one tenant, --target-ip-address and --target-resource-id exist on az network bastion rdp. Fixed: the vWAN spoke option was described as limited when the docs name IP-based connection through the hub. Removed: SKU requirement for IP-based connect, the forwarded-traffic claim and the peering state claim. The NSG/UDR asymmetric-routing advice is design guidance, not a documented figure.

Method: documentation only; no commands were run.
