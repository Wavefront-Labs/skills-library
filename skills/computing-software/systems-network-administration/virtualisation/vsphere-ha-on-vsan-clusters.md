---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-on-vsan-clusters
name: vsphere-ha-on-vsan-clusters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ha-vsan-network, vsphere-ha, vsan, isolation-address, heartbeat-datastore, vmware, vsphere]
level: advanced
status: draft
description: "Configure vSphere HA correctly on vSAN clusters: heartbeats on the vSAN network, isolation addresses, no datastore heartbeats, admission control and partition behaviour."
sources:
  - https://core.vmware.com/resource/vsan-stretched-cluster-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere HA behaviour on vSAN clusters

**Goal:** HA decisions match vSAN object accessibility, so VMs restart where their data is.

## Key difference
When vSAN is enabled, HA network heartbeats move from the management network to the **vSAN network**. HA isolation and partition then mirror vSAN partitions.

## Settings
- **Enable vSAN before HA**, or turn HA off and on after enabling vSAN so it rebinds to the vSAN vmk.
- **Isolation addresses**: set `das.usedefaultisolationaddress = false` and `das.isolationaddress0 = <IP on the vSAN network>` (a vSAN gateway or switch SVI). The management gateway is wrong for a vSAN cluster.
- **Isolation response**: *Power off and restart VMs*. On vSAN, an isolated host cannot reach its objects anyway.
- **Datastore heartbeating**: vSAN datastores cannot be heartbeat datastores. If no other shared datastore exists, set `das.ignoreInsufficientHbDatastore = true` to clear the warning.
- **Admission control**: reserve capacity equal to the host failures you design for (percentage based); keep vSAN slack capacity for rebuilds as well.

## Partitions
In a partition, VMs are restarted only on the side that holds more than 50% of the object's components (quorum). VMs on the minority side are powered off (isolation response) and restarted on the majority side.

## Stretched clusters
- Isolation address per site on the vSAN network; `das.isolationaddress0` and `1`.
- Site affinity via VM/host *should* rules; HA respects them after a site failure.
- Witness traffic separation for 2-node: witness traffic on management vmk (tagged `witness`).

## Verify
Cluster -> Monitor -> vSphere HA shows heartbeats on vSAN vmk; `fdm.log` lists the isolation address; a test host isolation (pull vSAN uplinks in a lab) restarts VMs on remaining hosts.
