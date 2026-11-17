---
id: computing-software.cloud-infrastructure-engineering.azure.ipv6-dual-stack-virtual-networks
name: ipv6-dual-stack-virtual-networks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet, ipv6, dual-stack, ipv6-load-balancer, ipv6-nsg, public-ip-ipv6]
level: advanced
status: docs-checked
description: "Add IPv6 to Azure VNets: dual-stack address space and /64 subnets, NIC IP configs, IPv6 public IPs and Standard LB, NSG rules, and service support gaps."
sources: ["https://learn.microsoft.com/azure/virtual-network/ip-services/ipv6-overview", "https://learn.microsoft.com/azure/virtual-network/ip-services/create-vm-dual-stack-ipv6-cli", "https://learn.microsoft.com/azure/load-balancer/ipv6-add-to-existing-vnet-cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 dual-stack VNets

**Goal:** workloads reachable over IPv6 (mobile carriers, government mandates) while IPv4 keeps
working — Azure VNets are dual-stack, not IPv6-only.

## Address plan
- Add an IPv6 address space of your choosing to the VNet (the example uses `fd00:db8:deca::/48`); IPv6 connectivity to the Internet is only established when you explicitly request it, for example with an IPv6 public IP.
- Each IPv6 subnet must be exactly **/64**.
```bash
az network vnet update -g rg -n vnet-web --address-prefixes 10.10.0.0/16 fd00:db8:deca::/48
az network vnet subnet update -g rg --vnet-name vnet-web -n snet-web --address-prefixes 10.10.1.0/24 fd00:db8:deca:1::/64
```

## VM NIC
```bash
az network nic ip-config create -g rg --nic-name nic-web1 -n ipconfig-v6 --private-ip-address-version IPv6 \
  --vnet-name vnet-web --subnet snet-web --public-ip-address pip-web1-v6
az network public-ip create -g rg -n pip-web1-v6 --sku Standard --version IPv6 --zone 1 2 3
```
Each NIC must keep at least one IPv4 IP configuration (IPv6-only VMs and scale sets aren't supported); IPv6 is added as a further IP configuration.

## Load balancer
Standard public and internal load balancers support IPv6, with an optional IPv6 health probe and multiple frontends using different IPv6 public IPs. A Basic IPv6 public load balancer is supported for legacy deployments. In a dual-stack setup, IPv6 health probes don't work unless a Network Security Group is active.

## NSG and routing
- NSG rules for IPv4 and IPv6 can live in one NSG, but a single rule can't combine an IPv4 and an IPv6 prefix.
- User-defined routes work for IPv6 traffic, for example towards an NVA.

## Support gaps (check current docs before designing)
- Azure Firewall doesn't support IPv6; it can run in a dual-stack VNet but the firewall subnet must be IPv4-only.
- Azure Container Instances and Azure Container Apps don't support IPv6 for containers.
- Azure Database for PostgreSQL Flexible Server can't be deployed in a VNet that has IPv6 addresses.
- Azure PaaS services are reached over their IPv4 endpoints from dual-stack VMs.

## Gotchas
- You can add IPv6 to existing IPv4 deployments without recreating them, but not to a VNet that has existing resource navigation links.
- DNS: add `AAAA` records (Azure DNS supports them).

## Verify
- [ ] `ip -6 addr` on the VM shows an address from the IPv6 subnet.
- [ ] From an IPv6 client, `curl -6 http://[<lb-v6-ip>]` reaches the backend.

## Checked

2026-10-31. Confirmed against the Learn IPv6 for Azure Virtual Network overview (dual-stack only, /64 subnets, at least one IPv4 configuration per NIC, load balancer IPv6 support and health probe NSG note, NSG rule and UDR behaviour, listed limitations, AAAA records, navigation-link restriction) and the dual-stack CLI tutorial commands via check_commands.py. Removed: the ULA claim, guest OS DHCPv6 advice, IPv6 outbound-rule claim, service-tag IPv6 coverage, App Service, VPN Gateway, ExpressRoute, NAT Gateway and Front Door statements, the alias-record claim and the external icanhazip check (none confirmed).

Method: documentation only; no commands were run.
