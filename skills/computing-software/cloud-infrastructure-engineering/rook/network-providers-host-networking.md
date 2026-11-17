---
id: computing-software.cloud-infrastructure-engineering.rook.network-providers-host-networking
name: network-providers-host-networking
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [network-provider, host-networking, addressranges, public-network, cluster-network, mon-ip]
level: advanced
status: docs-checked
description: "Choose between the default pod network and host networking for Ceph, define public and cluster networks with addressRanges, and handle mon IP annotations."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/network-providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Rook uses the Kubernetes software-defined network. That is simple and gives good node-level security, but adds latency, makes storage traffic contend with application bandwidth, and lets applications reach Ceph daemons by network scanning.

Ceph networks: daemons always use the public network, which carries client reads and writes (and Ceph-CSI traffic for PVCs); Rook defaults it to the pod network. The optional cluster network isolates internal replication, including OSD recovery. If unset, the public network carries that traffic.

`network.addressRanges` is optional and maps directly to Ceph's `public_network` and `cluster_network`:
```
network:
  provider: host
  addressRanges:
    public:
    - "192.168.100.0/24"
    - "192.168.101.0/24"
    cluster:
    - "192.168.200.0/24"
```
The default provider cannot use address ranges. Changing networks is allowed but needs great care: Rook assumes the current configuration keeps working, and changes reach OSD and MDS pods only when they restart, so restarted pods must still reach existing ones.

`network.provider: host` uses the host interfaces. It removes the pod-network latency but gives no host-level isolation, and Ceph uses any host network unless `addressRanges` restrict it. To set a mon IP different from the node IP, annotate the node with `network.rook.io/mon-ip: <IPAddress>`. If you switch host networking on a cluster with running mons, fail the mons over to complete the conversion.

## Checked

2026-11-03. Confirmed against the Network Providers page: default SDN trade-offs, public and cluster network roles, addressRanges example, provider host, the network.rook.io/mon-ip node annotation and the mon failover step. Removed: nothing.

Method: documentation only; no commands were run.
