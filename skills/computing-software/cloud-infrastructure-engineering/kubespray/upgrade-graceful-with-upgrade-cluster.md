---
id: computing-software.cloud-infrastructure-engineering.kubespray.upgrade-graceful-with-upgrade-cluster
name: upgrade-graceful-with-upgrade-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [upgrade, upgrade-cluster, cordon, drain, kube-version]
level: practitioner
status: docs-checked
description: "Upgrade an existing cluster with upgrade-cluster.yml, which cordons, drains and uncordons nodes, and set kube_version; contrast with the unsafe cluster.yml route."
sources:
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray handles an upgrade the way it handles first deployment: each component is laid down in a fixed order. Individual versions can be pinned with `docker_version`, `docker_containerd_version`, `containerd_version`, `kube_version`, `etcd_version`, `calico_version`, `calico_cni_version` and `flannel_version`.

The graceful route uses a separate playbook that cordons, drains and uncordons nodes. It only works on an existing cluster with at least one `kube_control_plane` deployed:

```ShellSession
ansible-playbook upgrade-cluster.yml -b -i inventory/sample/inventory.ini -e kube_version=1.19.7
```

Afterwards `kubectl version` should show the new Server Version.

The page also shows an "unsafe" upgrade using `cluster.yml`, run once per step with the version, adding `-e '{"upgrade_cluster_setup": true}'`:

```ShellSession
ansible-playbook cluster.yml -i inventory/sample/inventory.ini -e kube_version=1.18.10 -e '{"upgrade_cluster_setup": true}'
```

That variable migrates deployments like kube-apiserver inside the cluster immediately, which is normally only done in the graceful upgrade.

Warning on the page: upgrading from an older release straight to the latest release is unsupported and likely to break something.

## Checked

2026-11-04. Version variables, both command forms and the warning were confirmed on the Upgrading Kubernetes in Kubespray page.

Method: documentation only; no commands were run.
