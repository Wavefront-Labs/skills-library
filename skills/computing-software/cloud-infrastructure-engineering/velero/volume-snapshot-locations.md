---
id: computing-software.cloud-infrastructure-engineering.velero.volume-snapshot-locations
name: volume-snapshot-locations
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [volume-snapshot-location, snapshot-location, vsl, default-volume-snapshot-locations, portworx]
level: practitioner
status: docs-checked
description: "Configure VolumeSnapshotLocations per provider, choose them with --volume-snapshot-locations, and handle the multi-location requirement."
sources:
  - https://velero.io/docs/main/locations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `VolumeSnapshotLocation` (VSL) is defined entirely by provider-specific fields (AWS region, Azure resource group, Portworx snapshot type).

Create locations for two providers in one backup:

```shell
velero snapshot-location create ebs-us-east-1 --provider aws --config region=us-east-1
velero snapshot-location create portworx-cloud --provider portworx --config type=cloud
velero backup create full-cluster-backup --volume-snapshot-locations ebs-us-east-1,portworx-cloud
```

When each provider has only one VSL, Velero uses it automatically and `velero backup create full-cluster-backup` needs no flag.

Rules and caveats:
- A backup uses one VSL per volume provider; a snapshot cannot go to several locations.
- If more than one VSL exists for a provider, you must name a valid one at backup creation, even when volumes use File System Backup. Alternatively set `--default-volume-snapshot-locations` on `velero server` (the Velero deployment) to list the default per provider.
- Providers constrain location. AWS and Azure cannot create a snapshot in a different region than the volume; the backup fails if the VSL region differs.
- Cross-provider is not supported: with only an EBS VSL on a cluster that also has Portworx volumes, only the EBS volumes are snapshotted.
- Portworx can keep some snapshots local (`type=local`) and others cloud (`type=cloud`).

## Checked

2026-11-08. Read in full: the Backup Storage Locations and Volume Snapshot Locations page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
