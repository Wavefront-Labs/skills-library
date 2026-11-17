---
id: computing-software.cloud-infrastructure-engineering.azure.nat-gateway-deploy-with-public-ip-prefix
name: nat-gateway-deploy-with-public-ip-prefix
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nat-gateway, nat-gateway-deploy, public-ip-prefix, outbound-connectivity, snat]
level: practitioner
status: docs-checked
description: "Deploy an Azure NAT gateway with public IPs or a prefix, attach it to subnets, plan SNAT capacity and zones, and understand precedence over LB outbound rules and instance IPs."
sources: ["https://learn.microsoft.com/azure/nat-gateway/nat-overview", "https://learn.microsoft.com/azure/nat-gateway/quickstart-create-nat-gateway-cli", "https://learn.microsoft.com/azure/nat-gateway/nat-gateway-resource", "https://learn.microsoft.com/azure/nat-gateway/nat-availability-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy NAT gateway with a public IP prefix

**Goal:** all outbound internet traffic from a subnet uses known static IPs with enough SNAT
ports, independent of VM or load balancer configuration.

## Deploy
```bash
az network public-ip prefix create -g rg-net -n ippre-nat-weu --length 30 --zone 1     # 4 IPs
az network nat gateway create -g rg-net -n ng-weu-z1 --public-ip-prefixes ippre-nat-weu \
  --idle-timeout 4 --zone 1 --location westeurope
az network vnet subnet update -g rg-net --vnet-name vnet-spoke -n snet-app --nat-gateway ng-weu-z1
```
- Up to **16 public IPs** (individual and/or prefixes) per NAT gateway; each IP gives **64,512 SNAT ports**.
- Partners allow-list the prefix (e.g. /30) — adding IPs within it later doesn't change their rules.
- A subnet can have only one NAT gateway attached; one NAT gateway can serve multiple subnets in the **same VNet**.

## Precedence
A NAT gateway attached to a subnet becomes its default next hop for outbound internet traffic, and ranks first among the outbound methods (above instance-level public IPs, LB outbound rules and default outbound access).
A UDR sending 0.0.0.0/0 to an NVA or virtual network gateway **overrides** NAT gateway (NAT is not used for those flows).

## Zones
NAT gateway is zonal (or no zone) for the Standard SKU. For zone resilience with Standard: one NAT gateway per zone, each attached to
a zonal subnet with zonal VMs (subnet-per-zone design). The StandardV2 SKU is zone-redundant by default and also supports IPv6 public IPs; StandardV2 needs StandardV2 public IPs.

## Gotchas
- Basic SKU public IPs can't be used with NAT gateway.
- A Standard NAT gateway supports IPv4 public IPs only (StandardV2 supports IPv4 and IPv6).
- TCP idle timeout 4–120 min (UDP fixed at 4); long-lived idle TCP flows (DB connections) need keepalives < timeout.
- Inbound connections initiated from the internet are not possible through NAT gateway.

## Verify
- [ ] `curl -s ifconfig.me` from a VM in the subnet returns an IP in the prefix.
- [ ] `az network vnet subnet show ... --query natGateway.id` set on every intended subnet.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (NAT overview, NAT gateway resource, availability zones, troubleshoot NAT connectivity, outbound connections ranking, CLI reference for `nat gateway`, `public-ip prefix`, `vnet subnet`): 16 public IP limit, 64,512 SNAT ports per IP, one NAT gateway per subnet, multiple subnets per gateway in one VNet, `--public-ip-prefixes`, `--idle-timeout`, `--zone`, `--nat-gateway`, `--length` flags, Basic public IPs unsupported, UDR to NVA/gateway overrides NAT gateway, StandardV2 zone redundancy and IPv6.
- Removed or rewritten: the GatewaySubnet claim and the Basic LB claim (not confirmed), and the vague StandardV2 note (now stated from the docs).

Method: documentation only; no commands were run.
