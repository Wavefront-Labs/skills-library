---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.hybrid-cloud
name: hybrid-cloud
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, hybrid-cloud, azure-arc, aws-outposts, google-distributed-cloud, eks-anywhere, hybrid-management, data-gravity, latency-sensitive-on-prem]
level: advanced
status: draft
description: "Architect hybrid cloud deliberately: which workloads stay on-prem and why, connectivity and identity foundations, unified management (Arc, Outposts, GDC), data."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/hybrid/", "https://aws.amazon.com/outposts/", "https://cloud.google.com/distributed-cloud", "https://csrc.nist.gov/pubs/sp/800/145/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid cloud architecture

## Reasons that justify on-prem placement
Latency to factory/plant/store equipment, data residency where no cloud region qualifies,
large data gravity with existing systems, mainframe dependencies, depreciated hardware with
years left, disconnected/edge operation. "Because we always have" is not one — record the reason per workload.

## Foundations
1. **Connectivity**: redundant interconnect + VPN backup, non-overlapping IPs, hybrid DNS.
2. **Identity**: one IdP for both; workload identity across environments (federation/X.509).
3. **Unified management**: Azure Arc (servers, Kubernetes, data services projected into Azure
   management/policy), AWS Outposts/EKS Anywhere/ECS Anywhere/SSM hybrid activations, Google
   Distributed Cloud / GKE Enterprise (Anthos) fleets. Goal: same policy, monitoring and patching everywhere.
4. **Consistent platform**: Kubernetes + GitOps across sites so apps deploy the same way.
5. **Data placement**: decide system of record per dataset; replicate/cache where needed;
   minimise chatty cross-boundary calls (latency + egress).

## Gotchas
- Split applications (front end in cloud, DB on-prem) pay latency per query — move them together.
- Two operating models (ITIL on-prem, DevOps in cloud) for the same app slow everything; converge tooling.
- Hybrid appliances (Outposts, Azure Local) have capacity planning and hardware lead times like on-prem.

## Verify
- [ ] Placement rationale recorded per on-prem workload, reviewed yearly.
- [ ] Policy and monitoring coverage identical across environments.
