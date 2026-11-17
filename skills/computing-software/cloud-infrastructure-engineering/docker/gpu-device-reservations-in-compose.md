---
id: computing-software.cloud-infrastructure-engineering.docker.gpu-device-reservations-in-compose
name: gpu-device-reservations-in-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-gpu, device-reservations, gpus-flag, nvidia-container-toolkit, deploy-resources, compose-production]
level: practitioner
status: docs-checked
description: "Give Compose services GPUs: deploy.resources.reservations.devices with driver, count or device_ids and capabilities, the gpus shorthand, toolkit prerequisites and checks."
sources: ["https://docs.docker.com/compose/how-tos/gpu-support/", "https://docs.docker.com/reference/compose-file/deploy/#devices", "https://docs.docker.com/reference/compose-file/services/#gpus", "https://docs.docker.com/engine/containers/gpu/", "https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU device reservations in Compose

## Prerequisite
Install the NVIDIA driver on the host and the NVIDIA Container Toolkit following NVIDIA's
install guide (Docker's GPU page links to it and does not repeat the steps); follow that
guide for configuring Docker's runtime. Docker's GPU page shows a test with
`docker run -it --rm --gpus all ubuntu nvidia-smi`.

## Compose syntax
```yaml
services:
  trainer:
    image: nvidia/cuda:12.9.0-base-ubuntu22.04
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1                 # or "all"
              capabilities: [gpu]
  inference:
    image: nvidia/cuda:12.9.0-base-ubuntu22.04
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ["0", "3"]   # specific GPUs
              capabilities: [gpu]
```
- `capabilities` is the only required field (a list of strings); omitting it returns an
  error on service deployment. The generic capabilities recognised today are `gpu` and
  `tpu`; driver-specific ones must be prefixed with the driver name (for example
  `nvidia-compute`).
- `count` (an integer or `all`) and `device_ids` (a list of strings) are mutually exclusive;
  Compose returns an error if both are set.
- If `count` is `all` or not specified, Compose reserves all devices that satisfy the
  requested capabilities. Docker's GPU guide says device IDs can be found in the output of
  `nvidia-smi` on the host.
- `driver` is a string such as `nvidia`; `options` holds driver-specific key-value pairs.
- An error is returned if you use an invalid device ID or a `count` higher than the number of
  GPUs in the system.

Compose 2.30.0 and later also accept a service-level shorthand, equivalent to a device
request with an implicit `gpu` capability:
```yaml
services:
  trainer:
    gpus: all
```
The long form takes `driver` and `count` (and other device fields).

## Verify
```bash
docker compose up trainer                     # runs nvidia-smi from the example above
docker compose exec trainer nvidia-smi -L     # for a service that stays running
```

## Gotchas
- NVIDIA's `--gpus` flag can select GPUs by index or UUID (`nvidia-smi -L` lists UUIDs).
- Docker's GPU page notes that NVIDIA GPUs can only be accessed by systems running a single
  engine.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose GPU how-to, Deploy reference (`devices`: `capabilities`, `driver`,
`count`, `device_ids`, `options`, exclusivity, generic capability names), services `gpus`
reference and its 2.30.0 feature banner, and Docker's GPU page (`--gpus` examples, single
engine note, link to the NVIDIA install guide). Removed: the `nvidia-ctk` command and
restart advice, the specific CUDA image tag from the old test command, the
`NVIDIA_DRIVER_CAPABILITIES` mapping, MIG sharing remarks, the exact error text, and the
Docker Desktop and Swarm generic-resources remarks.
