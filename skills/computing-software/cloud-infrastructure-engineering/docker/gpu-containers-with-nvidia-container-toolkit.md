---
id: computing-software.cloud-infrastructure-engineering.docker.gpu-containers-with-nvidia-container-toolkit
name: gpu-containers-with-nvidia-container-toolkit
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, gpus-flag, nvidia-container-toolkit, gpu, cuda, cdi, resource-limits]
level: advanced
description: "Give containers NVIDIA GPUs: install the NVIDIA Container Toolkit, configure the runtime or CDI, use --gpus and Compose device reservations, and match CUDA to the driver."
sources: ["https://docs.docker.com/engine/containers/gpu/", "https://docs.docker.com/reference/cli/docker/container/run/#gpus", "https://docs.docker.com/compose/how-tos/gpu-support/", "https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GPU containers with the NVIDIA Container Toolkit

## Host setup
1. NVIDIA driver on the host (`nvidia-smi` works). The driver is **not** in the image.
2. NVIDIA Container Toolkit: Docker's GPU page tells you to follow NVIDIA's own installation guide (https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html); repository setup, `nvidia-ctk runtime configure` and rootless settings change between toolkit releases, so use that guide rather than copying commands from here. NVIDIA GPUs can only be accessed by systems running a single engine.

## Running
```sh
docker run -it --rm --gpus all ubuntu nvidia-smi
docker run --gpus device=0 ...                          # one GPU by index
docker run --gpus '"device=0,2"' ...                    # several (the value must be quoted because of the comma)
docker run --gpus device=<GPU-UUID> ...                 # by UUID, from nvidia-smi -L
docker run --gpus 'all,capabilities=utility' ...        # set driver capabilities
```
CDI (Container Device Interface) alternative: a GPU can also be requested as a CDI device with `--device`, for example `docker run --device nvidia.com/gpu=all ...`. CDI is enabled by default for Linux containers; the daemon reads CDI specs from `/etc/cdi/` (static) and `/var/run/cdi` (generated), configurable with `cdi-spec-dirs`. Generate the spec as NVIDIA's guide describes.

## Compose
```yaml
services:
  trainer:
    image: registry.example.com/trainer:1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1              # or device_ids: ["0"]; count and device_ids are mutually exclusive
              capabilities: [gpu]
```

## CUDA vs driver compatibility
The image's CUDA runtime must be supported by the host driver; the `nvidia-smi` header shows the CUDA version the driver reports. Capabilities can be set through environment variables in images, and the official CUDA images set them for you (see the NVIDIA toolkit and NGC catalog pages for tags).

## Gotchas
- `--gpus` needs the NVIDIA toolkit installed first.
- Docker's resource-constraint options do not describe a GPU memory limit; check NVIDIA's documentation for MIG or other partitioning.
- Environment variables set in the image can also configure NVIDIA capabilities; see the toolkit documentation.

## Verify
`docker run --rm --gpus all ubuntu nvidia-smi -L` lists the expected GPUs (with the `utility` capability, `all,capabilities=utility`, if the tool is missing).

## Checked

Checked against docker/docs `engine/containers/gpu.md`, the `docker container run` reference (`--gpus`, CDI devices), `reference/cli/dockerd` (CDI spec directories) and `compose/how-tos/gpu-support.md` (docker/docs latest commit 2026-10-23, Engine 29).

- `--gpus` forms (`all`, `device=0`, UUID, quoted `"device=0,2"`), `capabilities=utility`, CDI via `--device`, CDI default-on and spec directories, Compose `deploy.resources.reservations.devices` keys (`driver`, `count`, `device_ids`, `capabilities` required, `count` and `device_ids` exclusive).
- Removed as unconfirmed: the NVIDIA apt repository and `nvidia-ctk` command lines (deferred to NVIDIA's guide), the rootless `no-cgroups` setting, pinned CUDA image tags, the error message texts, MIG advice and the `docker info` runtimes check.

Method: documentation only; no commands were run.
