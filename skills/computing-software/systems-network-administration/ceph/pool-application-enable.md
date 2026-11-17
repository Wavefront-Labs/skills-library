---
id: computing-software.systems-network-administration.ceph.pool-application-enable
name: pool-application-enable
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, application, rbd, cephfs, rgw]
level: intro
status: docs-checked
description: "Associate a Ceph pool with an application (rbd, cephfs, rgw or a custom name) and know which tools do it for you automatically."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each pool must be associated with an application before it can be used. In most cases you do not run the command yourself:

- Pools made for CephFS, and pools RGW creates automatically, are associated automatically.
- Pools for RBD should be initialised with the `rbd` CLI tool or the dashboard (see the RBD Block Device Commands page for the exact command).

For unusual cases, attach a free-form application name directly:

```
ceph osd pool application enable {pool-name} {application-name}
```

The application names used by Ceph itself are `cephfs`, `rbd` and `rgw`. These tags also appear as `application rgw` and similar in the output of `ceph osd pool ls detail`, which is the quickest way to audit which pools are tagged.

Pools whose names begin with `.` belong to Ceph and should not be created or modified by hand.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): Associating a Pool with an Application, Pool Names, List Pools (ceph osd pool ls detail shows application).

Removed: the `rbd pool init` example, and the claim that application tags drive CephX caps (neither is on the page).

Method: documentation only; no commands were run.
