---
id: computing-software.systems-network-administration.ceph.crush-bucket-management
name: crush-bucket-management
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, crush, bucket, osd-tree, crush-location, weight]
level: advanced
status: docs-checked
description: "Edit the CRUSH hierarchy with ceph osd crush add-bucket, move, set, reweight and remove commands."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/crush-map/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
View the hierarchy with `ceph osd tree`. Buckets are typed (host, rack, datacenter and so on) and OSDs are the leaves.

Add and move buckets:

```
ceph osd crush add-bucket rack12 rack
ceph osd crush move rack12 root=default
ceph osd crush rename-bucket {oldname} {newname}
ceph osd crush remove rack12
```

Place an OSD at a location with a weight:

```
ceph osd crush set osd.0 1.0 root=default datacenter=dc1 room=room1 row=foo rack=bar host=foo-bar-1
```

Change its weight and remove it:

```
ceph osd crush reweight {name} {weight}
ceph osd crush remove {name}
```

Notes:

- `set` takes the OSD name, weight, and one or more `bucket-type=bucket-name` pairs describing its location.
- Use `ceph osd crush reweight` for the CRUSH weight (the absolute capacity, in TiB) and `ceph osd reweight {osd-num} {weight}` for the separate override weight, which is not absolute and must not be confused with the CRUSH weight. An override reweight conflicts with the balancer, which expects override values reset to `1.0000`.
- A bucket must be empty before it can be removed.

## Checked

2026-11-03. Confirmed against: the Ceph CRUSH Maps page (docs.ceph.com/en/latest/rados/operations/crush-map/) (set, reweight, remove an OSD, add-bucket, move, rename-bucket, remove bucket must be empty) and the Control Commands page (docs.ceph.com/en/latest/rados/operations/control/) for osd reweight.

Removed: the claim that moving buckets or changing weights remaps data (not stated for these commands) and the 'between 0 and 1' range.

Method: documentation only; no commands were run.
