---
id: computing-software.systems-network-administration.ceph.pool-delete-safeguards
name: pool-delete-safeguards
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, delete, mon-allow-pool-delete, nodelete, crush-rule]
level: practitioner
status: docs-checked
description: "Delete a Ceph pool safely: the mon_allow_pool_delete gate, the confirmation string, and cleaning up orphaned CRUSH rules and CephX users."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deleting a pool is deliberately awkward. The monitors refuse to remove pools unless `mon_allow_pool_delete` is `true` in central config, and the command takes the pool name twice with `--yes-i-really-really-mean-it`:

```
ceph config set mon mon_allow_pool_delete true
ceph osd pool delete {pool-name} {pool-name} --yes-i-really-really-mean-it
```

The pool setting `nodelete` sets or unsets the NODELETE flag on a pool (1 sets, 0 unsets): `ceph osd pool set {pool-name} nodelete 0`.

After the delete, tidy up what pointed at the pool.

1. Custom CRUSH rule: find the rule a pool used with `ceph osd pool get {pool-name} crush_rule` before deleting. Then check every pool, for example rule 123, with `ceph osd dump | grep "^pool" | grep "crush_rule 123"`. If nothing uses it, the rule is safe to delete.
2. Users with caps restricted to the dead pool: `ceph auth ls | grep -C 5 {pool-name}`, then `ceph auth del {user}`.

To only change the name: `ceph osd pool rename {current-pool-name} {new-pool-name}`. After a rename, update the caps of any user with per-pool capabilities, because they still reference the old name.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): Deleting a Pool, Renaming a Pool, nodelete.

Removed: the claim that a nodelete pool cannot be removed (the page only says the flag is set or unset) and the 'safer alternative' framing.

Method: documentation only; no commands were run.
