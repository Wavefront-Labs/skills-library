---
id: computing-software.cloud-infrastructure-engineering.rook.stretch-storage-cluster-arbiter
name: stretch-storage-cluster-arbiter
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [stretch-cluster, arbiter, five-mons, failuredomainlabel, subfailuredomain, zones]
level: advanced
status: docs-checked
description: "Configure a Ceph stretch cluster with two data zones and an arbiter zone, five mons, and OSD placement restricted to the data zones."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/stretch-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stretch clusters cover environments with only two failure domains for data: if one fails, the data stays fully available in the other. Rook requires three zones.

Layout:
- Two data zones (A and B) run all types of Rook pods. Each runs two mons and holds two replicas, giving four data replicas in total.
- The third, arbiter zone runs a single mon. No other Rook or Ceph daemons are needed there.
- The failure domain is the zone in the example, but another known topology node label already used for OSD failure domains can be chosen.

Example fields:
```
mon:
  count: 5
  allowMultiplePerNode: false
  stretchCluster:
    failureDomainLabel: topology.kubernetes.io/zone
    subFailureDomain: host
    zones:
    - name: a
      arbiter: true
    - name: b
    - name: c
cephVersion:
  image: quay.io/ceph/ceph:v20.2.4
  allowUnsupported: true
```
Five mons must be created for stretch mode. Exactly one of the three zones is `arbiter: true`. `subFailureDomain` defaults to `host` and is where replicas within a zone are spread.

OSDs use either `storageClassDeviceSets` or the `storage` section (the example uses all devices). OSD placement must include the non-arbiter zones, shown as node affinity on `topology.kubernetes.io/zone` with values `b` and `c`.

Refer to the Stretch Cluster design doc for more details.

## Checked

2026-11-03. Confirmed against the Stretch Cluster page: the three zones with one arbiter, five mons, failureDomainLabel and subFailureDomain, the zones list and the OSD placement on the non-arbiter zones. Removed: nothing.

Method: documentation only; no commands were run.
