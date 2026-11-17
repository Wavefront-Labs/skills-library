---
id: computing-software.systems-network-administration.ceph.crush-device-classes
name: crush-device-classes
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, crush, device-class, ssd, hdd, crush-rule]
level: practitioner
status: docs-checked
description: "Assign device classes to Ceph OSDs and build a class-restricted replicated CRUSH rule to pin a pool to SSD or HDD."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/crush-map/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OSDs set their device class at startup to `hdd`, `ssd` or `nvme` according to the device, and the class can be set explicitly. Rules can be restricted to one class so a pool uses only those devices.

```
ceph osd crush rm-device-class osd.2
ceph osd crush set-device-class ssd osd.2
ceph osd crush rule create-replicated fast default host ssd
ceph osd pool set <pool-name> crush_rule fast
```

Steps and notes:

- Remove an existing class before setting a new one; `set-device-class` does not overwrite a class that is already assigned.
- `create-replicated <rule-name> <root> <failure-domain> <class>` builds the rule; here the root is `default`, the failure domain `host`.
- Classes are implemented with shadow trees. See them with `ceph osd crush tree --show-shadow`.
- `ceph osd crush rule ls` lists rules and `ceph osd crush rule dump` shows their definitions.

A pool constrained to one class while another pool, such as `.mgr`, spans the default root makes `ceph osd pool autoscale-status` return nothing. Constrain `.mgr` to a class-based rule to fix that.

## Checked

2026-11-03. Confirmed against: the Ceph CRUSH Maps page (docs.ceph.com/en/latest/rados/operations/crush-map/): Device classes, shadow hierarchies; the Placement Groups page for the spanning-pool note.

Removed: the claim that applying the rule needs a quiet window (the page's note on .mgr says a small backfill results).

Method: documentation only; no commands were run.
