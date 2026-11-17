---
id: computing-software.ai-ml-engineering.mlflow.mlproject-docker-environments
name: mlproject-docker-environments
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-projects, mlproject-docker, docker-env, containerized-training, kubernetes-backend]
level: practitioner
status: docs-checked
description: "Use docker_env in MLflow Projects: base images, volumes and environment passthrough, how MLflow layers project code into an image, and the Kubernetes backend."
sources:
  - https://mlflow.org/docs/latest/ml/projects/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/docker.py
  - https://github.com/mlflow/mlflow/blob/master/mlflow/cli/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker environments for MLflow Projects

**Goal:** run projects in a container with system libraries and CUDA that a Python environment file can't describe.

## MLproject with docker_env
```yaml
name: vision-train
docker_env:
  image: registry.example.com/ml/pytorch-cuda:2.3-cu121     # your base image with deps installed
  volumes: ["/data/imagenet:/data/imagenet:ro"]
  environment: [["NCCL_DEBUG", "WARN"], "AWS_PROFILE"]       # set a value, or pass through from host
entry_points:
  main:
    parameters: {epochs: {type: int, default: 10}}
    command: "python train.py --epochs {epochs}"
```
```bash
mlflow run . -P epochs=20 --build-image          # --build-image: build/tag a new image containing the project
mlflow run . -A gpus=all                          # -A passes docker run args (e.g. GPU access)
```
- With `--build-image`, MLflow creates an image `FROM` the base image named in `docker_env.image`, copies the project directory in, and runs the entry point inside it. Without it the base image is used as is, so it must already contain everything the entry point needs.
- The tracking URI is passed into the container; for a local `file:` store, MLflow mounts it, but a remote tracking server (`MLFLOW_TRACKING_URI=http://...`) is far less fragile.
- Credentials: pass environment variables through (`"AWS_PROFILE"` form) or mount config read-only; never bake secrets into the image.

## Kubernetes backend
```bash
mlflow run . --backend kubernetes --backend-config kubernetes_config.json
```
`kubernetes_config.json`: `kube-context`, `repository-uri` (registry to push the built image), `kube-job-template-path` (a Job YAML whose name, container name, image and command MLflow overwrites). MLflow builds, pushes, and creates the Job; the run tracks the Job.

## Gotchas
- GPU access is requested with `-A gpus=all` (`-A name=value` passes a `docker run` argument).
- Image builds per run can be slow; pre-bake dependencies in the base image so the added layer is just code.
- Pin the base image by digest for reproducibility.

## Verify
- [ ] `mlflow run` inside Docker logs to the remote tracking server.
- [ ] Base image pinned by digest and recorded in run tags/params.
- [ ] GPU visible inside the container (`torch.cuda.is_available()` logged).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `docker_env` keys `image`, `volumes`, `environment` (a `[name, value]` pair or a bare name copied from the host): docs/classic-ml/projects/index.mdx.
- `--build-image` (only for Docker projects) and `-A name=value`/`--docker-args` (for example `-A gpus=all`): mlflow/cli/__init__.py.
- Image build (`FROM` base image, `COPY` of the project archive), tracking-URI passing and local-store mount: mlflow/projects/docker.py. Kubernetes config keys and Job overwrite behaviour: mlflow/projects/kubernetes.py.
- Removed as unconfirmed: the NVIDIA container toolkit statement and the requirement that the base image already holds MLflow.

Method: documentation only; no commands were run.
