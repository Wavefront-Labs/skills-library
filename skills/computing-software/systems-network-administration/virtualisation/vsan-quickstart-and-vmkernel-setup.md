---
id: computing-software.systems-network-administration.virtualisation.vsan-quickstart-and-vmkernel-setup
name: vsan-quickstart-and-vmkernel-setup
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-quickstart, vsan-vmkernel, vsan, cluster-quickstart, vsan-networking, vmware, vsphere]
level: practitioner
status: draft
description: "Stand up a vSAN cluster with Cluster Quickstart: prerequisites, vSAN VMkernel adapters on a vDS, claiming disks for OSA or ESA, and the post-enable health checks."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enabling vSAN with Quickstart

## Prerequisites
- 3+ hosts (2 + witness for two-node), all on vSAN ReadyNode/HCL components, same ESXi
  build, controllers in HBA/passthrough mode.
- Dedicated vSAN network: 10 GbE minimum OSA, **25 GbE minimum for ESA**; MTU consistent
  (9000 recommended) end to end.
- Licence with vSAN; NTP synced; DNS forward/reverse for all hosts.
- Disks empty (no partitions). Check: `vdq -q` lists devices and "Eligible for use by VSAN".

## Quickstart flow (Cluster → Configure → Quickstart)
1. **Cluster basics**: enable vSAN (plus HA/DRS).
2. **Add hosts**.
3. **Configure cluster**: creates/uses a vDS, port groups, and one vmk per host for vMotion
   and one for vSAN with static IPs or DHCP; choose vSAN ESA vs OSA, dedup/compression
   (OSA), encryption, fault domains, and claim disks (OSA: cache vs capacity tiers;
   ESA: storage pool).

Manual equivalent for the VMkernel:
```sh
esxcli network ip interface add -i vmk3 -p vSAN-PG
esxcli network ip interface ipv4 set -i vmk3 -t static -I 10.10.40.11 -N 255.255.255.0
esxcli network ip interface set -i vmk3 -m 9000
esxcli vsan network ip add -i vmk3
esxcli vsan network list
```

## Post-enable checks
- Monitor → vSAN → Skyline Health → Retest: Network (connectivity, MTU, unicast), Physical
  disk, HCL DB up to date, Controller driver/firmware.
- Proactive tests: VM creation test.
- `esxcli vsan cluster get` shows every host as member with the same sub-cluster UUID.

## Gotchas
- Quickstart is a one-time workflow; after "skip quickstart", configure manually.
- vSAN traffic uses unicast (6.6+); a missing vmk on one host partitions the cluster
  (health: "vSAN cluster partition").
- Tagging vmk for vSAN witness traffic (two-node direct connect) is separate:
  `esxcli vsan network ip add -i vmk0 -T=witness`.
- vCLS VMs land on vSAN as soon as it exists; plan before enabling vSAN maintenance.

## Verify
vsanDatastore capacity equals expected raw capacity minus overhead; health all green;
test VM deploys with the default storage policy and is compliant.
