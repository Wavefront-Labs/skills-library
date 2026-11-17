---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-trainer-overview
name: kubeflow-trainer-overview
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [trainer, trainjob, training-runtimes, llm-fine-tuning, kueue]
level: intro
status: docs-checked
description: "Kubeflow Trainer: Kubernetes-native distributed training and LLM fine-tuning with TrainJob and Runtimes, MPI, data caching, Kueue, JobSet and LeaderWorkerSet."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/trainer/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trainer overview

Kubeflow Trainer is a Kubernetes-native distributed AI platform for scalable LLM fine-tuning and training across frameworks including PyTorch, MLX, HuggingFace, DeepSpeed, JAX and XGBoost. Training Operator V1 users are pointed to a migration document and legacy V1 guides.

Capabilities stated in the documentation:
- **MPI on Kubernetes**: orchestrates multi-node, multi-GPU jobs on HPC-style clusters for high-throughput inter-process communication.
- **Ecosystem integration**: Kueue for topology-aware scheduling and multi-cluster dispatch; JobSet and LeaderWorkerSet for workload orchestration; Coscheduling, Volcano and YuniKorn for coordinated scheduling.
- **Distributed data cache**: built on Apache Arrow and Apache DataFusion, it streams tensors with zero-copy transfer to GPU nodes so preprocessing and I/O run on CPU while GPUs train.
- **LLM fine-tuning blueprints** for fine-tuning and deployment.
- **Python SDK**: AI practitioners use the Kubeflow Python SDK with the two core APIs, `TrainJob` and Runtimes.

Documentation is split by persona on the Trainer site: AI Practitioners (user guides), Platform Administrators (operator guides, managing training runtimes) and Contributors.

## Checked

Confirmed the framework list, MPI, Kueue, JobSet, LeaderWorkerSet, Coscheduling, Volcano and YuniKorn integrations, the Arrow and DataFusion data cache, the SDK and personas. Removed the supersedes wording and the Katib and Pipelines integration sentence because the page does not state them.

Method: docs-checked 2026-11-09 against the raw kubeflow/website trainer overview.md page, read in full.
