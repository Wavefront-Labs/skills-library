---
id: computing-software.cloud-infrastructure-engineering.aws.outposts-local-zones-and-wavelength
name: outposts-local-zones-and-wavelength
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, outposts, local-zones, wavelength, edge-computing, hybrid-cloud, low-latency, data-residency, outposts-rack, outposts-servers, local-gateway, lgw, service-link, carrier-gateway, carrier-ip, 5g-edge, dedicated-local-zones, hybrid-architecture, enable-local-zone, local-zone-subnet, outposts-capacity, capacity-tasks]
level: practitioner
status: draft
description: "Place AWS compute where latency or residency demands it: Outposts racks/servers on-prem (service link, local gateway, capacity), Local Zones in metros, Wavelength in 5G networks, and their limits."
sources: ["AWS Outposts User Guide - Outposts rack and servers, local gateway and service link", "AWS Local Zones User Guide - Getting started and available services", "AWS Wavelength Developer Guide - Carrier gateway and carrier IPs", "AWS Whitepaper - Hybrid and edge architectures with AWS Outposts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outposts, Local Zones and Wavelength — AWS outside the region, with the same APIs and real limits

**Goal:** choose the right edge option for a latency, residency or local-processing need;
extend a VPC into it correctly; and design around the smaller service catalogue, fixed
capacity and region dependency each one has.

## 1. Which one
| Option | Where | Latency to users | Who operates hardware | Typical use |
|---|---|---|---|---|
| **Local Zones** | AWS-run facilities in metros (dozens worldwide) | single-digit ms in that metro | AWS | Media/gaming/real-time apps, data residency within a country without a region |
| **Wavelength Zones** | Inside telco 5G networks (Verizon, Vodafone, KDDI, SKT, Bell…) | < 10 ms over 5G | AWS + carrier | Mobile edge: AR/VR, V2X, live video analytics for carrier subscribers |
| **Outposts rack** | Your data centre (42U racks, from 1 to many) | LAN | AWS-owned, AWS-maintained; you provide power/space/network | Residency, low latency to on-prem systems, local data processing |
| **Outposts servers** (1U/2U) | Branches, factories, retail | LAN | AWS | Small footprints; EC2 + ECS/EKS local, no EBS/S3 on Outposts |
| **Dedicated Local Zones** | AWS-built for a single customer/community | — | AWS | Government/regulated |
All are **extensions of a parent region**: control plane and most managed services live in
the region; losing the link degrades or stops management actions.

## 2. Local Zones
- Opt in: `aws ec2 modify-availability-zone-group --group-name us-west-2-lax-1 --opt-in-status opted-in`
  then create **subnets in the Local Zone** in your existing VPC (`--availability-zone us-west-2-lax-1a`).
- Services (varies by zone): EC2 (subset of families), EBS (gp2/gp3), ALB, ECS/EKS nodes,
  FSx, ElastiCache/RDS in some, VPC endpoints limited. Check `aws ec2 describe-availability-zones --all-availability-zones` + the per-zone service list.
- Networking: an **internet gateway** in the VPC serves Local Zone subnets with local egress;
  NAT gateway in some zones; **Direct Connect** to a Local Zone for on-prem adjacency.
- Pattern: latency-sensitive tier (game servers, render, ingestion) in the Local Zone;
  state and control in the region; ALB in the Local Zone for local HTTP; Route 53 latency/geo routing to steer users.
- Pricing is higher than the region; capacity is finite — use ODCR for launches you must have.

## 3. Wavelength
- Opt in to the Wavelength Zone, create a subnet, attach a **carrier gateway** to the VPC
  (`create-carrier-gateway`) and route `0.0.0.0/0` of the Wavelength subnet to it; instances
  get **carrier IPs** (`allocate-address --network-border-group <wlz>`) reachable only from
  that carrier's network (not the public internet).
- Services: EC2 (limited types incl. GPU `g4dn`), EBS, ECS/EKS nodes, ALB in some zones; no NAT/IGW — egress to the internet goes via the carrier.
- Traffic between the Wavelength subnet and the region's subnets uses the VPC privately;
  devices on other carriers/Wi-Fi must be routed to the region or a Local Zone (latency
  routing at the app/DNS layer: resolve to the carrier IP only when on that carrier).
- Use for the last 10 ms: inference/edge rendering; keep auth/state in the region.

## 4. Outposts rack
- Order through the console (sizing: EC2 families `m5/c5/r5/i3en…` in fixed quantities,
  EBS gp2 capacity, S3 on Outposts capacity); AWS installs; 3-year term, all-upfront/partial/none.
- **Service link**: VPN-like encrypted connection to the parent region over your internet
  or Direct Connect (≥ 500 Mbps–1 Gbps recommended, ~1 Gbps+ for busy racks); required
  for control plane, monitoring and most APIs. Local workloads keep running during an outage but you cannot launch/modify.
- **Local gateway (LGW)**: routes between Outposts subnets and your on-prem network via
  BGP to your routers; **customer-owned IP (CoIP)** pool lets on-prem reach instances on
  your addresses. Subnets are created in your VPC with `--outpost-arn`.
- Services local: EC2, EBS, S3 on Outposts (separate API endpoint/bucket type), ECS, EKS
  (nodes; control plane in region), RDS (MySQL/PostgreSQL/SQL Server), ElastiCache, EMR,
  ALB, Route 53 Resolver endpoints, App Mesh — all with the region's APIs plus Outposts ARN.
- Capacity management: `aws outposts get-outpost-instance-types`, utilisation in CloudWatch
  (`AWS/Outposts` `InstanceFamilyCapacityUtilization`, `EBSVolumeTypeCapacityAvailabilityGB`,
  `ConnectedStatus`); **capacity tasks** reshape instance sizes; no autoscaling beyond what is installed — plan N+1 for host failure.
- Outposts servers: same model without EBS/S3; local NICs (LNI) to the on-prem LAN; EC2 + ECS/EKS/IoT Greengrass.
- Resilience: an Outpost is **one AZ-like fault domain**; for HA run two Outposts or Outpost + region with async replication (RDS read replica to region, S3 on Outposts → region replication).

## 5. Design rules common to all three
- Keep the **data of record in the region**; edge holds caches, buffers and local processing.
- Assume the link will fail: local DNS (Route 53 Resolver on Outposts / local resolvers), local
  auth caches, queues that buffer (Kinesis Agent/Greengrass StreamManager) and replay.
- IAM, KMS, CloudWatch, CloudTrail come from the region — latency on every control call.
- Tag and budget separately; edge capacity is prepaid or premium.
- Test the **link-down** scenario and the **region-impaired** scenario before go-live.

## Gotchas
- Local Zone subnets cannot host most managed services; an RDS in the region adds 20–60 ms — put a read replica/cache in the zone if the app is chatty.
- Wavelength carrier IPs are unreachable from your laptop; test from a device on that carrier or via the region.
- Outposts service link bandwidth is shared by EBS snapshots to region, S3 replication and control traffic — a big snapshot job can starve the control plane.
- Outposts EBS volumes cannot be attached across Outposts/AZs; snapshots go to the region (bandwidth, egress-free).
- Instance type availability in a Local Zone changes; pin a fallback type list in launch templates.
- Unconfirmed: current Local Zone/Wavelength locations and per-zone service matrices change frequently — check the Local Zones features page.

## Verify
- [ ] Measured latency from the target users/devices to the edge subnet meets the requirement (e.g. < 10 ms p95), vs region baseline.
- [ ] Edge tier keeps serving cached/buffered work for 30 min with the service link / region path blocked, then drains cleanly.
- [ ] Outposts: `ConnectedStatus` alarm and capacity utilisation alarm at 80 % exist; N+1 host capacity confirmed.
- [ ] Wavelength: client on the carrier reaches the carrier IP; off-carrier client is routed to the region endpoint.
- [ ] Data of record lives in the region (replication lag alarm from edge stores).
