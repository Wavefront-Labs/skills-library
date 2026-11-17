---
id: computing-software.cloud-infrastructure-engineering.rook.quickstart-operator-and-cluster-deploy
name: quickstart-operator-and-cluster-deploy
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [quickstart, rook-operator, crds-yaml, cluster-yaml, datadirhostpath]
level: intro
status: docs-checked
description: "Deploy the Rook operator and a Ceph cluster with the quickstart manifests and verify the pods in the rook-ceph namespace."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/quickstart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The quickstart deploys Rook from the example manifests of a tagged release. Always test in a virtual machine, never on a host whose local devices could be consumed by mistake.

Commands from the guide (the page shows a v1.21.1 clone):
```
git clone --single-branch --branch v1.21.1 https://github.com/rook/rook.git
cd rook/deploy/examples
kubectl create -f crds.yaml -f common.yaml -f csi-operator.yaml
kubectl create -f operator.yaml
kubectl -n rook-ceph get pod
kubectl create -f cluster.yaml
```
Wait until `rook-ceph-operator` is `Running` before creating the cluster. The Rook Helm charts can replace these manifests for the operator and the cluster.

Pick the cluster manifest to match the environment:
- `cluster.yaml`: bare metal production, needs at least three worker nodes.
- `cluster-on-pvc.yaml`: production in a dynamic cloud environment.
- `cluster-test.yaml`: test environments such as minikube.

For the cluster to survive reboots, set `dataDirHostPath` to a path valid on the hosts. With the default `cluster.yaml`, one OSD is created for each available device on each node.

A healthy result lists operator, CSI controller and node plugin pods, `rook-ceph-mon-a/b/c`, one or two `rook-ceph-mgr` pods, `rook-ceph-osd-N` pods and completed `rook-ceph-osd-prepare-*` pods. If mon, mgr or osd pods never appear, consult the Ceph common issues page.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (quickstart) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 3 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
