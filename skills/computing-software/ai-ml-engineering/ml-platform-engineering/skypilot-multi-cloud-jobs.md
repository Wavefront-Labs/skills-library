---
id: computing-software.ai-ml-engineering.ml-platform-engineering.skypilot-multi-cloud-jobs
name: skypilot-multi-cloud-jobs
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform-engineering, skypilot, multi-cloud, gpu-availability, spot-instances, managed-jobs]
level: practitioner
status: docs-checked
description: "Run training and serving across clouds with SkyPilot: task YAML, resource and region failover, managed spot jobs with auto-recovery, file mounts, clusters and SkyServe."
sources:
  - https://docs.skypilot.co/en/latest/docs/index.html
  - https://docs.skypilot.co/en/latest/examples/managed-jobs.html
  - https://docs.skypilot.co/en/latest/serving/sky-serve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SkyPilot multi-cloud jobs

**Problem solved:** GPUs are scarce and priced differently across clouds and regions. SkyPilot finds capacity, provisions it, runs your job and recovers from preemptions.

## Task YAML
```yaml
name: finetune-llm
resources:
  accelerators: {H100:8, A100-80GB:8}    # any of these, cheapest available first
  use_spot: true
  disk_size: 500
file_mounts:
  /data: s3://my-bucket/datasets/sft-v3
  /checkpoints:
    source: s3://my-bucket/ckpt/finetune-llm
    mode: MOUNT
workdir: .
setup: pip install -r requirements.txt
run: |
  torchrun --nproc_per_node=$SKYPILOT_NUM_GPUS_PER_NODE train.py \
    --data /data --output /checkpoints
```
```bash
sky launch -c dev task.yaml      # interactive cluster; sky down dev
sky jobs launch task.yaml        # managed job: auto-recovers from preemption
sky jobs queue; sky jobs logs <id>
```

## Managed spot jobs
On preemption, SkyPilot re-provisions (possibly another region/cloud) and reruns `run`. Your code must checkpoint to the mounted bucket and resume from the latest checkpoint.

## Cost and capacity
- Constrain placement for data gravity and compliance in the task's `resources`; look up the exact keys in the SkyPilot docs.
- Tear down idle clusters with `sky down`.
- Kubernetes clusters can be targets too, mixing on-prem and cloud.

## Serving
SkyServe (`sky serve up service.yaml`) runs replicas across regions/clouds with load balancing and autoscaling, e.g. vLLM endpoints on spot with on-demand fallback.

## Verify
- [ ] A spot interruption resumes from the last checkpoint.

## Checked
2026-11-01. Confirmed against the SkyPilot managed jobs and SkyServe pages: task YAML keys (accelerators, use_spot, disk_size, file_mounts MOUNT mode, workdir), sky launch, sky down, sky jobs launch/queue/logs/cancel, re-provisioning in another region, Kubernetes targets, on-demand fallback, SkyServe load balancing and autoscaling across regions/clouds. Removed: num_nodes, sky check, sky ssh, sky show-gpus, --cloud/--region, sky autostop, --resume flag.
Method: documentation only; no commands were run.
