---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.big-compute
name: big-compute
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, big-compute, hpc, aws-batch, azure-batch, aws-parallelcluster, slurm, mpi]
level: practitioner
status: docs-checked
description: "Design big compute (HPC) workloads in cloud: embarrassingly parallel vs tightly coupled, Batch vs scheduler-based clusters, interconnect choice, burst-and-release capacity."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/big-compute", "https://docs.aws.amazon.com/parallelcluster/latest/ug/what-is-aws-parallelcluster.html", "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html", "https://docs.cloud.google.com/cluster-toolkit/docs/overview", "https://learn.microsoft.com/azure/cyclecloud/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Big compute

## Steps
1. **Classify the workload** (Azure Architecture Center, big compute): work is split into finite
   discrete tasks run across many cores at once. Tasks are either independent (embarrassingly
   parallel: rendering, Monte Carlo runs repeated hundreds or thousands of times) or tightly
   coupled (they exchange intermediate results). For tightly coupled work consider high-speed
   networking such as InfiniBand and RDMA.
2. **Pick the orchestration**:
   - Managed scheduling as a service: Azure Batch (VM pool, task assignment, autoscale, job
     scheduling) or AWS Batch (managed batch on ECS/EKS, scaling EC2, Fargate or ECS Managed
     Instances, Spot or On-Demand).
   - You operate a scheduler: Azure CycleCloud (provisions and autoscales Azure infrastructure for
     Slurm, PBSPro, LSF, Grid Engine, HTCondor; it is not itself a scheduler) or AWS ParallelCluster
     (open source cluster tool; Slurm scheduler; AWS Batch as scheduler is no longer supported from
     3.16.0). The ParallelCluster page recommends AWS Parallel Computing Service (managed Slurm).
     Google Cluster Toolkit deploys HPC/AI/ML clusters from YAML blueprints via the `gcluster`
     tool, generating Terraform and Packer; Slurm is its named scheduler.
   - Rule of thumb from the CycleCloud page: keep an existing scheduler's scripts and policies with
     CycleCloud; use Batch when the application can submit tasks via an API and has no scheduler
     dependency.
3. **Interconnect**: for tightly coupled tasks use an RDMA/InfiniBand network; Azure lists HBv5,
   HC and HX VM families as compute-intensive options. Check the provider's current docs for the
   equivalent instance families and placement options elsewhere.
4. **Capacity pattern**: provision a large number of cores in a burst then reduce to zero when the
   job ends. The system must handle node failures and application crashes.
5. **Hybrid**: HPC Pack can burst to Azure from an on-premises head node over ExpressRoute or VPN
   Gateway.
6. Before production, record why the service fits, rejected alternatives, scheduler compatibility
   test, topology, peak capacity and quota, storage benchmark, failure recovery approach, and time
   and cost per representative job (CycleCloud page).

## Gotchas
- For tightly coupled tasks adding cores has diminishing returns; experiment to find the optimum.
- Provisioning thousands of cores in a timely manner is a listed challenge; check quotas early.
- Changing scheduler on Cluster Toolkit means redeploying the cluster.

## Verify
- [ ] Scaling test shows efficiency at the target core count.
- [ ] A failed node or crashed task is handled without losing the whole run.

## Checked
Confirmed against the five cited pages (Azure big-compute style, CycleCloud overview, ParallelCluster
overview, AWS Batch overview, Cluster Toolkit overview). Removed as not stated there: EFA and
placement-group specifics, H3/C3 and compact placement, Lustre/Parallelstore storage options, spot
interruption advice, license-server note, Kueue/Volcano, Google Cloud Batch.
Method: docs-only read of cited pages, 2026-11-08
