---
id: computing-software.cloud-infrastructure-engineering.openebs.verify-openebs-installation
name: verify-openebs-installation
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [install, verification, pods, storageclass, openebs-hostpath, openebs-single-replica, helm]
level: intro
status: docs-checked
description: "Verify an OpenEBS install with kubectl get pods -n openebs and kubectl get sc, and know which pods and default StorageClasses to expect with and without Replicated Storage."
sources:
  - https://openebs.io/docs/quickstart-guide/installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After install, check the pods in the `openebs` namespace with `kubectl get pods -n openebs`.

**Default installation.** The sample output lists, among others: `openebs-agent-core`, `openebs-agent-ha-node`, `openebs-api-rest`, `openebs-csi-controller`, `openebs-csi-node`, three `openebs-etcd` pods, `openebs-eventing-aggregator`, `openebs-io-engine`, `openebs-localpv-provisioner`, `openebs-loki`, the LVM controller and node pods, three `openebs-nats` pods, `openebs-obs-callhome`, `openebs-operator-diskpool`, `openebs-promtail` and the ZFS controller and node pods. All show Running with their containers ready.

**Replicated Storage disabled.** The sample shrinks to `openebs-localpv-provisioner`, the LVM controller and node pods, and the ZFS controller and node pods.

**StorageClasses.** `kubectl get sc` should show these defaults (reclaim policy Delete for all four):

| Name | Provisioner | Binding | Expansion |
|---|---|---|---|
| mayastor-etcd-localpv | openebs.io/local | WaitForFirstConsumer | false |
| mayastor-loki-localpv | openebs.io/local | WaitForFirstConsumer | false |
| openebs-hostpath | openebs.io/local | WaitForFirstConsumer | false |
| openebs-single-replica | io.openebs.csi-mayastor | Immediate | true |

To validate the install, the page says to provision a test Local PV volume with the `openebs-hostpath` StorageClass, as in the Local Storage User Guide. The per-engine user guides then show how to use storage devices on the nodes instead of the `/var/openebs` directory.

## Checked

Method: 2026-11-08 read the raw markdown of the cited installation page (openebs/website docs repo) in full and compared each claim. Pod names, StorageClass table and post-install advice match the page; the reclaim-policy note was added and the "needs no extra setup" aside was dropped because the page does not say it.
