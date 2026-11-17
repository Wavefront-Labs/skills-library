---
id: computing-software.cloud-infrastructure-engineering.kubespray.containerd-runtime-and-registry-mirrors
name: containerd-runtime-and-registry-mirrors
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [containerd, container-manager, registry-mirrors, insecure-registry, etcd]
level: practitioner
status: docs-checked
description: "Select containerd with container_manager, keep etcd_deployment_type host, and set registry mirrors, the server field and insecure registries via containerd_registries_mirrors."
sources:
  - https://kubespray.io/docs/CRI/containerd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set containerd as the container runtime in `k8s_cluster.yml`:

```yaml
container_manager: containerd
```

and in `etcd.yml`:

```yaml
etcd_deployment_type: host
```

The page explains why: when `kube_node` contains etcd, the etcd hosts are schedulable, and containerd and dockerd cannot run at the same time, so etcd must run on the host with only containerd.

**Mirrors.** Example for Docker Hub:

```yaml
containerd_registries_mirrors:
  - prefix: docker.io
    mirrors:
      - host: https://mirror.gcr.io
        capabilities: ["pull", "resolve"]
        skip_verify: false
      - host: https://registry-1.docker.io
        capabilities: ["pull", "resolve"]
        skip_verify: false
```

When none of the mirrors has the image, containerd falls back to `https://{{ prefix }}`; change that with a `server:` field on the entry (the page shows `server: https://mirror.example.org`).

**Insecure registries** use the same structure with `http://` hosts and `skip_verify: true`, for prefixes like `test.registry.io`, `172.19.16.11:5000` or `repo:5000`.

The older `containerd_registries` and `containerd_insecure_registries` settings are deprecated.

## Checked

The variables, the server fallback and the deprecation note were confirmed against the containerd page.

Method: docs-checked 2026-11-09 against the Kubespray docs/CRI/containerd.md page (full file read).
