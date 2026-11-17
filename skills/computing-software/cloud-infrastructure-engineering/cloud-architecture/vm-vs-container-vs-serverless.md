---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.vm-vs-container-vs-serverless
name: vm-vs-container-vs-serverless
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, vm-vs-container-vs-serverless, compute-decision-tree, serverless, containers]
level: practitioner
status: docs-checked
description: "Decide between VMs, containers and serverless functions on Azure using the compute decision tree: control, operational overhead, scaling, skills and limits."
sources: ["https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree", "https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/compute-and-hardware.html", "https://cloud.google.com/architecture/framework/performance-optimization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM vs container vs serverless decision

## Decision factors (Azure services, from the Azure compute decision guide)
| Factor | Virtual Machines | Containers (AKS, Container Apps, Container Instances) | Azure Functions |
|---|---|---|---|
| Hosting model | IaaS: most control, flexibility and portability | AKS gives direct Kubernetes API access; Container Apps is serverless on Kubernetes without that access; Container Instances has no orchestration | FaaS: manages nearly all of running the app |
| Operational overhead | High | AKS high; Container Apps low; Container Instances very low | Very low |
| Density / nodes | Agnostic; 1 node minimum (two or more for the higher SLA) | AKS production minimum 6 nodes (3 system, 3 per user pool); Container Apps serverless | Serverless on Consumption and Flex Consumption plans |
| Autoscaling | Virtual machine scale sets | AKS pod and cluster autoscaling; Container Apps scaling rules; Container Instances not supported | Built in |
| Scale limits | 1,000 nodes per scale set (platform image), 600 (custom image) | AKS 5,000 nodes (Standard or Premium tier); Container Apps 1,000 replicas per revision | 200 instances (Consumption), 1,000 (Flex Consumption) |
| GPU | Supported | AKS and Container Apps supported; Container Instances not | Not supported |

## Steps
1. **Start from the flowchart** (migrate versus build new; need full control; HPC; event-driven; orchestration) and treat
   the result as a starting point. Evaluate each distinct component separately: a solution can use two or more services.
2. **Hard constraints first**: GPU needs, special hosting (SAP, Oracle, VMware, bare metal), control of the OS.
3. **Weigh control against management effort**: IaaS gives control but you manage the VMs and networks; PaaS and FaaS
   shift that work to the platform.
4. **Team skills and overhead**: the guide maps VMs to OS administration skills, AKS to Kubernetes administration,
   Container Apps to teams wanting modern patterns without Kubernetes complexity, Functions to event-driven developers.
5. **Check limits, SLAs, regional availability and pricing** in the vendor pages; every listed platform is regional and
   needs an external router for multiregion topologies.
6. **Model cost at expected and peak traffic** using the vendor pricing calculator, and record an ADR with a revisit
   trigger (local practice).

## Gotchas
- Kubernetes for a couple of services adds cluster management, upgrade and security overhead without benefit.
- Check serverless limits and the plan you use: Functions features such as virtual network integration depend on the plan.

## Verify
- [ ] ADR lists constraints, the cost model at two traffic levels and a revisit trigger.

## Checked
2026-11-08. Confirmed against the Azure "Choose an Azure compute service" page (hosting models, node minimums,
autoscaling, scale limits, team skills and overhead, GPU, regional-only note, last updated 2026-02-19). The AWS compute
and hardware page lists PERF02 best practice titles only and the Google performance pillar page gives principles only.
Removed: Lambda 15 minute and Azure Functions 10 minute limits, startup-time and Cloud Run or Fargate scale-to-zero
claims, cold-start and database connection advice (not stated on these pages).
Method: documentation only; no commands were run.
