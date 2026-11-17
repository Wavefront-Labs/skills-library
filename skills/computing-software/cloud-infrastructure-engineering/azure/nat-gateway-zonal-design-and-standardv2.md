---
id: computing-software.cloud-infrastructure-engineering.azure.nat-gateway-zonal-design-and-standardv2
name: nat-gateway-zonal-design-and-standardv2
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nat-gateway, nat-gateway-zones, standardv2-nat, zone-redundancy, outbound-connectivity]
level: advanced
status: docs-checked
description: "Design zone-resilient outbound with NAT gateway: Standard is zonal or no-zone, per-zone NAT stacks, the zone-redundant StandardV2 SKU and its migration and known issues."
sources: ["https://learn.microsoft.com/azure/nat-gateway/nat-overview", "https://learn.microsoft.com/azure/nat-gateway/nat-availability-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway zonal design and StandardV2

**Goal:** outbound internet survives a zone failure.

## Standard SKU behaviour
- A Standard NAT gateway is zonal (one availability zone) or placed in **No zone**; by default it is No zone and Azure
  picks the zone. After deployment you can't change the zone selection.
- It works with Standard public IPs or prefixes, and a Standard NAT gateway can use up to 16 IPv4 public IPs.

## Zonal isolation pattern (Standard)
One NAT gateway per zone with its own zonal public IP(s), attached to subnets whose VMs are pinned to that zone:
```bash
for z in 1 2 3; do
  az network public-ip create -g rg-net -n pip-natgw-z$z --sku Standard --zone $z
  az network nat gateway create -g rg-net -n natgw-z$z --zone $z --public-ip-addresses pip-natgw-z$z
  az network vnet subnet update -g rg-net --vnet-name vnet-app -n snet-app-z$z --nat-gateway natgw-z$z
done
```

## StandardV2 (zone-redundant)
- StandardV2 is zone redundant: it provides outbound connectivity from all zones in a region and maintains
  connectivity through a single zone failure. It also offers higher throughput than Standard, IPv6 support and flow log support.
- It requires StandardV2 public IPs or prefixes; Standard public IPs aren't supported. Up to 16 IPv4 and 16 IPv6 IPs.
- You can't upgrade Standard to StandardV2: create a StandardV2 NAT gateway to replace the Standard one on the subnet.
  Some regions don't support StandardV2 - check the list on the overview page.
- Known issues: adding a StandardV2 NAT gateway can interrupt outbound connections that use a load balancer, Azure
  Firewall or instance-level public IPs, and disrupts IPv6 outbound via load balancer outbound rules; adding it and
  enabling a service endpoint in one operation on a subnet with running VMs might fail, so do them separately.

## Gotchas
- NAT gateway takes precedence over other outbound methods (load balancer, instance-level public IP, Azure Firewall).
- You can't use NAT gateway with subnets that contain Basic resources (Basic load balancer or Basic public IPs).
- New outbound IPs mean partners must update allow-lists first.

## Verify
- [ ] Zone-down test or design review: subnets in surviving zones keep outbound; egress IPs are documented for partners.

## Checked
2026-10-31. Confirmed against Learn "What is Azure NAT Gateway": zonal/No zone behaviour, zone selection fixed after
deployment, 16-IP limits, StandardV2 capabilities, requirements, no in-place upgrade, known issues, precedence, Basic
resources restriction. Removed: 64,512 SNAT ports per IP, `--idle-timeout 10`, "one NAT gateway per subnet" wording,
zonal-IP matching rules, flow-reset claim, Chaos Studio mention.
Method: documentation only; no commands were run.
