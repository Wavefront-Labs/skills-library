---
id: computing-software.ai-ml-engineering.ollama.docker-run-cpu-nvidia-amd
name: docker-run-cpu-nvidia-amd
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [docker, nvidia-container-toolkit, rocm, jetson, dockerrun]
level: practitioner
status: docs-checked
description: "Run the ollama/ollama image on CPU, NVIDIA (--gpus=all) or AMD (ollama/ollama:rocm with /dev/kfd and /dev/dri)."
sources:
  - https://docs.ollama.com/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: containerise Ollama with GPU access.

CPU only:

```
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

NVIDIA: install the NVIDIA Container Toolkit (via apt or yum, per the page), then:

```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

For Jetson, set `JETSON_JETPACK=5` or `6` in the container environment.

AMD: use the ROCm tag and pass the devices:

```
docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:rocm
```

Vulkan support is bundled in the image. Turn it off with `OLLAMA_VULKAN=0` and pick devices with `GGML_VK_VISIBLE_DEVICES`.

Run a model inside the container:

```
docker exec -it ollama ollama run llama3.2
```

Docker Desktop for macOS has no GPU passthrough. If a container falls back to CPU after some time, the troubleshooting page attributes one cause to the cgroup driver; set `"exec-opts": ["native.cgroupdriver=cgroupfs"]` in `/etc/docker/daemon.json` and restart Docker.

Logs: `docker logs ollama`.

## Checked

2026-11-03. CPU, NVIDIA (`nvidia-ctk`, `--gpus=all`), Jetson, ROCm and Vulkan commands against the Docker page; macOS GPU limit against the FAQ (docs.ollama.com/faq); cgroup driver fix against the troubleshooting page (docs.ollama.com/troubleshooting). Nothing removed.

Method: documentation only; no commands were run.
