---
id: computing-software.cloud-infrastructure-engineering.rook.network-providers-multus
name: network-providers-multus
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [multus, networkattachmentdefinition, macvlan, whereabouts, selectors, public-network]
level: sme
status: docs-checked
description: "Use Multus NetworkAttachmentDefinitions for Ceph public and cluster networks, with host routing rules, macvlan and whereabouts guidance."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/network-providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook supports Multus NetworkAttachmentDefinitions (NADs) for the Ceph public and cluster networks, attaching any CNI to Ceph for strong isolation from applications. The intent is to connect Ceph to specific host interfaces for latency and bandwidth while keeping host-level isolation.

For host-network Ceph-CSI to talk to a Multus CephCluster, hosts and pods must route to each other:
- Each host needs an interface on the Multus public network, with an IP address, and a route sending traffic for pods on that network through that interface.
- The public NAD's IPAM must route traffic destined for nodes through the network.
- No node IP may overlap any pod IP on the Multus public network.

Plan address space: there are often ten or more Rook and Ceph pods per host, so the pod range may need to be an order of magnitude larger than the host range.

Recommendations:
- CNI type `macvlan`, which has less CPU and memory overhead than a Linux bridge. The `master` interface name must be the same on all hosts.
- IPAM type `whereabouts`, giving each pod a cluster-unique IP with no DHCP server. Avoid overlap with any DHCP range.

Selectors reference the NAD with its namespace. If `public` is left out, client traffic uses the pod network. Only OSD pods get both networks; other Ceph and CSI pods get only public, and the operator gets none, proxying commands via a sidecar in the mgr pod.

Rook tries to auto-discover CIDRs, takes a new lease on each reconcile, and may fail, so set `addressRanges` manually in that case.

## Checked

2026-11-08. Read in full against https://rook.io/docs/rook/latest-release/CRDs/Cluster/network-providers/ : host routing prerequisites, macvlan and whereabouts recommendations, selectors, which pods get which networks, auto-discovery caveat. Nothing else was removed.

Method: documentation only; no commands were run.
