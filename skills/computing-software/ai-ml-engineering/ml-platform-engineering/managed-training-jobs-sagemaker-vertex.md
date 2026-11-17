---
id: computing-software.ai-ml-engineering.ml-platform-engineering.managed-training-jobs-sagemaker-vertex
name: managed-training-jobs-sagemaker-vertex
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, sagemaker-training-jobs, vertex-custom-training, managed-training, spot-training, checkpointing, distributed-training]
level: practitioner
status: draft
description: "Run training on SageMaker training jobs and Vertex AI custom jobs: entry points, data channels and env vars, distributed config, checkpoint paths, spot capacity and outputs."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html
  - https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html
  - https://cloud.google.com/vertex-ai/docs/training/create-custom-job
  - https://cloud.google.com/vertex-ai/docs/training/code-requirements
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed training jobs: SageMaker and Vertex AI

**Goal:** run training scripts on managed, ephemeral clusters with the platform handling provisioning, logs and artifact upload.

## SageMaker
```python
from sagemaker.pytorch import PyTorch
est = PyTorch(
    entry_point="train.py", source_dir="src", role=role,
    framework_version="2.3", py_version="py311",
    instance_type="ml.g5.12xlarge", instance_count=2,
    distribution={"torch_distributed": {"enabled": True}},          # torchrun across instances
    hyperparameters={"epochs": 3, "lr": 3e-4},
    use_spot_instances=True, max_run=36000, max_wait=72000,
    checkpoint_s3_uri="s3://ml/ckpt/llm-ft/", checkpoint_local_path="/opt/ml/checkpoints",
)
est.fit({"train": "s3://ml/data/train/", "val": "s3://ml/data/val/"})
```
Inside the container:
- Data channels at `/opt/ml/input/data/<channel>` (`SM_CHANNEL_TRAIN`); input modes File (copy first), FastFile (stream on demand), Pipe.
- Save the model to `/opt/ml/model` (`SM_MODEL_DIR`) - uploaded as `model.tar.gz` at the end.
- Hyperparameters arrive as CLI args.
- Spot: anything in `/opt/ml/checkpoints` syncs to `checkpoint_s3_uri`; on interruption the job restarts and your script must resume from there.

## Vertex AI
```python
from google.cloud import aiplatform
job = aiplatform.CustomJob.from_local_script(
    display_name="llm-ft", script_path="train.py",
    container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.2-3.py310:latest",
    requirements=["transformers", "datasets"], args=["--epochs=3"],
    machine_type="a2-highgpu-1g", accelerator_type="NVIDIA_TESLA_A100", accelerator_count=1,
    replica_count=1, staging_bucket="gs://ml-staging",
)
job.run()
```
- Env vars: `AIP_MODEL_DIR` (write the model there), `AIP_CHECKPOINT_DIR`, `AIP_TENSORBOARD_LOG_DIR`; multi-replica jobs get `CLUSTER_SPEC`.
- GCS is mounted via Cloud Storage FUSE at `/gcs/<bucket>/` - read data with file paths.
- Use custom containers for full control; worker pool specs for multi-node (chief + workers).

## Common practice
- Same container image locally and in the job; test with a tiny dataset locally (SageMaker local mode or docker run).
- Log metrics to the experiment tracker (MLflow/W&B) plus the platform's metrics.
- Tag jobs with team/project for cost attribution.

## Verify
- [ ] Spot interruption simulated: job resumes from the last checkpoint.
- [ ] Model artifact lands in the expected location and loads.
- [ ] Multi-instance job shows all ranks participating.
