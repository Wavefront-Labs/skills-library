---
id: computing-software.systems-network-administration.virtualisation.vsan-stretched-and-two-node-clusters
name: vsan-stretched-and-two-node-clusters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan, vsan-stretched-cluster, vsan-witness, two-node-vsan, witness-appliance, preferred-site, site-disaster-tolerance, witness-traffic-separation, vmware, vsphere]
level: advanced
status: draft
description: "Design vSAN stretched and two-node clusters: witness appliance placement, latency/bandwidth limits, witness traffic separation, site policies and HA/DRS settings to match."
sources:
  - https://core.vmware.com/resource/vsan-stretched-cluster-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN stretched and two-node clusters

**Goal:** survive a whole-site (or one-host, for two-node) failure with no data loss,
with a witness that breaks ties from a third location.

## Topology
- **Stretched:** two data sites (preferred and secondary) with equal hosts, plus a
  **witness host** (usually the witness appliance VM) in a third site.
- **Two-node:** two hosts (often direct-connected for vSAN traffic) at a branch, witness
  at the main DC.
- Requirements (check the current guide): inter-site RTT ≤ 5 ms between data sites,
  ≤ 200 ms (stretched, up to ~10 hosts/site) or ≤ 500 ms (two-node) to the witness;
  bandwidth sized to write rate (rule: ~1.4x peak write throughput between data sites).

## Witness
- Deploy the witness appliance OVA sized to component count; it **must not** run on the
  cluster it witnesses. One witness per cluster (vSAN 8 allows a shared witness for many
  two-node clusters).
- **Witness traffic separation (WTS):** tag a management vmk for witness traffic
  (`esxcli vsan network ip add -i vmk0 -T=witness`) so data hosts reach the witness over a
  routed network while vSAN data uses the direct link.

## Policies
- **Site disaster tolerance:** "Site mirroring - stretched cluster" protects across sites;
  add local protection (e.g. RAID-5 within each site) for host failures inside a site.
- "None - keep data on preferred/secondary" for site-local workloads (cheaper, no site
  protection).

## Matching HA and DRS
- HA admission control reserve 50% CPU/memory (one site must carry everything).
- HA isolation addresses: one per site (`das.isolationaddress0/1`), disable default gateway
  use (`das.usedefaultisolationaddress=false`).
- DRS **should** VM-Host rules to keep VMs on their data's site (read locality), not must.

## Failure behaviour
- Inter-site link down: the preferred site plus witness keeps quorum; VMs on the secondary
  site are restarted by HA on the preferred site.
- Witness down: data stays available; fix quickly because a further failure is fatal.

## Verify
Skyline Health stretched-cluster checks green; a planned site isolation test (in a
window) restarts VMs on the surviving site; witness latency in performance charts stays
within limits.
