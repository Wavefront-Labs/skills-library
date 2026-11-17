---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.managed-vs-self-managed
name: managed-vs-self-managed
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, managed-vs-self-managed, managed-services, operational-toil, build-vs-buy, kafka-vs-msk, postgres-on-vms-vs-rds, total-cost-of-ownership]
level: practitioner
status: draft
description: "Decide between a managed cloud service and running the software yourself: full cost including people and on-call, feature/version gaps, limits, lock-in, and exit options."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/framework/perf_architecture_evaluate_options.html", "https://learn.microsoft.com/azure/well-architected/operational-excellence/principles"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed service vs self-managed

## Compare honestly
| Factor | Managed (RDS, MSK, Elasticache, AKS…) | Self-managed on VMs/k8s |
|---|---|---|
| Infra price | higher per unit | lower per unit |
| People cost | lower: patching, backups, HA, upgrades done for you | on-call, upgrades, tuning, backups, DR — often 0.5-2 FTE per technology for production-grade ops |
| Features/versions | provider's subset; new versions lag | anything, any extension |
| Limits | service quotas, restricted superuser/config | your hardware limits |
| SLA | provider SLA for the service | yours |
| Lock-in | API-compatible services (Postgres, Kafka, Redis protocols) keep exit open | portable |

## Steps
1. List required features/extensions/config (e.g. Postgres extensions, Kafka configs, Redis modules) and check managed support.
2. Estimate 3-year TCO including people (on-call rotation size, upgrade projects).
3. Assess team expertise — self-managing a stateful distributed system without deep skills is the main risk.
4. Prefer managed for stateful systems unless a specific blocker exists; document the blocker in an ADR.
5. Keep exit options: protocol-compatible services, data export tested, IaC for both paths.

## Gotchas
- Managed ≠ maintenance-free: you still own sizing, schema, query performance, parameter groups, major version upgrades (scheduled by you, sometimes forced at end of support).
- Self-managed on Kubernetes with operators reduces toil but adds operator expertise needs.

## Verify
- [ ] ADR with TCO including people and the list of feature gaps checked.
