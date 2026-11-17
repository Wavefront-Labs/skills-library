---
id: computing-software.cybersecurity-defensive.falco.missing-container-fields
name: missing-container-fields
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [missing-fields, container-plugin, cri-sockets, host-root, containerd]
level: practitioner
status: docs-checked
description: "Fix missing container or Kubernetes fields: mount the runtime socket, load the container plugin and use the CRI engine for containerd."
sources:
  - https://falco.org/docs/troubleshooting/missing-fields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco derives many fields from several events. For each spawned process it extracts and derives fields from `clone*`, `fork` and `execve*` syscalls and stores them in a userspace struct, so null values can occur. Some absences are legitimate: shell built-ins like `echo` do not spawn a process and are not logged.

Missing container image or name checklist:
- Is the container runtime socket mounted? On Kubernetes mount it with the `HOST_ROOT` prefix, for example `/host/run/k3s/containerd/containerd.sock`.
- Is the `container` plugin loaded? It must be in `load_plugins` and configured under `plugins`.
- For a custom runtime socket path, set `engines.cri.sockets` in the container plugin `init_config`. Paths are relative to `HOST_ROOT` when that variable is set.
- The old `container_engines.cri` configuration is no longer supported, and there is no equivalent of `container_engines.cri.disable_async`.
- `container.id` equal to `host` means a host process, so no image exists.

`k8s.*` fields come from the same runtime socket lookup as `container.*`.

containerd: use the CRI engine on `/run/containerd/containerd.sock`. The native containerd protocol provides only container IDs, while CRI adds names and richer metadata. If `container.name` is missing under containerd, check you configured the CRI engine rather than the containerd engine.

The container plugin `init_config` also has `engine_timeout`, default 10 seconds (0 disables it): an engine that does not answer in time is skipped with a warning for the rest of the run and its containers get no metadata, so check plugin warnings and socket connectivity.

Metrics help: with `state_counters_enabled: true`, snapshots include `falco.n_containers` and `falco.n_missing_container_images`. Processes in a Kubernetes pod sandbox container have no image in the API responses (their `container.id` equals `k8s.pod.sandbox_id`); an image missing for a container's whole life is most likely this case. Metadata can also be absent when an event arrives before its container lookup finishes.

Gotcha: keep other plugin entries and `load_plugins` entries when editing the `container` entry in `plugins`.

## Checked

2026-11-08. Read the Missing Fields page in full. Added engine_timeout default, state counters metrics, pod sandbox containers and lookup timing.

Method: documentation only; no commands were run.
