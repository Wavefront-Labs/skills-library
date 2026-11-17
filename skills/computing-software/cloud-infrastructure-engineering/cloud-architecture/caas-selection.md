---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.caas-selection
name: caas-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, caas-selection, serverless-containers, managed-kubernetes, cloud-run, fargate, container-apps, eks, aks, gke]
level: practitioner
status: draft
description: "Choose between serverless container services (Cloud Run, Fargate, Container Apps) and managed Kubernetes using team size, workload shape, control needs and cost at scale."
sources: ["https://cloud.google.com/run/docs/overview/what-is-cloud-run", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html", "https://learn.microsoft.com/azure/container-apps/compare-options", "https://learn.microsoft.com/azure/architecture/guide/choose-azure-container-service"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Container platform choice: serverless containers vs managed Kubernetes

## Options in order of control
1. **Serverless containers** - Cloud Run, Azure Container Apps, AWS App Runner. Push an image, get
   HTTPS, autoscale to zero. No nodes, limited networking/sidecar control.
2. **Serverless task/pod runtime** - ECS on Fargate, EKS on Fargate, GKE Autopilot. You still model
   services/tasks or pods but do not manage nodes.
3. **Managed Kubernetes with node pools** - EKS, AKS, GKE Standard. Full Kubernetes API, DaemonSets,
   custom schedulers, GPUs, operators. You own upgrades, node pools, add-ons.

## Decision factors
| Factor | Lean serverless containers | Lean managed Kubernetes |
|---|---|---|
| Platform team | None or < 2 people | Dedicated platform team |
| Workloads | Stateless HTTP / event handlers | Mixed: stateful sets, operators, batch, GPU, service mesh |
| Portability need | Image + env vars is enough | Must run same manifests on several clouds / on-prem |
| Traffic | Spiky, idle periods (scale to zero) | Steady high utilisation (bin-packing saves money) |
| Ecosystem | Few add-ons | Needs Helm charts, CRDs, admission policy, DaemonSet agents |
| Compliance | Accepts provider-managed runtime | Needs node-level hardening or custom kernels |

## Cost crossover
Serverless containers bill per vCPU-second and GiB-second while serving (or always-on if
configured). At sustained high utilisation, nodes with committed-use/reserved pricing and good
bin-packing are cheaper; below roughly 30-40% average utilisation serverless often wins. Model both
with the pricing calculator using real request rate, duration and concurrency per instance.

## Procedure
1. Inventory workloads by type (HTTP, worker, cron, stateful, GPU).
2. Score the factor table; if more than ~80% fit serverless containers, start there and keep a
   Kubernetes cluster only for the exceptions.
3. Standardise the contract both ways: OCI image, env config, health endpoint, SIGTERM handling.
4. Record the decision and revisit thresholds (team size, spend) in an ADR.

## Gotchas
- Kubernetes for three stateless services is the most common over-build.
- Serverless container request timeouts and max instance limits bite batch jobs; use the
  platform's jobs feature (Cloud Run jobs, Container Apps jobs) instead of long HTTP calls.
- Autopilot/Fargate bill on pod requests; oversized requests are pure waste.

## Verify
- [ ] Each workload has a target platform and reason.
- [ ] Cost model at current and 5x load for both options.
- [ ] Same image deploys to the chosen platform and a fallback.
