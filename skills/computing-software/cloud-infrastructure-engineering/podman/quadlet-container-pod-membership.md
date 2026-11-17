---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-pod-membership
name: quadlet-container-pod-membership
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, pod, startwithpod, cgroupsmode, no-conmon, pod-membership, container-unit]
level: advanced
status: docs-checked
description: "Put a Quadlet container into a pod with Pod=name.pod, how StartWithPod behaves, and why to change CgroupsMode for pod-level resource limits."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: attach a container to a Quadlet pod correctly.

`Pod=` links the container to a Quadlet `.pod` unit. The value must be `<name>.pod` and the `.pod` unit must exist. Quadlet adds all the parameters needed to link the container and pod and their services.

`StartWithPod=` (default true) starts the container after the associated pod is created. When true, the container starts, stops and restarts with the pod. When false, it is not started when the pod starts but is stopped with it; restarting the pod also restarts the container if it was running before. It can still be started manually or via a target with an `[Install]` section, and the pod starts as needed.

`CgroupsMode=` maps to `--cgroups`. Quadlet's default is `split`, which differs from the CLI default `enabled`. If the container joins a pod, you may want `no-conmon` or `enabled` so pod-level cgroup resource limits can take effect.

Quadlet supplies the parameters that link container and pod, so no manual `--pod` flag is written in the unit.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
