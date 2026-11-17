---
id: computing-software.ai-ml-engineering.ml-platform-engineering.sagemaker-studio-and-vertex-ai-workbench
name: sagemaker-studio-and-vertex-ai-workbench
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, sagemaker-studio, vertex-workbench, notebooks, idle-shutdown, ml-dev-environment]
level: practitioner
status: draft
description: "Run managed notebook environments: SageMaker Studio domains, spaces and lifecycle configs, Vertex AI Workbench instances, idle shutdown, network isolation and per-user roles."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lcc.html
  - https://cloud.google.com/vertex-ai/docs/workbench/instances/introduction
  - https://cloud.google.com/vertex-ai/docs/workbench/instances/idle-shutdown
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SageMaker Studio and Vertex AI Workbench

**Goal:** data scientists get self-service notebooks with GPUs, while the platform team controls network access, permissions and cost.

## SageMaker Studio
- **Domain:** one per account/environment; VPC-only mode routes all traffic through your VPC (with VPC endpoints for S3, SageMaker API, STS, CloudWatch) - no direct internet.
- **User profiles** with their own execution roles (least privilege per team); IAM Identity Center for SSO.
- **Spaces:** JupyterLab and Code Editor apps with chosen instance type and EBS storage; private or shared spaces.
- **Lifecycle configurations:** scripts run on app start (install packages, configure git, set idle shutdown); attach per domain or user profile and enforce with `DefaultResourceSpec`.
- **Idle shutdown:** built-in idle timeout for JupyterLab/Code Editor apps - set it domain-wide; idle GPU notebooks are a top cost leak.
- Restrict instance types with IAM conditions (`sagemaker:InstanceTypes`) so a user cannot start a p5 for a notebook.

## Vertex AI Workbench
- Instances are managed Compute Engine VMs with JupyterLab; choose machine type and GPU; custom container images for standard environments.
- Access mode: service account vs single user; use per-user or per-team service accounts, not the default compute SA.
- Idle shutdown (`idle-timeout-seconds` metadata / console setting), post-startup scripts, scheduled notebook executions.
- Network: no public IP, Private Google Access, VPC Service Controls perimeter for data exfiltration protection.
- Colab Enterprise is the lighter managed notebook alternative.

## Platform guardrails (both)
- Data access through roles/service accounts scoped to project buckets; no long-lived keys in notebooks.
- Standard images with pinned framework versions; allow pip installs into user envs but promote reproducible work to pipelines.
- Tag/label resources by user and team; dashboard notebook spend.
- Encourage moving long training out of notebooks into training jobs (cheaper, reproducible, tracked).

## Verify
- [ ] Idle shutdown enforced and observed (instances stop after the timeout).
- [ ] Notebooks cannot reach the public internet where policy requires.
- [ ] Notebook spend per user visible.
