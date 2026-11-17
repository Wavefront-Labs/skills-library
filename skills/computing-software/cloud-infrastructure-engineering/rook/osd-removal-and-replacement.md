---
id: computing-software.cloud-infrastructure-engineering.rook.osd-removal-and-replacement
name: osd-removal-and-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [osd-removal, purge-osd, osd-purge-job, replace-ready-for-swap, removeosdsifoutandsafetoremove, ceph-osd-purge]
level: advanced
status: docs-checked
description: "Add and remove OSDs safely: pre-checks, stopping the operator on host clusters, kubectl rook-ceph purge-osd, the purge job, manual commands and annotated replacement."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Advanced/ceph-osd-mgmt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adding OSDs: Rook watches for new nodes and devices matching the cluster CR `storage` filters and creates OSDs. For PVC-based OSDs, raise the `count` of a `storageClassDeviceSets` entry or add another set.

Before removing an OSD:
- Confirm enough space remains and the remaining OSDs and PGs are healthy.
- Do not remove too many at once, and wait for rebalancing between removals.
- If all PGs are `active+clean` with no low-space warnings the data is fully replicated; a failing OSD will not be perfectly clean, so proceed anyway.

On host-based clusters, stop the operator so it does not re-create the OSD before the disk is wiped:
```
kubectl -n rook-ceph scale deployment rook-ceph-operator --replicas=0
```
Purge the OSD, delete data or replace the disk, then scale the operator back to 1. With the krew plugin: `kubectl rook-ceph rook purge-osd 0 --force`. Or use the `rook-ceph-purge-osd` job: set the IDs in `osd-purge.yaml`, `kubectl create -f osd-purge.yaml`, read logs with `kubectl -n rook-ceph logs -l app=rook-ceph-purge-osd`, then delete the job.

Manual toolbox steps: `ceph osd out osd.<ID>` to start backfill, then `ceph osd purge <ID> --yes-i-really-mean-it`. The operator removes deployments that are safe-to-destroy automatically only with `removeOSDsIfOutAndSafeToRemove` set.

Annotated replacement: annotate the OSD deployment for replacement (the ID in the value must match). Rook drains and destroys it, then adds `osd.rook.io/replace-ready-for-swap`. Cancel only before that annotation appears.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-osd-mgmt) against this skill: 14 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
