---
id: computing-software.systems-network-administration.ceph.cephadm-osd-deploy
name: cephadm-osd-deploy
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, osd, orch-apply, device-ls, osd-spec]
level: practitioner
status: docs-checked
description: "Deploy OSDs with cephadm: list devices, dry-run an all-available-devices spec, add a single device and use an OSD service spec."
sources:
  - https://docs.ceph.com/en/latest/cephadm/services/osd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List candidates:

```
ceph orch device ls [--hostname=...] [--wide] [--refresh]
```

Create OSDs on every unused device, dry-run first:

```
ceph orch apply osd --all-available-devices --dry-run
ceph orch apply osd --all-available-devices
```

That spec is declarative and keeps creating OSDs on new devices. Stop that behaviour with:

```
ceph orch apply osd --all-available-devices --unmanaged=true
```

One device or one LVM volume:

```
ceph orch daemon add osd host1:/dev/sdb
ceph orch daemon add osd host1:data_devices=/dev/sda,/dev/sdb,db_devices=/dev/sdc,osds_per_device=2
ceph orch daemon add osd host1701:/dev/vg_osd/lvm_osd1701
```

Detailed layouts go in a service spec file:

```
ceph orch apply -i spec.yml
```

Attach an existing OSD to a spec with `ceph orch osd set-spec-affinity <service_name> <osd_id(s)>`.

Dry runs are snapshots of one moment, so re-check before applying a spec for real. With `--unmanaged=true` (or `unmanaged: true` in a spec) nothing happens even if you apply a new OSD service, so use it when you want devices left alone. Zapping a device uses `ceph orch device zap <hostname> <path> --force`; without `--force` it stops with `must pass --force to PERMANENTLY ERASE DEVICE DATA`. To move an existing OSD under a spec use `ceph orch osd set-spec-affinity <service_name> <osd_id(s)>`, for example `ceph orch osd set-spec-affinity osd.default_drive_group 0 1`. Preview a spec file with `ceph orch apply -i <osd_spec_file> --dry-run`.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm OSD Service page (docs.ceph.com/en/latest/cephadm/services/osd/): listing devices, all-available-devices, daemon add osd, unmanaged, set-spec-affinity, device zap and spec files.

Removed: nothing; every command and quoted message was found on the page.

Method: documentation only; no commands were run.

