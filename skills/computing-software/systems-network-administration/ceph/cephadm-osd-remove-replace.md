---
id: computing-software.systems-network-administration.ceph.cephadm-osd-remove-replace
name: cephadm-osd-remove-replace
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, osd, rm, replace, zap]
level: practitioner
status: docs-checked
description: "Remove or replace OSDs under cephadm with ceph orch osd rm, track progress and stop a removal."
sources:
  - https://docs.ceph.com/en/latest/cephadm/services/osd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remove:

```
ceph orch osd rm <osd_id(s)> [--replace] [--force] [--zap]
ceph orch osd rm 1701
ceph orch osd rm 1138 --zap
```

The orchestrator drains the OSD by moving its PGs away, then removes it. `--zap` also wipes the device.

Watch and cancel:

```
ceph orch osd rm status
ceph orch osd rm stop <osd_id(s)>
```

Replace a failed drive and keep the OSD ID:

```
ceph orch osd rm 1701 --replace
```

The OSD is marked destroyed rather than removed from CRUSH; when a new device matching the OSD spec appears on the host, it is built with the same ID.

Use `--force` only when you accept the risk to data availability; the default is to drain first. Device inventory for the replacement comes from `ceph orch device ls`.

Safety behaviour: an OSD that is not safe to destroy is not rejected, it stays in the removal queue until its PGs have drained and `ceph osd safe-to-destroy` succeeds. `--force` skips both waits; without it cephadm skips them only for an OSD in the `error` state that holds no PGs. `ceph orch osd rm status` prints OSD, HOST, STATE, PGS, REPLACE, FORCE, ZAP and DRAIN STARTED AT, or `No OSD remove/replace operations reported`. A replaced OSD is flagged `destroyed`, its ID is reused, and the replacement must be created on the same host. New drives matching your OSD spec take the old IDs automatically.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm OSD Service page (docs.ceph.com/en/latest/cephadm/services/osd/): Remove an OSD, status and stop, Replace an OSD, destroyed flag and the force and error-state behaviour.

Removed: nothing; every statement was found on the page.

Method: documentation only; no commands were run.

