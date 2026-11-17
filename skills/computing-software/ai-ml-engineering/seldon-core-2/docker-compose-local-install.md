---
id: computing-software.ai-ml-engineering.seldon-core-2.docker-compose-local-install
name: docker-compose-local-install
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, installation, docker-compose, make-deploy-local, local-model-folder, gpu-enabled, custom-image-tag, jaeger, grafana, local-install]
level: intro
status: docs-checked
description: "Run Seldon Core 2 locally with Docker Compose: make deploy-local, CUSTOM_IMAGE_TAG, GPU_ENABLED, mounting LOCAL_MODEL_FOLDER at /mnt/models, and local Jaeger and Grafana ports."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/docker-installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Compose local install

## Prepare
Clone `github.com/SeldonIO/seldon-core` at branch `v2`, build the Seldon CLI, install Docker Compose and install `make` (on Ubuntu, `sudo apt-get install build-essential`).

## Deploy and remove
From the project root run `make deploy-local`; it uses `latest` images. Triton and MLServer images are large (11G and 9G), so the first run takes time to download. Remove everything with `make undeploy-local`.

To run a release instead of latest, set `CUSTOM_IMAGE_TAG` first:
```sh
export CUSTOM_IMAGE_TAG=0.2.0
make deploy-local
```

## GPU
Install `nvidia-container-runtime`, then `export GPU_ENABLED=1`.

## Local models
Set `LOCAL_MODEL_FOLDER` to a folder on your machine; it is mounted at `/mnt/models` in the containers.
```sh
export LOCAL_MODEL_FOLDER=/path/to/models
make deploy-local
```
Then reference models with a local `storageUri`, for example `/mnt/models/iris` for a model stored in `iris` under that folder:
```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: iris
spec:
  storageUri: "/mnt/models/iris"
  requirements:
  - sklearn
```

## Observability
The default local install provides Jaeger tracing at `http://0.0.0.0:16686/search` and Grafana at `http://localhost:3000`.

## Checked

2026-11-04. Confirmed against getting-started/docker-installation.md (Seldon Core 2 docs, v2 branch): make targets, image sizes, CUSTOM_IMAGE_TAG, GPU_ENABLED, /mnt/models, Jaeger and Grafana URLs. Removed or corrected: nothing.

Method: documentation only; no commands were run.
