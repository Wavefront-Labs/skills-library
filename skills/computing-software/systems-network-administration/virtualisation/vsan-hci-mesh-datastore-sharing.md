---
id: computing-software.systems-network-administration.virtualisation.vsan-hci-mesh-datastore-sharing
name: vsan-hci-mesh-datastore-sharing
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hci-mesh, vsan-datastore-sharing, vsan-max, remote-datastore, vsan, vmware, vsphere]
level: advanced
status: draft
description: "Mount a remote vSAN datastore from another cluster (HCI Mesh / datastore sharing, vSAN Max), with network, limit and policy rules and how failures behave."
sources:
  - https://core.vmware.com/resource/vsan-hci-mesh-tech-note
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCI Mesh and vSAN datastore sharing

**Goal:** use spare capacity of one vSAN cluster from another cluster (or a compute-only cluster) in the same vCenter.

## Roles
- **Server cluster**: owns the vSAN datastore.
- **Client cluster**: another vSAN cluster (HCI Mesh), or a vSphere cluster without local vSAN (compute-only, 7.0U2+), or a vSAN Max storage cluster serving compute clusters (8.0U2+).

## Requirements
- Same vCenter; vSAN Enterprise licensing on both sides.
- vSAN vmkernel connectivity between clusters, 10 GbE+ low latency (sub-millisecond, same datacenter), L3 routing allowed with static routes or the vSAN TCP/IP stack gateway.
- Limits (8.0): a client mounts up to 5 remote datastores; a server serves up to 10 client clusters (check current maximums).

## Mount
Client cluster -> Configure -> vSAN -> Remote datastores -> Mount remote datastore -> pick datastore. Health check *Remote vSAN datastore* tests connectivity first. Then VMs can be placed or Storage vMotioned onto it; storage policies of the server cluster apply.

## Behaviour and gotchas
- Network partition between client and server: VMs on the remote datastore hit APD; HA restarts them once access returns (VMCP setting matters).
- Stretched and two-node clusters had restrictions in earlier versions; check the release notes for your build.
- Data services (dedup, encryption) are those of the server cluster.
- Capacity planning: client VMs consume server cluster slack; keep server cluster under ~70% used.

## Verify
Remote datastore mounted on all client hosts; vSAN health *HCI Mesh* checks green; a test VM runs and survives a client host failover.
