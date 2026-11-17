---
id: computing-software.cloud-infrastructure-engineering.azure.subnet-reserved-addresses-and-static-private-ips
name: subnet-reserved-addresses-and-static-private-ips
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-network, static-private-ip, reserved-addresses, subnet-sizing, nic-ip-configuration]
level: practitioner
status: docs-checked
description: "Plan subnet capacity with Azure's five reserved addresses per subnet, assign static private IPs on NICs the right way, and avoid setting IPs inside the guest OS."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-networks-faq#are-there-any-restrictions-on-using-ip-addresses-within-these-subnets", "https://learn.microsoft.com/azure/virtual-network/ip-services/virtual-networks-static-private-ip-arm-cli", "https://learn.microsoft.com/azure/virtual-network/ip-services/private-ip-addresses"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reserved subnet addresses and static private IPs

**Goal:** right-sized subnets and predictable IPs for DNS servers, NVAs and domain controllers.

## Five addresses reserved per subnet
Azure reserves the first four addresses and the last address of every subnet, so usable = size - 5. For
example, in `10.0.0.0/16` the reserved addresses are 10.0.0.0-10.0.0.3 and 10.0.255.255. Some services need larger
subnets; check each service's documentation.

## Static private IP on a NIC
```bash
az network nic ip-config update -g rg -n ipconfig1 --nic-name dc01-nic --private-ip-address 10.0.1.10
az network nic ip-config show -g rg -n ipconfig1 --nic-name dc01-nic --query "{ip:privateIPAddress,method:privateIPAllocationMethod}"
```
Setting an address switches allocation to **Static**. Dynamic is the default; a dynamic address is released when
the NIC is deleted, moved to a different subnet, or switched to static with a different address. Static addresses are
released only when the NIC is deleted. Dynamic allocation is not sequential or guaranteed, so use static when a
specific address is required.

## Inside the guest OS
Avoid assigning the static private IP from within the guest operating system; set it on the Azure network interface.
If you must set it in the OS, it has to match the address assigned to the Azure NIC, otherwise you can lose
connectivity to the VM.

## Gotchas
- To move a NIC to a different subnet, change the allocation method from static to dynamic, assign the NIC to the new
  subnet, then set static again with an address from the new subnet's range.

## Verify
- [ ] The allocation method is Static for infrastructure NICs and the subnet has headroom.

## Checked
2026-10-31. Confirmed on Microsoft Learn (private IP addresses, static private IP with the Azure CLI pages): five reserved addresses (first four and last), dynamic and static allocation and when each is released, moving a NIC between subnets, guest OS static assignment guidance. `az network nic ip-config update` checked against the CLI reference. Corrected: the old text said dynamic IPs are released on VM deallocation; the docs say on NIC delete, subnet change or switching to static with a different address. Removed: per-address roles (.1/.2/.3), /29 smallest subnet, service subnet sizes, VM restart on IP change, load balancer/private endpoint/Application Gateway/Firewall notes, top-of-range and scale-out advice.
Method: documentation only; no commands were run.
