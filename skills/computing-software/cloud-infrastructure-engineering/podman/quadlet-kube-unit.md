---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-kube-unit
name: quadlet-kube-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, kube-unit, kubernetes-yaml, kube-play, configmap, exitcodepropagation, setworkingdirectory]
level: advanced
status: docs-checked
description: "Run Kubernetes YAML as a service with a Quadlet .kube: required Yaml key, ConfigMap, PublishPort merging, ExitCodePropagation, SetWorkingDirectory and KubeDownForce."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage podman kube play as a systemd service.

A `.kube` file's `[Kube]` section produces `ExecStart=podman kube play ... file.yml`. The only required key is `Yaml=`, the path to the YAML (absolute or relative to the unit file); it can be repeated.

Keys: `ConfigMap=` passes a ConfigMap YAML path (a single path, absolute or relative to the unit file; repeatable). `Network=` follows `podman kube play --network`; a name ending `.network` uses `systemd-$name` and depends on `$name-network.service`. `PublishPort=` is merged with ports in the YAML; if the same container port and protocol appear in both, the unit file wins. `LogDriver`, `UserNS`, `GlobalArgs` and `PodmanArgs` (placed right before the YAML path) are available. `KubeDownForce=` is `--force` for `podman kube down`, removing all resources including volumes.

`ExitCodePropagation=` controls the service exit: `all` exits non-zero if all containers failed, `any` if any failed, `none` (current default) exits zero and ignores failures.

`SetWorkingDirectory=` takes `yaml` or `unit` so relative paths resolve; with multiple `Yaml` paths only `unit` is supported, and an explicit `WorkingDirectory` in `[Service]` is never overridden. `AutoUpdate=` accepts `registry`, `local` and `name/(local|registry)`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
