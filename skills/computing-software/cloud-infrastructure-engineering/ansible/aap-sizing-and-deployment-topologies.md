---
id: computing-software.cloud-infrastructure-engineering.ansible.aap-sizing-and-deployment-topologies
name: aap-sizing-and-deployment-topologies
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-install, aap-topology, automation-mesh, capacity]
level: advanced
status: docs-checked
description: "Choose an Ansible Automation Platform topology (growth vs enterprise, containerized vs operator) and size controller, hub, EDA, gateway and database nodes."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/tested_deployment_models/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/planning_your_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AAP sizing and topologies

## Tested topologies (AAP 2.5)
| Topology | Shape | Use |
|---|---|---|
| Container growth | one VM: gateway, controller, hub, EDA, Postgres (podman) | labs, small teams, < few hundred hosts |
| Container enterprise | gateway x2, controller x2, hub x2, EDA x2, execution nodes, external DB, load balancer | production with HA |
| Operator growth/enterprise | OpenShift operators, external or managed DB | Kubernetes-native shops |
| RPM (setup.sh based) | existing RHEL VM estates | documented for 2.5; containerized/operator are the newer models |

Every topology needs a Postgres database (managed or external for enterprise) and, for HA, a load balancer in front of gateways.

## Sizing starting points
- Controller/hybrid node: 4 vCPU, 16 GB RAM in the tested models; capacity ≈ min(CPU forks, memory forks) where memory forks = (mem - 2048) / mem_per_fork (mem in MB; a 4 GB node runs ~20 forks) and CPU forks = cpus x fork_per_cpu (`SYSTEM_TASK_FORKS_MEM`/`SYSTEM_TASK_FORKS_CPU` overrides; fork_per_cpu defaults to 4).
- Execution nodes do the work: scale them horizontally per network zone (mesh) rather than growing control nodes.
- Database: fast SSD, IOPS matter; job events table grows fast — 100+ GB for busy installs; schedule cleanup.
- Hub: storage for collections and EE images (hundreds of GB with many images), or S3/Azure blob.

## Workload estimate
concurrent forks needed ≈ (hosts per run x runs in parallel) / runs' serial batching. Divide by per-node capacity → execution node count, plus headroom (N+1).

## Decisions to record
- Which networks need hop/execution nodes (mesh).
- External DB ownership and backup.
- Identity source (LDAP/SAML) at the gateway.
- Upgrade cadence (check the release notes for the current cadence).

## Gotchas
- Running jobs on control nodes in enterprise topologies starves the UI/API; keep control plane nodes `control` type.
- Job event volume, not host count, is the usual DB bottleneck: lower verbosity on chatty templates.

## Verify
- [ ] Instance capacity in the UI exceeds peak concurrent forks with one node failed.

## Checked

- 2026-10-31: growth vs enterprise topologies for containerized and operator deployment models,
control/execution/hop node sizing (16 GB / 4 vCPU class), load balancer in front of gateways,
PostgreSQL 15 requirement, the documented fork-capacity algorithm ((mem - 2048) / mem_per_fork,
cpus * fork_per_cpu, SYSTEM_TASK_FORKS_CPU/MEM with defaults) and managed-node licensing confirmed
in the AAP 2.5 tested deployment models, planning, and Using automation execution guides.
- Fixed: `SYSTEM_TASK_ABS_CPU` was not a real setting (the documented names are
  SYSTEM_TASK_FORKS_CPU/SYSTEM_TASK_FORKS_MEM); the RPM-deprecated-in-2.5 claim and the ~6-month
  release-cadence figure were removed (not documented).
Method: documentation only; no commands were run.
