---
id: computing-software.cloud-infrastructure-engineering.openebs.prerequisites-replicated-pv-mayastor-nodes
name: prerequisites-replicated-pv-mayastor-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [prerequisites, mayastor, replicated-storage, hugepages, nvme-tcp, kernel, io-engine, ports, multipath]
level: advanced
status: docs-checked
description: "Worker-node requirements for Replicated PV Mayastor: SSE4.2 x86-64, kernel modules, 2 cores, 1GiB RAM and 2GiB hugepages per io-engine, free ports, optional multipath."
sources:
  - https://openebs.io/docs/quickstart-guide/prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replicated PV Mayastor is the most demanding engine to prepare. Every worker node needs:

- an **x86-64 CPU with SSE4.2**;
- Linux kernel 5.15 (tested), with 5.13 or higher recommended, and the `nvme-tcp` module loaded, plus `ext4` and optionally `xfs`;
- Helm v3.7 or later.

Each node that will host an **io-engine** pod must have free and available for that pod's exclusive use:

- two CPU cores;
- 1GiB of RAM;
- HugePage support, with at least **2GiB of 2MiB-sized pages**.

**Network.** The ports 10124 (the Mayastor gRPC server) and 8420 and 4421 (NVMf targets) must not be in use on the node, and the firewall must not restrict connections to the node.

**High availability.** Enabling `nvme_core.multipath` is required for the HA feature; set the kernel parameter `nvme_core.multipath=Y` at installation. The page marks this prerequisite as optional, meaning it is needed only if you want HA.

**Placement.** Nodes carrying the label `openebs.io/engine=mayastor` run io-engine. If an application is scheduled onto such a node, the volume target is preferably placed on that same node.

**Cluster size and transport.** The minimum supported worker node count is three; with N-way mirroring, the number of nodes running io-engine pods must be no less than the replication factor. Volumes are exported and mounted over NVMe-oF TCP only, which needs kernel 5.13 or later and the `nvme-tcp` module loaded.

**Hugepages.** At least 1024 2MiB pages (2GiB) must be available exclusively to the io-engine pod on each node. Check with `grep HugePages /proc/meminfo`; set with `echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages` and persist with `vm.nr_hugepages = 1024` in `/etc/sysctl.conf`. After changing hugepages you must restart kubelet or reboot, because Mayastor will not deploy correctly unless the kubelet reports enough pages.

**Labelling.** Label each io-engine candidate node with `kubectl label node <node_name> openebs.io/engine=mayastor`. If `csi.node.topology.nodeSelector` is true, nodes must also be labelled to match `csi.node.topology.segments`.

**Versions.** The page's supported list: Kubernetes 1.23 or higher and Linux kernel 5.15 or higher.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for quickstart-guide/prerequisites) in full. Removed the claim that the Local PV engines need none of these requirements, which the page does not state. Existing claims match the page; added node count, transport, hugepages and labelling details from it.
