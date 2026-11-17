---
id: computing-software.systems-network-administration.ceph.erasure-code-profile-create
name: erasure-code-profile-create
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, erasure-coding, profile, k, m, plugin]
level: practitioner
status: docs-checked
description: "Create, inspect and delete Ceph erasure-code profiles, and read the k and m values in the default profile."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/erasure-code-profile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A profile sets how an erasure-coded pool splits data into `k` data chunks plus `m` coding chunks. The default profile is k=2, m=2: four OSDs, any two can be lost, and space use equals a two-replica pool. A k=10, m=4 profile survives four lost OSDs with 40 percent raw overhead.

```
ceph osd erasure-code-profile set {name} \
     [{directory=directory}] \
     [{plugin=plugin}] \
     [{stripe_unit=stripe_unit}] \
     [{key=value} ...] \
     [--force]
ceph osd erasure-code-profile get {name}
ceph osd erasure-code-profile ls
ceph osd erasure-code-profile rm {name}
```

Notes:

- `plugin` defaults to `isa`; `stripe_unit` should be a multiple of 4K and defaults from `osd_pool_erasure_code_stripe_unit` at pool creation.
- A profile referenced by a pool cannot be removed.
- The SHEC and CLAY plugins, and all Jerasure techniques except `reed_sol_van`, are deprecated per the page.
- Pools do not follow later profile edits, so create a new profile and a new pool instead of editing.
- Use it in a pool with `ceph osd pool create {pool} erasure {profile}`.

## Checked

2026-11-03. Confirmed against: the Ceph Erasure code profiles page (docs.ceph.com/en/latest/rados/operations/erasure-code-profile/); the Pools page for the profile-change-after-creation note.

Removed: nothing.

Method: documentation only; no commands were run.
