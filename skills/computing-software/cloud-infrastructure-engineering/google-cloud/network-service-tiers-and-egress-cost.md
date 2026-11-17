---
id: computing-software.cloud-infrastructure-engineering.google-cloud.network-service-tiers-and-egress-cost
name: network-service-tiers-and-egress-cost
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-service-tiers, premium-tier, standard-tier, egress-cost, internet-egress, inter-region-egress, inter-zone-egress, data-transfer-pricing, cold-potato-routing, hot-potato-routing, anycast, cdn-egress, cloud-nat-cost, interconnect-egress, network-cost-optimization, egress-monitoring]
level: practitioner
status: docs-checked
description: "Choose Google Cloud Premium vs Standard Network Service Tier per resource: routing, feature limits, SLA, free tier, and how to set and switch tiers."
sources: ["https://docs.cloud.google.com/network-tiers/docs/overview", "https://docs.cloud.google.com/network-tiers/docs/set-network-tier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network Service Tiers and egress cost

**Goal:** choose the tier per workload rather than by default. Outbound data transfer pricing differs per tier
and by destination: take current figures from the Network Service Tiers and VPC network pricing pages, not from
a skill.

## 1. Tiers
| | **Premium** (default) | **Standard** |
|---|---|---|
| Routing | traffic travels within Google's network to reach users; inbound enters at the PoP closest to the user | uses peering, ISP or transit networks; inbound enters at the PoP closest to the region of the IP; outbound exits near the sending region |
| Features | all Google Cloud networking features; global external IPs | foundational set: Cloud NAT, regional external Application Load Balancer, regional external passthrough Network Load Balancer |
| SLA (VMs) | 99.99% uptime | 99.9% uptime |
| Fit | users in many places, multi-region backends | applications not latency sensitive, resources within one region |

- Standard Tier is unsupported for the global external Application Load Balancer and global external proxy
  Network Load Balancer, Cloud VPN gateways, and Cloud CDN (always Premium). Classic LBs can use Standard with a
  regional IP and forwarding rule, backends in that region only.
- Internal IP traffic between VMs always uses Premium infrastructure at standard VM-to-VM pricing; tier applies to
  internet-facing traffic on external IPs only.
- Cloud Storage is Premium by default; Standard is possible only when the bucket is the backend of an external
  Application Load Balancer in the same region as the forwarding rule (multi-region buckets need Premium).
- Free tier: 200 GB of Standard Tier usage per month in each region across all projects, per SKU.
- Google recommends Premium if unsure; it is the default.

## 2. Set and switch
```bash
gcloud compute project-info update --default-network-tier NETWORK_TIER
gcloud compute addresses create ADDRESS_NAME --region=REGION --network-tier STANDARD
```
A resource-level tier overrides the project default. The reference page lists `--network-tier` on addresses,
forwarding rules, instance creation and instance templates, and Global forwarding rules and global IPs are
always Premium.
- Premium and Standard use separate IP pools: changing an instance's tier changes an ephemeral IP, and an IP
  cannot move between pools or (for Standard) regions.
- A Standard regional LB cannot be changed to Premium in place: reserve a new Premium IP and migrate by DNS.
- Moving more than 5 Gbps from Standard to Premium independent of an outage needs your account manager, and
  re-labelling traffic Premium during a Standard outage does not help (treated as Standard).

## 3. Reduce cost (structure only)
- Use Standard Tier for single-region, non-latency-sensitive egress; keep user-facing multi-region on Premium.
- Keep compute and data in the same region; check egress SKUs in the billing export with the pricing pages open.
- Compare Interconnect and CDN egress on their own pricing pages before assuming a discount.

## Verify
- [ ] `gcloud compute project-info describe` shows the intended default tier, and Standard resources show `networkTier: STANDARD`.
- [ ] Global load balancers use Premium IPs (Standard is rejected for them).

## Checked
2026-11-09. Confirmed against Network Service Tiers overview (read in full) and Using Network Service Tiers
(searched for the commands and tier rules, not read in full). Removed: the price-class table, price percentages,
Cloud NAT, LB and Interconnect cost statements, the billing-export SQL and SKU names, GKE `PreferClose` advice,
the traceroute check and the specific error message, because the pricing pages were not read line by line.
Method: documentation only; no commands were run.
