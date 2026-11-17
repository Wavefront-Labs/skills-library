---
id: computing-software.cloud-infrastructure-engineering.kubespray.upgrade-single-components-with-tags
name: upgrade-single-components-with-tags
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [upgrade, tags, etcd, kubelet, network, helm]
level: sme
status: docs-checked
description: "Upgrade only one component with cluster.yml tags (etcd, node, master, network, apps, helm), including skipping etcd cert rotation; unsupported by CI."
sources:
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray installs components in a fixed order and upgrades them in the same order: Docker, Containerd, etcd, kubelet and kube-proxy, the network plugin (such as Calico), kube-apiserver / kube-scheduler / kube-controller-manager, then add-ons (such as KubeDNS).

To upgrade one component, run `cluster.yml` with a tag. The page warns this is not covered by CI, so it is not guaranteed to work, and only suits fully deployed, healthy hosts, not undeployed or partial ones.

```ShellSession
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=etcd
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=etcd --limit=etcd --skip-tags=etcd-secrets
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=node --skip-tags=k8s-gen-certs
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=master
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=network
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=apps
ansible-playbook -b -i inventory/sample/inventory.ini cluster.yml --tags=helm
```

In order: etcd, etcd without rotating certs, kubelet, Kubernetes master components, network plugins, all add-ons, and just helm (requires `helm_enabled`). A `--tags=docker` run upgrades docker.

## Checked

2026-11-04. Component order, the warning and each tag command were confirmed on the Upgrade order and Component-based upgrades sections of the Upgrading page.

Method: documentation only; no commands were run.
