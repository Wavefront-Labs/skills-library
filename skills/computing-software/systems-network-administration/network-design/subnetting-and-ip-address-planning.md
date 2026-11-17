---
id: computing-software.systems-network-administration.network-design.subnetting-and-ip-address-planning
name: subnetting-and-ip-address-planning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ip-address-planning, address-plan, subnetting, cidr, address-space-budget, hybrid-cloud, aws-vpc, azure-vnet, gcp-vpc, reserved-addresses, vpc-peering, transit-gateway, kubernetes, pod-cidr, service-cidr, eks, gke, aks, docker, default-address-pools, overlap, ip-conflict, renumbering, mergers-acquisitions, nat, ipam, netbox, phpipam, infoblox, capacity-planning, utilisation]
level: practitioner
status: verified
description: "Plan address space across on-prem, cloud VPCs, Kubernetes and VPNs: an org-wide budget, cloud reserved IPs, pod/service CIDR sizing, overlap avoidance, renumbering, IPAM-driven allocation."
sources:
  - https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html
  - https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq
  - https://cloud.google.com/vpc/docs/subnets
  - https://kubernetes.io/docs/concepts/cluster-administration/networking/
  - https://docs.netbox.dev/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnetting and IP address planning — one budget for every place an address can live

**Goal:** allocate addresses so that no two environments that may ever need to talk
(sites, cloud VPCs, Kubernetes clusters, VPN pools, partners) overlap, and every
allocation is recorded and summarisable. CIDR math, VLSM worked examples and the
per-site VLAN template are in
`computing-software.systems-network-administration.network-design.ip-addressing-and-subnetting`;
this skill is the organisation-level planning method that sits above it.

## 1. Inventory what already uses address space
Before allocating anything new, list every range in use or likely to be routed:
- on-prem sites, data centres, DMZs, out-of-band networks;
- every cloud VPC/VNet in every account, subscription and region;
- Kubernetes pod and service CIDRs (often invisible to network teams);
- Docker defaults on build hosts (`172.17.0.0/16`, then 172.18-172.31 as /16s and
  `192.168.0.0/16` as /20s for user-defined and compose networks), VPN client pools, SD-WAN overlays;
- partner/B2B tunnels and any acquired company's ranges.
Overlaps found here are the most expensive problem in the plan; find them now.

## 2. Budget the org space top-down
Carve RFC 1918 into large, aligned blocks by environment so each summarises to a single
route at the edge. An illustrative split of `10.0.0.0/8`:

| Block | Use | Size |
|---|---|---|
| 10.0.0.0/10 | On-prem sites (/16 each) | 64 sites |
| 10.64.0.0/10 | Public cloud (/16 per account-region, carved further) | 64 VPCs |
| 10.128.0.0/11 | Kubernetes pod ranges (routable) | |
| 10.160.0.0/11 | Reserved: acquisitions, future | |
| 10.192.0.0/10 | Reserved | |
Plus `172.16.0.0/12` for non-routed lab/test and a small, documented block for VPN pools.
Exact numbers are a design choice; the rule is: **aligned, contiguous, one summary per
environment and region, and at least half held in reserve.**

## 3. Cloud specifics
- Each provider reserves addresses per subnet: **AWS and Azure 5** (first four and the
  last), **GCP 4**. A /28 in AWS gives 11 usable, not 14.
- AWS VPC CIDRs are /16 to /28 and AWS subnets are /28 to /16; you can add secondary CIDRs later.
  GCP can expand a subnet's primary range but never shrink or replace it; Azure can resize a subnet
  only while no VMs or services are deployed in it. Size subnets for the largest autoscaling event plus load-balancer nodes
  and interface endpoints, which all consume IPs.
- VPC peering and Transit Gateway/Virtual WAN routing require **non-overlapping** CIDRs.
  Never accept the console default (`172.31.0.0/16` default VPC on AWS) for anything that
  may be connected.
- Spread subnets across availability zones from day one (e.g. a /20 per tier per AZ).

## 4. Kubernetes sizing
- Pod IPs = nodes × max pods per node. GKE defaults to a /24 per node (110 pods); EKS with
  the VPC CNI gives pods real VPC addresses, so a 50-node cluster can consume thousands of
  subnet IPs (prefix-delegation mode allocates /28s per ENI). Size the subnet accordingly.
- Overlay CNIs (Calico, Cilium, Flannel) use a separate pod CIDR. Defaults collide easily:
  Calico's sample `192.168.0.0/16` (`blockSize: 26`), Flannel's `10.244.0.0/16`, kubeadm's service CIDR
  `10.96.0.0/12`. Override them with ranges from your budget.
- Service CIDR is not routed outside the cluster but still must not overlap anything pods
  need to reach.

## 5. When ranges already overlap (mergers, legacy)
Options, best first:
1. **Renumber** the smaller side: move DHCP scopes first, then statics by DNS name,
   with lowered DNS TTLs and dual addressing during the transition.
2. **NAT at the boundary** (twice-NAT / static NAT pools) as a bridge, documented with an
   end date. It breaks protocols that embed IPs and complicates logging.
3. Isolate and proxy (application-level gateways) when neither is feasible.

## 6. Allocate through IPAM, never by hand
- One source of truth (NetBox, phpIPAM, Infoblox). Every prefix has an owner, site/VPC,
  VLAN and purpose.
- Allocate programmatically so two people cannot pick the same block, e.g. NetBox:
  `POST /api/ipam/prefixes/<parent_id>/available-prefixes/` with `{"prefix_length": 24}`.
- Cloud subnets created by Terraform should pull their CIDR from IPAM (provider/data
  source) instead of hard-coding.
- Alert on utilisation: plan expansion at ~70–80% of a subnet or pool, before DHCP or
  autoscaling fails.

## 7. Worked sizing example
A new app VPC: 3 AZs, tiers public/app/data, app tier autoscales to 300 instances, EKS
with VPC CNI at up to 40 nodes × 30 pods.
- App: 300 / 3 AZs = 100 per AZ, × 2 headroom = 200 → /24 per AZ.
- Pods: 1,200 / 3 = 400 per AZ, × 2 → /22 per AZ.
- Public and data: /26 per AZ each.
- Total = 3 × (256 + 1,024 + 2 × 64) = 4,224 addresses: just over a /20 (4,096), so
  allocate a /19 for the VPC, with the adjacent /19 reserved for growth so both
  summarise as a /18. Always add it up; "about a /20" is how VPCs run out.

## Verify
- [ ] Every range in use (including pod, service, Docker, VPN pools) is in IPAM.
- [ ] No overlap between any two environments that route to each other.
- [ ] Each environment/region summarises to one prefix; ≥ 50% of the org space unallocated.
- [ ] Cloud subnet sizes account for provider-reserved IPs and peak scaling.
- [ ] Utilisation alerts configured at 70–80%.
