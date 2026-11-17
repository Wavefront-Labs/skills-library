---
id: computing-software.cloud-infrastructure-engineering.kubespray.cri-o-container-manager-registries-and-userns
name: cri-o-container-manager-registries-and-userns
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cri-o, crio, container-manager, registries, user-namespaces, nri, capabilities]
level: advanced
status: docs-checked
description: "Run CRI-O with container_manager crio, configure crio_registries mirrors, insecure registries and auth, user namespaces via crio_remap_enable, default capabilities and NRI."
sources:
  - https://kubespray.io/docs/CRI/cri-o.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CRI-O is supported on Kubernetes v1.11.1 or later; for etcd choose a kubeadm-managed or host deployment.

```yaml
# all/all.yml
download_container: false
skip_downloads: false
etcd_deployment_type: host # optionally kubeadm
# k8s_cluster/k8s_cluster.yml
container_manager: crio
```

**Registries** (`all/crio.yml`): mirrors for Docker Hub via `crio_registries` with fields `prefix`, `insecure`, `blocked`, `location`, `unqualified` and a `mirrors` list (the page uses a local 192.168.100.100:5000 mirror and `mirror.gcr.io`). Insecure registries and their authentication:

```yaml
crio_insecure_registries:
  - 10.0.0.2:5000
crio_registry_auth:
  - registry: 10.0.0.2:5000
    username: user
    password: pass
```

**User namespaces** (optional):

```yaml
crio_runtimes:
  - name: runc
    path: /usr/bin/runc
    type: oci
    root: /run/runc
    allowed_annotations:
    - "io.kubernetes.cri-o.userns-mode"

crio_remap_enable: true
```

`crio_remap_enable` adds an entry for the containers user to `/etc/subuid` and `/etc/subgid`, reserving 16M ids (256 pods times 65536) at the end of the id space.

`crio_default_capabilities` defaults to CHOWN, DAC_OVERRIDE, FSETID, FOWNER, SETGID, SETUID, SETPCAP, NET_BIND_SERVICE and KILL; add MKNOD for a Rancher deployment. With CRI-O v1.26.0 or above, `nri_enabled: true` enables NRI.

## Checked

Settings, YAML and the capability list were confirmed against the CRI-O page.

Method: docs-checked 2026-11-09 against the Kubespray docs/CRI/cri-o.md page (full file read).
