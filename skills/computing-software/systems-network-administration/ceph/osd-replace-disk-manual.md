---
id: computing-software.systems-network-administration.ceph.osd-replace-disk-manual
name: osd-replace-disk-manual
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, osd, replace, destroy, ceph-volume, lvm]
level: advanced
status: docs-checked
description: "Replace a failed OSD disk while keeping the OSD ID, using ceph osd destroy and ceph-volume lvm."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/add-or-rm-osds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replacing keeps the same ID so CRUSH placement and the OSD map stay stable. Sequence:

```
ceph osd out {id}
while ! ceph osd safe-to-destroy osd.{id} ; do sleep 10 ; done
sudo systemctl stop ceph-osd@{id}
ceph osd destroy {id}
ceph-volume lvm zap --destroy /dev/sdX
ceph-volume lvm prepare --osd-id {id} --data /dev/sdX
ceph-volume lvm activate {id} {osd-fsid}
```

Or in one step:

```
ceph-volume lvm create --osd-id {id} --data /dev/sdX
```

Points:

- Mark the OSD `out` first if it is still in so its data moves to other OSDs, then stop it on its host if it is still running.
- `destroy` keeps the CRUSH entry and ID but removes the CephX keys and config-key data.
- `zap --destroy` is optional for a disk that is not new; it also removes the volume groups and logical volumes on the disk and destroys all data on it.

On a cephadm-managed cluster the page says to replace OSDs with the orchestrator instead; see the cephadm skills.

Destroying is irreversible for encrypted OSDs: the step removes the OSD's CephX keys, config-key data and lockbox keys, and on an encrypted OSD the config-key data holds the encryption key, so the old data can never be read again. That is why the sequence first runs `ceph osd safe-to-destroy` in a loop, and why `ceph osd destroy` refuses an OSD that is not `down`. Replacing differs from removing because the replaced OSD's ID and CRUSH map entry stay intact. `ceph-volume lvm list` shows the `osd fsid` that `activate` needs; it is not the cluster fsid.

## Checked

2026-11-09. Confirmed against: the Ceph Adding/Removing OSDs page (docs.ceph.com/en/latest/rados/operations/add-or-rm-osds/): Replacing an OSD, including every command in the sequence, the destroy warning and the single-step ceph-volume lvm create alternative.

Removed: the recovery-watching bullet and the specific orchestrator command (not on this page).

Method: documentation only; no commands were run.

