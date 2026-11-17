---
id: computing-software.cloud-infrastructure-engineering.portainer.install-portainer-on-kubernetes
name: install-portainer-on-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [install, kubernetes, helm, storageclass, rbac]
level: practitioner
status: docs-checked
description: "Install Portainer Server on a bare-metal Kubernetes cluster, covering the required default StorageClass, cluster-admin rights and the portainer namespace."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/install/server/kubernetes/baremetal.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: an up-to-date Kubernetes cluster, `helm` or `kubectl` access, cluster-admin rights (Portainer creates a ServiceAccount and ClusterRoleBinding), and a default StorageClass. Assumptions: RBAC is enabled (needed for Portainer's access control), the `portainer` namespace is used (other namespaces are currently unsupported), and the metrics server is installed if you want metrics in the UI.

Portainer needs persistence, so a StorageClass must be marked default; otherwise deployment will likely fail. The docs recommend block storage over network storage for performance and reliability, and advise checking the IOPS of the volume you choose. Check with:

```
kubectl get sc
```

Look for `(default)` after a class name. To set one: `kubectl patch storageclass <storage-class-name> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'`. With the Helm chart you can instead pass `--set persistence.storageClass=<storage-class-name>`.

On a NodePort install, Edge Agents use ports 30779 (UI) and 30776 (tunnel) instead of 9443 and 8000.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Replaced the abbreviated patch command with the documented one and added the Helm parameter.

Method: documentation only; no commands were run.
