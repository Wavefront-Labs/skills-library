---
id: computing-software.cloud-infrastructure-engineering.google-cloud.private-nat-and-hybrid-nat
name: private-nat-and-hybrid-nat
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-nat, private-nat, hybrid-nat, overlapping-ip, ncc]
level: advanced
status: docs-checked
description: "Connect networks with overlapping IP ranges using Private NAT: NAT between NCC VPC spokes, Hybrid NAT toward on-prem over VPN/Interconnect, PRIVATE_NAT subnets and rules."
sources: ["https://cloud.google.com/nat/docs/private-nat", "https://cloud.google.com/nat/docs/set-up-private-nat", "https://cloud.google.com/nat/docs/nat-rules-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/rules/create", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/get-nat-mapping-info"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private NAT and Hybrid NAT

Private NAT translates private source IPs to other private IPs, for traffic between networks whose ranges overlap.
- **Private NAT for NCC spokes**: between VPC spokes of a Network Connectivity Center hub (and between spokes and hybrid spokes).
- **Hybrid NAT**: from a VPC to on-prem/other clouds reachable via Cloud VPN/Interconnect (dynamic routes learned by Cloud Router).

## 1. NAT subnet
```bash
gcloud compute networks subnets create pnat-range --network=VPC --region=REGION \
  --range=192.168.100.0/24 --purpose=PRIVATE_NAT
```
Its addresses become the translated source. The subnet must be in the gateway's region, must not overlap any subnet in the connected networks, and cannot hold other resources.

## 2. Gateway and rules
```bash
gcloud compute routers create pnat-router --network=VPC --region=REGION
gcloud compute routers nats create pnat --router=pnat-router --region=REGION --type=PRIVATE \
  --nat-custom-subnet-ip-ranges=app-subnet --enable-dynamic-port-allocation
# Inter-VPC: translate traffic to any NCC spoke
gcloud compute routers nats rules create 1 --router=pnat-router --region=REGION --nat=pnat \
  --match='nexthop.hub == "//networkconnectivity.googleapis.com/projects/PROJECT_ID/locations/global/hubs/HUB"' \
  --source-nat-active-ranges=pnat-range
# Hybrid NAT: translate traffic going to dynamic routes (on-prem)
gcloud compute routers nats rules create 2 --router=pnat-router --region=REGION --nat=pnat \
  --match='nexthop.is_hybrid' --source-nat-active-ranges=pnat-range
```

## 3. Return path
- Private NAT does not permit unsolicited inbound requests from connected networks, even if firewall rules allow them; only return traffic for connections the VPC started is translated back.
- Private NAT does not support destinations reached through VPC Network Peering.

## Gotchas
- Only source NAT for connections initiated from the VPC; inbound from on-prem to overlapping ranges needs another design (PSC, proxies).
- Private NAT does not support auto mode VPC networks; each gateway is tied to one VPC network, region and Cloud Router.
- Endpoint-independent mapping is not available for Private NAT; if no NAT rule matches, traffic is dropped.
- Egress firewall rules are evaluated before NAT and ingress rules after NAT.

## Verify
- [ ] On-prem firewall/logs show connections from the NAT range; `gcloud compute routers get-nat-mapping-info pnat-router --region=REGION` lists mappings.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (Private NAT overview): NCC spoke and Hybrid NAT variants, routes used (NCC subnet routes, dynamic routes), PRIVATE_NAT subnet requirement, no unsolicited inbound, no VPC Network Peering destinations, no auto mode networks, one VPC/region/Cloud Router per gateway, EIM unavailable, firewall evaluation order relative to NAT.
- Confirmed (set up Private NAT and NAT rules pages): NAT subnet must not overlap connected networks; match expressions nexthop.hub == "//networkconnectivity.googleapis.com/projects/.../hubs/..." and nexthop.is_hybrid; --source-nat-active-ranges; rule numbers 0-65000; unmatched traffic is dropped.
- Confirmed (gcloud reference): `subnets create --purpose=PRIVATE_NAT`, `nats create --type=PRIVATE`, `get-nat-mapping-info --nat-name --region`.
- Removed: custom-advertisement return path and hub export-filter advice (not found in the pages read).

Method: documentation only; no commands were run.
