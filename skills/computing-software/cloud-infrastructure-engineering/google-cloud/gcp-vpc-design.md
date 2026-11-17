---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcp-vpc-design
name: gcp-vpc-design
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, vpc-design, global-vpc, custom-mode-vpc, regional-subnets, secondary-ranges, alias-ip, gke-ip-planning, shared-vpc, vpc-peering, network-connectivity-center, firewall-policies, hierarchical-firewall-policies, network-firewall-policies, secure-tags, cloud-nat, cloud-router, private-google-access, private-service-connect, private-services-access, dns-peering, vpc-flow-logs, connectivity-tests, firewall-insights]
level: practitioner
status: docs-checked
description: "Design GCP VPCs: custom-mode global networks, regional subnets with GKE secondary ranges, Shared VPC, firewall policies with secure tags, Cloud NAT, Private Google Access and PSC."
sources: ["https://docs.cloud.google.com/vpc/docs/vpc", "https://docs.cloud.google.com/vpc/docs/subnets", "https://docs.cloud.google.com/vpc/docs/shared-vpc", "https://docs.cloud.google.com/vpc/docs/provisioning-shared-vpc", "https://docs.cloud.google.com/firewall/docs/firewall-policies-rule-eval-order", "https://docs.cloud.google.com/firewall/docs/tags-firewalls-overview", "https://docs.cloud.google.com/nat/docs/ports-and-addresses", "https://docs.cloud.google.com/vpc/docs/configure-private-google-access", "https://docs.cloud.google.com/vpc/docs/configure-private-services-access", "https://docs.cloud.google.com/vpc/docs/vpc-peering", "https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/vpc-spokes-overview", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/alias-ips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP VPC design — global networks, regional subnets, explicit everything

**Goal:** a VPC whose IP plan fits GKE and future regions, whose firewalling is
expressed as tag-based policies rather than per-project rules, and whose private
workloads reach Google APIs and managed services without public IPs. Org-wide hub
topology is in
`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone`.

## 1. The model differs from AWS/Azure
- A VPC network is **global**; subnets are **regional** (span all zones). One VPC can serve
  every region.
- Routes and firewall are network-level, not subnet-level.
- Always **custom mode**: auto mode creates a subnet in every region from the
  10.128.0.0/9 block, which collides with everything later. Stop new projects getting a
  `default` network with the org policy constraint `compute.skipDefaultNetworkCreation`.

## 2. IP planning (GKE drives it)
Subnet primary range for nodes/VMs, plus **secondary ranges** for GKE pods and services
(alias IPs, VPC-native clusters):
- Size pod and service ranges for 2-3x current scale from the GKE alias IP page; do not
  rely on remembered defaults.
- Add ranges later with **discontiguous multi-Pod CIDR** (additional pod IPv4 ranges)
  when you run short, but plan headroom now.
- Four IP addresses are unusable in every subnet's primary IPv4 range; count them.
- Check that every peer and on-prem path can route any non-RFC1918 range you use.

## 3. Shared VPC
Central network team owns a **host project** per environment; workload **service
projects** attach. Grant `roles/compute.networkUser` on **specific subnets** (not the whole
host project) to each service project's deploying principals; GKE additionally needs the
service-agent grants listed in the Shared VPC GKE guide. Firewall and routes stay with the
network team.

## 4. Firewalls: policies + secure tags
- **Hierarchical firewall policies** at org/folder: deny known-bad, allow Google health-check
  and IAP source ranges (take them from the load balancer and IAP docs), or use `goto_next`
  to delegate to the next level.
- **Global network firewall policies** per VPC for workload rules, targeting
  **secure tags** (IAM-governed resource tags) instead of legacy network tags.
- Evaluation order is documented on the rule evaluation order page: do not assume it, read
  it, and keep the implied rules in mind (the implied default is to allow egress and deny
  ingress); add an explicit egress deny with exceptions if you need egress control.

## 5. Egress and private access
- **Cloud NAT** (on a Cloud Router, per region) for VMs/GKE nodes without external IPs.
  Consider **dynamic port allocation** and set the minimum ports per VM deliberately:
  with dynamic port allocation `MIN_PORTS` must be a power of 2 between 32 and 32768, and
  the default is 32 (static allocation is a different setting). Manual NAT IPs if partners
  allowlist.
- **Private Google Access** per subnet lets internal-only VMs call Google APIs. With VPC
  Service Controls use `restricted.googleapis.com` (199.36.153.4/30) DNS + routes;
  otherwise `private.googleapis.com`.
- **Private Service Connect** endpoints give a private IP in your subnet for Google APIs
  or a producer's published service; **private services access** (VPC peering to a
  service-producer network) is the older path for Cloud SQL, Memorystore etc. — reserve an
  allocated range once per VPC and size it generously.

## 6. Connecting VPCs
VPC Network Peering does not provide transitive routing; **Network Connectivity Center**
VPC spokes join a hub in a mesh or star topology. Export custom routes explicitly when
peering to on-prem-connected networks.

## Gotchas
- Private services access ranges consumed by managed services cannot be shrunk; too small = Cloud SQL creation fails later.
- GKE pod ranges overlapping on-prem break hybrid traffic silently at the router.
- Legacy network tags in firewall rules can be changed by anyone able to set instance tags; secure tags are IAM-governed.
- Peering quotas and NCC pricing change: check the current docs before designing a large mesh.

## Verify
- [ ] No auto-mode or `default` networks; `compute.skipDefaultNetworkCreation` enforced.
- [ ] IP plan document covers nodes, pods, services and PSA ranges for 2-3x current scale, non-overlapping with on-prem.
- [ ] Service projects hold subnet-level `networkUser` only.
- [ ] Firewall rules target secure tags; Firewall Insights shows no shadowed/overly permissive rules.
- [ ] Connectivity Tests confirm intended paths; internal VMs reach APIs via PGA/PSC with no external IP.

## Checked
2026-10-28. Confirmed against the VPC, Subnets, Shared VPC, Cloud NAT ports, Private Google Access, private services access, VPC Peering, NCC VPC spokes, firewall rule evaluation order and GKE alias IP pages: global network and regional subnets, auto mode 10.128.0.0/9 block, `compute.skipDefaultNetworkCreation`, four unusable subnet addresses, `compute.networkUser` on subnets, `goto_next`, dynamic port allocation `MIN_PORTS` power of 2, 32-32768, default 32, 199.36.153.4/30 for `restricted.googleapis.com`, peering non-transitive, NCC mesh and star. Removed as not confirmed in those pages: pod/node sizing figures, services range size, health-check and IAP source ranges, `container.hostServiceAgentUser`, `ERRORS_ONLY`, the secure-tag example, the Cloud SQL PSC remark, the hierarchical-first evaluation sentence, and a wrong NAT default (64).
Method: documentation only; no commands were run.
