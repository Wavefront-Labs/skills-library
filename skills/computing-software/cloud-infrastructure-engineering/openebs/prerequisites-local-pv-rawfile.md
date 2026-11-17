---
id: computing-software.cloud-infrastructure-engineering.openebs.prerequisites-local-pv-rawfile
name: prerequisites-local-pv-rawfile
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [prerequisites, local-pv, rawfile, reflink, btrfs, xfs, snapshots, clones]
level: practitioner
status: docs-checked
description: "Prepare for Local PV Rawfile: off by default, bundles its own tools, needs only a pool directory (default /var/csi/rawfile), and reflink support for CoW snapshots."
sources:
  - https://openebs.io/docs/quickstart-guide/prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local PV Rawfile is **disabled by default** in the OpenEBS Helm chart, so these prerequisites matter only if you enable it.

The driver container image already bundles `losetup`, `mkfs.ext4`, `mkfs.xfs` and `mkfs.btrfs`, so nothing needs installing on the host. The only host-side requirement is that the storage pool directory, which defaults to `/var/csi/rawfile`, exists or can be created on each node and has enough free space for the volumes you plan to provision.

Snapshots and clones are different. For space-efficient, near-instant copy-on-write behaviour, the filesystem that holds the pool directory must support **reflinks**:

- btrfs supports them natively;
- XFS supports them when formatted with `mkfs.xfs -m reflink=1`;
- ext4 does not currently support reflinks.

Without CoW support, snapshots and clones perform a full data copy instead.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for quickstart-guide/prerequisites) in full. Removed two statements the page does not make: that changing the pool filesystem requires recreating the pool directory, and the `engines.local.rawfile.enabled` value. Other claims match the page.
