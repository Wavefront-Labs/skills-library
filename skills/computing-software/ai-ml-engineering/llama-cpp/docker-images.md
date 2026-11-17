---
id: computing-software.ai-ml-engineering.llama-cpp.docker-images
name: docker-images
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, docker, ghcr, container-images, devops]
level: intro
status: docs-checked
description: "Pick the right prebuilt llama.cpp Docker image tag and run it with a mounted model directory."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker images

Images are published at `ghcr.io/ggml-org/llama.cpp`. Three kinds of tag:

- `full`: includes `llama-cli`, `llama-completion` and the tools to convert models to ggml and quantize them to 4-bit.
- `light`: only the `llama-cli` and `llama-completion` executables.
- `server`: only the llama-server executable.

Accelerator variants add a suffix, for example `server-cuda`, `server-cuda13`, `server-rocm`, `server-musa`, `server-intel`, `server-vulkan`, `server-openvino` (and `-s390x` images for IBM Z).

Examples:

```bash
docker run -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:full --run -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512
docker run -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:server -m /models/7B/ggml-model-q4_0.gguf --port 8080 --host 0.0.0.0 -n 512
```

The `full` image entrypoint accepts `--all-in-one` (download, convert and quantize), `--run` (CLI), `--run-legacy`, plus the convert and quantize modes.

GPU: the page's CUDA examples use locally built images with `docker run --gpus all ...` and `--n-gpu-layers`; the nvidia-container-toolkit must be installed on Linux. The published GPU images are only built by CI, not tested; for a different CUDA, ROCm or MUSA library, build locally.

Build locally:

```bash
docker build -t local/llama.cpp:server-cuda --target server -f .devops/cuda.Dockerfile .
```

The CUDA Dockerfile takes `CUDA_VERSION` (default 12.8.1) and `CUDA_DOCKER_ARCH` (default: the cmake build default, all supported architectures) as build arguments.

## Checked

2026-11-04: confirmed against the llama.cpp `docs/docker.md` page: image kinds and contents, accelerator variants, `--all-in-one`, `--run`, `--run-legacy`, build command and CUDA build arguments, CI-testing note. Fixed the full/light contents and the `--gpus` guidance.
Method: documentation only; no commands were run.
