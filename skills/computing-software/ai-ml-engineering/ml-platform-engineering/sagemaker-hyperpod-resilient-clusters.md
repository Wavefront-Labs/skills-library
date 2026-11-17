---
id: computing-software.ai-ml-engineering.ml-platform-engineering.sagemaker-hyperpod-resilient-clusters
name: sagemaker-hyperpod-resilient-clusters
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, sagemaker-hyperpod, resilient-training, slurm, eks, auto-resume]
level: practitioner
status: draft
description: "Operate SageMaker HyperPod clusters for long training runs: Slurm or EKS orchestration, lifecycle scripts, health checks, automatic node replacement and job auto-resume."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-resiliency-slurm.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SageMaker HyperPod resilient clusters

**Goal:** weeks-long distributed training survives hardware failures with minimal lost time and little manual intervention.

## Orchestrator choice
- **Slurm:** familiar HPC workflow (`sbatch`, `srun`), controller + login + compute instance groups configured by lifecycle scripts.
- **Amazon EKS:** Kubernetes-native (PyTorchJob, JobSet, Kueue), shares tooling with inference platforms; HyperPod adds health monitoring and node replacement under EKS.

## Create (Slurm example)
`create_cluster` with instance groups (e.g. `controller-machine` ml.m5.xlarge, `worker-group` ml.p5.48xlarge x N) and a `LifeCycleConfig` pointing to S3 scripts (`on_create.sh`) that install Slurm config, mount FSx for Lustre, set up users and observability. Version-control the lifecycle scripts; failures there are the commonest cluster-creation issue (check CloudWatch logs for the cluster).

## Resilience features
- Health monitoring agent checks GPUs, EFA and accelerators continuously; deep health checks (stress, NCCL tests) can run before nodes join.
- Faulty nodes are rebooted or replaced automatically with healthy capacity.
- **Auto-resume (Slurm):** `srun --auto-resume=1 python train.py ...` - when a node fails, HyperPod replaces it and restarts the job step from the latest checkpoint. The training code must checkpoint regularly and resume from the latest checkpoint on start.
- EKS: the HyperPod training operator / job auto-resume restarts affected jobs after node replacement.

## Checkpoint strategy
Lost time per failure = time since last checkpoint + restart time. With failures every few days on large clusters, checkpoint every 15-60 minutes, write asynchronously to local NVMe/FSx, and test resume regularly (deliberately kill a job).

## Capacity and cost
Use reserved capacity (flexible training plans / reserved instances) for large GPU counts; keep a few spare nodes in the instance group if your plan allows so replacements do not wait on capacity. Task governance (EKS) shares the cluster across teams with quotas and priorities.

## Observability
Integrate Amazon Managed Prometheus/Grafana or CloudWatch: GPU (DCGM), EFA, FSx metrics, and job throughput (tokens/s); alert on throughput drops, which reveal stragglers before outright failures.

## Verify
- [ ] Simulated node failure: node replaced and job resumed from checkpoint automatically.
- [ ] Lifecycle scripts reproducible from git; cluster recreatable.
