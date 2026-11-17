---
id: computing-software.systems-network-administration.ceph.crush-replicated-and-erasure-rules
name: crush-replicated-and-erasure-rules
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, crush, rule, create-replicated, create-erasure, failure-domain]
level: practitioner
status: docs-checked
description: "Create and delete CRUSH rules for replicated and erasure-coded Ceph pools."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/crush-map/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replicated rule: name, root, failure-domain type and optionally a device class.

```
ceph osd crush rule create-replicated {name} {root} {failure-domain-type} [{class}]
```

Erasure rule: derive it from an erasure-code profile.

```
ceph osd erasure-code-profile ls
ceph osd erasure-code-profile get {profile-name}
ceph osd crush rule create-erasure {name} {profile-name}
```

Inspect and remove:

```
ceph osd crush rule ls
ceph osd crush rule dump
ceph osd crush rule rm {rule-name}
```

Practical rules:

- The failure domain you pick (for example `host` or `rack`) makes CRUSH store each replica on a different unit of that type.
- When creating a pool with an erasure-code profile and no rule argument, Ceph creates the CRUSH rule automatically.
- Set a rule on a pool with `ceph osd pool set <pool> crush_rule <rule-name>`.
- Before deleting a rule, confirm no pool uses it: `ceph osd dump | grep "^pool" | grep "crush_rule 123"`.

## Checked

2026-11-03. Confirmed against: the Ceph CRUSH Maps page (docs.ceph.com/en/latest/rados/operations/crush-map/): Creating a rule for a replicated pool, erasure-coded pool, Deleting rules; the Pools page for the crush_rule dump check.

Removed: the six-failure-domains figure for k=4 m=2 and the claim about implicit rules not following later profile edits.

Method: documentation only; no commands were run.
