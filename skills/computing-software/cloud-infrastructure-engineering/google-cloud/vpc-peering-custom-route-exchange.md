---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vpc-peering-custom-route-exchange
name: vpc-peering-custom-route-exchange
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, vpc-peering-routes, peering-custom-routes, vpc-network-peering, hybrid]
level: advanced
status: docs-checked
description: "Control what routes cross a VPC peering: subnet routes, import/export of custom routes, public-IP subnet routes, no transitive peering, and making on-prem reachable from a peer."
sources: ["https://cloud.google.com/vpc/docs/vpc-peering", "https://cloud.google.com/vpc/docs/using-vpc-peering", "https://cloud.google.com/vpc/docs/routes#routes_and_peering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC peering custom route exchange

## 1. Defaults
Subnet routes (private ranges) are always exchanged. **Custom routes** (static and dynamic/BGP) are
not, unless both sides opt in. Subnet routes using privately used public IPs are exported by default
but imported only if `--import-subnet-routes-with-public-ip` is set.

## 2. Exchange custom routes
```bash
# hub side (has VPN/Interconnect to on-prem)
gcloud compute networks peerings update hub-to-spoke --network=hub --export-custom-routes
# spoke side
gcloud compute networks peerings update spoke-to-hub --network=spoke --import-custom-routes
gcloud compute networks peerings list-routes spoke-to-hub --network=spoke --region=<R> --direction=INCOMING
```
For on-prem to reach the spoke, the Cloud Router on the hub must **advertise** the spoke's ranges:
```bash
gcloud compute routers update hub-router --region=<R> --advertisement-mode=CUSTOM \
  --set-advertisement-groups=ALL_SUBNETS --set-advertisement-ranges=10.20.0.0/16
```
(In default advertisement mode Cloud Routers do not advertise peering subnet routes; the custom advertisements must include the peered VPC's subnet ranges.)

## 3. Limits and design
- Peering is **not transitive**: spoke A cannot reach spoke B through the hub unless A and B are also connected to each other.
- Overlapping subnet ranges (one containing or fitting within another) make peering fail; plan IPAM up front.
- Peering group quotas (routes, instances, forwarding rules) count across the whole peering group.

## Gotchas
- Private services access uses a peering too; deleting it prevents creating new private connections for private services access.
- If the local VPC has a route with an identical or more specific destination, it always uses its local route over the peered one.

## Verify
- [ ] `list-routes --direction=INCOMING` shows on-prem prefixes in the spoke, and a spoke VM can reach an on-prem IP.

## Checked

2026-10-27. Confirmed in the VPC Network Peering overview and the routes pages and `gcloud compute networks peerings update/list-routes` and `gcloud compute routers update` reference pages: subnet routes always exchanged, privately used public IPv4 subnet routes exported but not imported by default, `--import-subnet-routes-with-public-ip`, `--export-custom-routes`, `--import-custom-routes`, custom advertisement mode needed on the Cloud Router for peered ranges, non-transitive peering, overlap rule, peering group quotas, local route precedence, private services access peering. Removed: NCC/NVA suggestion, default-route and tag-scoped export claims, `servicenetworking-googleapis-com` export advice, Connectivity Tests check. Read end to end.

Method: documentation only; no commands were run.
