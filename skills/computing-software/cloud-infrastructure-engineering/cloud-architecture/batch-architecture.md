---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.batch-architecture
name: batch-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, batch-architecture, hpc, aws-batch, azure-batch, job-scheduling]
level: practitioner
status: docs-checked
description: "Design batch and HPC architecture: pick a managed batch service or a scheduler-based cluster, classify parallel vs tightly coupled jobs, and record recovery and cost per job."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html", "https://learn.microsoft.com/azure/batch/batch-technical-overview", "https://cloud.google.com/batch/docs/get-started", "https://docs.aws.amazon.com/parallelcluster/latest/ug/what-is-aws-parallelcluster.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch and HPC architecture

## Classify the job
- **Intrinsically (embarrassingly) parallel**: instances run independently and do not communicate with each other, though they may read common data. Examples on the Azure page: Monte Carlo risk modelling, VFX and 3D rendering, image analysis, media transcoding, genetic sequence analysis, OCR, ETL, software test runs.
- **Tightly coupled**: applications communicate with each other, normally through MPI. Azure Batch can run them with Microsoft MPI or Intel MPI, on specialised HPC and GPU-optimised VM sizes. Examples: finite element analysis, fluid dynamics, multi-node AI training.

## Steps
1. **Choose the service.**
   - AWS Batch: a fully managed batch service that provisions compute in response to submitted jobs, running on Amazon ECS or EKS with EC2 (Spot or On-Demand), Fargate or ECS Managed Instances.
   - Azure Batch: Azure provides scheduling as a service over a pool of VMs; no scheduler software to manage. Azure CycleCloud fits when you need a specific scheduler, custom cluster topology or to keep existing on-premises scheduler workflows (you manage the scheduler; CycleCloud provisions and autoscales the infrastructure). Azure CycleCloud Workspace for Slurm is a Marketplace solution that deploys CycleCloud, Slurm, networking, storage and access components.
   - Google Cloud Batch: a fully managed service where a job is an array of tasks run as a sequence of runnables (scripts or containers) on a regional managed instance group of Compute Engine VMs; no third-party scheduler to run.
   - AWS ParallelCluster: open-source cluster management for HPC clusters with a scheduler and shared file system. From ParallelCluster 3.16.0, AWS Batch is no longer supported as its scheduler.
2. **Don't choose Batch only to avoid managing VMs.** On Azure, if scheduler compatibility is required, translating existing scheduler workflows into Batch pools, jobs and tasks can become an application redesign; choose CycleCloud or Workspace for Slurm instead.
3. **Size and cap**: Azure Batch pools can use Spot VMs or autoscale the node count as load changes. Google Cloud Batch requires staying within Batch quotas and limits, and supports only listed machine series; check the current list on its page.
4. **Data**: Azure's standard workflow uploads inputs and applications to Azure Storage, tasks download inputs to their node, and results are uploaded back to storage. Use the same shape elsewhere: inputs and outputs in object storage.
5. **Observability**: monitor job and task progress (query the Batch service efficiently when there are thousands of tasks) and record time and cost per representative job.
6. **Before production** (Azure guidance): record why Batch fits, which alternatives you rejected, the peak task and capacity estimate, the recovery behaviour for interrupted work, and benchmarked time and cost per representative job.

## Gotchas
- Batch services charge nothing extra on Azure and Google Cloud; you pay for the underlying resources. Leaving large clusters running between jobs still costs; scale down.
- Interrupted work needs a defined recovery behaviour (retry or checkpoint) before you rely on Spot capacity.

## Verify
- [ ] Interrupted tasks resume or re-run correctly in tests.
- [ ] Cost per job tracked.

## Checked
2026-11-08. Confirmed on the AWS Batch overview, Azure Batch technical overview (service comparison, parallel vs tightly coupled, workflow, pre-production checklist), Google Cloud Batch get-started page (components, MIG, restrictions, no extra charge) and the AWS ParallelCluster overview (3.16.0 note). Removed (not on these pages): EFA and InfiniBand HB/HC, Google Cluster Toolkit, Kubernetes Jobs with Kueue, FSx for Lustre, Azure Managed Lustre and Parallelstore, Step Functions, Airflow and Nextflow, placement groups, per-queue priority and max vCPU cap advice, and the object-prefix hot-spot gotcha.
Method: documentation only; no commands were run.
