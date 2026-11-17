---
id: computing-software.data-engineering.apache-hadoop.yarn-gpu-scheduling
name: yarn-gpu-scheduling
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, gpu, nvidia, resource-plugins, scheduling]
level: advanced
status: docs-checked
description: "Scheduling GPUs on YARN: yarn.io/gpu resource type, the NodeManager GPU plugin and device keys, DominantResourceCalculator, cgroups and Docker settings, and a submit example."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/UsingGpus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPUs on YARN

Prerequisites per the page: only NVIDIA GPUs are supported; NodeManagers need the NVIDIA drivers pre-installed; with Docker, nvidia-docker 1.0 is the version currently supported by YARN.

Scheduling: in resource-types.xml set `yarn.resource-types` = `yarn.io/gpu`. `DominantResourceCalculator` MUST be configured; for Capacity Scheduler set `yarn.scheduler.capacity.resource-calculator` = `org.apache.hadoop.yarn.util.resource.DominantResourceCalculator` in capacity-scheduler.xml.

Isolation, yarn-site.xml:
- `yarn.nodemanager.resource-plugins` = `yarn.io/gpu` enables the NodeManager isolation module. With only this, YARN detects and configures GPUs automatically; the keys below are for specialised needs.
- `yarn.nodemanager.resource-plugins.gpu.allowed-gpu-devices`: default `auto`; to specify manually use `index:minor_number[,...]`, e.g. `0:0,1:1,2:2,3:4`, with minor numbers found via `nvidia-smi -q` ("Minor Number").
- `yarn.nodemanager.resource-plugins.gpu.path-to-discovery-executables`: absolute path to nvidia-smi (only supported discovery binary), e.g. `/usr/local/bin/nvidia-smi`; empty (default) means the NodeManager locates it.
- Docker: `...gpu.docker-plugin` default `nvidia-docker-v1` (`nvidia-docker-v2` available); `...nvidia-docker-v1.endpoint` default `http://localhost:3476/v1.0/docker/cli`. Not needed with default nvidia-docker installation.
- `yarn.nodemanager.linux-container-executor.cgroups.mount` = true so the cgroup devices controller is mounted automatically; otherwise create the devices subfolder manually.

container-executor.cfg: `[gpu]` `module.enabled=true`. Without Docker also `[cgroups]` with `root=/sys/fs/cgroup` (same as the yarn-site cgroups mount-path) and `yarn-hierarchy=yarn` (same as the cgroups hierarchy).

With Docker, in `[docker]`: `docker.allowed.devices` (output of `ls /dev/nvidia*`), add `nvidia-docker` to `docker.allowed.volume-drivers`, add `nvidia_driver_<version>` (e.g. nvidia_driver_375.66) to `docker.allowed.ro-mounts`, and with nvidia-docker-v2 add `nvidia` to `docker.allowed.runtimes`.

Distributed shell supports extra resource types. Without Docker (2 containers of 3 GB, 1 vcore, 2 GPUs):

```
yarn jar <path/to/hadoop-yarn-applications-distributedshell.jar> \
  -jar <path/to/hadoop-yarn-applications-distributedshell.jar> \
  -shell_command /usr/local/nvidia/bin/nvidia-smi \
  -container_resources memory-mb=3072,vcores=1,yarn.io/gpu=2 \
  -num_containers 2
```

With Docker, add `-shell_env YARN_CONTAINER_RUNTIME_TYPE=docker` and `-shell_env YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=<docker-image-name>` (both required) and use `nvidia-smi` as the command. The page shows nvidia-smi output with two GPUs for the non-Docker run.

## Checked

Method: 2026-11-08, read the project's UsingGpus markdown source in full against this skill. Added prerequisites and Docker plugin keys; clarified that the device and discovery keys are optional; changed the "verify" line to what the page shows (sample nvidia-smi output). Submit command and keys were unchanged. Note: the page's cgroups root/hierarchy comments are the source for the "same as yarn-site" wording.
