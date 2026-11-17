---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.hybrid-management-plane
name: hybrid-management-plane
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, hybrid-management-plane, azure-arc, anthos, gke-enterprise, aws-outposts, eks-anywhere, hybrid-cloud-operations]
level: advanced
status: draft
description: "Pick and design a hybrid management plane (Azure Arc, GKE Enterprise, AWS Outposts / EKS Anywhere) to govern, patch and deploy to on-prem and multi-cloud estates."
sources: ["https://learn.microsoft.com/azure/azure-arc/overview", "https://cloud.google.com/kubernetes-engine/enterprise/docs/concepts/overview", "https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html", "https://anywhere.eks.amazonaws.com/docs/overview/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid management plane

## Two different models
- **Projection (control plane in cloud, your hardware)**: Azure Arc projects servers, Kubernetes
  clusters and data services into Azure Resource Manager so Azure Policy, Defender, Monitor, RBAC
  and GitOps apply. GKE Enterprise (formerly Anthos) attaches clusters to a fleet with Config Sync,
  Policy Controller and service mesh. EKS Anywhere runs EKS distro on your hardware with optional
  console connection.
- **Provider hardware on-prem**: AWS Outposts racks/servers, Azure Local (formerly Azure Stack HCI),
  Google Distributed Cloud. Same APIs locally; provider owns the hardware lifecycle.

## Selection questions
1. Which cloud is the governance home (identity, policy, logging)? Pick its native plane.
2. Do you need cloud APIs locally (low latency, data residency) or just central governance?
   Governance only -> projection; local APIs -> provider hardware.
3. Disconnected operation? Outposts need a reliable service link to the parent region;
   check each product's disconnected mode limits.
4. What will you manage: servers (patching, inventory, extensions), Kubernetes, databases?

## Design steps
1. Inventory sites, clusters, OS versions; check agent support matrix.
2. Network: outbound HTTPS from agents to the provider endpoints (or via proxy / private link);
   document the endpoint allow-list.
3. Identity: onboarding service principal with least privilege; RBAC on the projected resources.
4. Organise projected resources in the same hierarchy as cloud ones (resource groups / fleets) so
   policies and tags inherit.
5. GitOps for configuration (Flux via Arc, Config Sync) and policy-as-code applied fleet-wide.
6. Monitoring and patch orchestration through the plane; measure agent health.

## Gotchas
- Agent sprawl: each plane needs its own agents; standardise on one governance home.
- Projection pricing is often per core / per vCPU per month for premium features; model it.
- Clock skew and proxy TLS inspection break agent onboarding; exempt the endpoints.

## Verify
- [ ] 100% of in-scope servers/clusters report healthy agents.
- [ ] A test policy applies identically to cloud and on-prem resources.
- [ ] Patch run completes on an on-prem server from the cloud console.
