---
id: computing-software.cloud-infrastructure-engineering.aws.aws-batch-gpu-jobs-and-resource-requirements
name: aws-batch-gpu-jobs-and-resource-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-batch, batch-gpu, resource-requirements, gpu-instances, multi-node-parallel]
level: advanced
status: docs-checked
description: "Run GPU workloads on AWS Batch: GPU compute environments and AMIs, resourceRequirements for GPU, vCPU and memory, and fixing GPU jobs stuck in RUNNABLE."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html", "https://docs.aws.amazon.com/batch/latest/APIReference/API_ResourceRequirement.html", "https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU jobs and resource requirements on AWS Batch

## 1. Compute environment
```bash
aws batch create-compute-environment --compute-environment-name gpu-ce --type MANAGED \
  --compute-resources 'type=EC2,allocationStrategy=BEST_FIT_PROGRESSIVE,minvCpus=0,maxvCpus=256,
    instanceTypes=[g5.xlarge,g5.2xlarge,g6.xlarge],subnets=[subnet-a],securityGroupIds=[sg-batch],
    instanceRole=ecsInstanceRole'
```
- All instance types in a compute environment that runs GPU jobs must come from the p3, p4, p5, p6, g3,
  g3s, g4, g5, g6, gr6, g7 or g7e families (per the GPU jobs page); otherwise GPU jobs may not schedule.
- For GPU scheduling Batch supports only instance types with NVIDIA GPUs (for example G4ad is not supported).
  ARM64 GPU types such as G5g need a custom AMI or launch-template user data.
- GPUs are not available for jobs running on Fargate.

## 2. Job definition
```bash
aws batch register-job-definition --job-definition-name train --type container \
  --container-properties '{"image":"<IMAGE>","command":["python","train.py"],
    "resourceRequirements":[{"type":"GPU","value":"1"},{"type":"VCPU","value":"4"},{"type":"MEMORY","value":"15000"}]}'
```
- Use `resourceRequirements` (types `GPU`, `VCPU`, `MEMORY`), not the deprecated `vcpus`/`memory` fields.
- For EC2 resources at least one vCPU must be specified. Each vCPU equals 1,024 CPU shares.
- Memory must fit on the instance after system overhead; see "Compute resource memory management" in the Batch user guide before choosing the value.

## 3. Multi-node parallel (distributed training)
`--type multinode` uses `nodeProperties`; see the multi-node parallel jobs documentation for the node definitions.

## 4. Stuck in RUNNABLE
- Requested GPU/vCPU/memory larger than any allowed instance type.
- The account's EC2 vCPU quota for the GPU instance families is too low (see Service Quotas).
- `describe-compute-environments` status `INVALID`.

## Verify
- [ ] Job log shows `nvidia-smi` output with the expected GPU count.

## Checked

2026-10-28. Confirmed against the Batch GPU jobs page, the ResourceRequirement API reference and the batch botocore model: supported GPU instance families, NVIDIA-only GPU scheduling, G4ad exception, ARM64 custom AMI note, no GPUs on Fargate, resource requirement types GPU/VCPU/MEMORY, deprecated vcpus/memory, one-vCPU minimum on EC2 and 1,024 CPU shares per vCPU. Removed (unconfirmed): ec2Configuration image type and AMI claim, NVIDIA_VISIBLE_DEVICES behaviour, the 15,000 MiB figure, multi-node placement group/EFA details, specific quota name and capacity advice. Read end to end.

Method: documentation only; no commands were run.
