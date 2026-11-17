---
id: computing-software.cloud-infrastructure-engineering.openebs.prerequisites-local-pv-hostpath
name: prerequisites-local-pv-hostpath
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [prerequisites, local-pv, hostpath, basepath, rancher, rke, air-gapped, kubelet]
level: intro
status: docs-checked
description: "Prepare nodes for Local PV Hostpath: choose a BasePath (default /var/openebs/local), mount extra disks, add the RKE extra_binds and mirror the two images for air-gapped use."
sources:
  - https://openebs.io/docs/quickstart-guide/prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local PV Hostpath needs only a directory on each node where volumes will be created. The docs call it the `BasePath`, and the default is `/var/openebs/local`.

`BasePath` can be:

- a directory on the root (OS) disk;
- on bare metal, a mounted directory on an additional drive or SSD, for example an SSD at `/dev/sdb` formatted ext4 and mounted at `/mnt/openebs-local`;
- on cloud or virtual instances, a mount from an attached cloud volume or virtual disk, for example a GKE Local SSD at `/mnt/disk/ssd1`.

**Air-gapped clusters.** Make these images available in your local registry: `openebs/provisioner-localpv` and `openebs/linux-utils`.

**Rancher RKE.** The kubelet service must bind-mount the base path through `extra_binds`. For the default path, the page gives:

```
services:
  kubelet:
    extra_binds:
      - /var/openebs/local:/var/openebs/local
```

For every engine, the page says to verify you have the admin context on the cluster, and links troubleshooting steps for creating one if you do not.

The page also lists supported versions: Kubernetes 1.23 or higher, Linux kernel 5.15 or higher, Ubuntu and RHEL 8.8.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for quickstart-guide/prerequisites) in full. Removed the unsourced advice about choosing a dedicated mount early for quotas. Other claims match the page.
