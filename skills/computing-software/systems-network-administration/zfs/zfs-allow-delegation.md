---
id: computing-software.systems-network-administration.zfs.zfs-allow-delegation
name: zfs-allow-delegation
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, allow, unallow, delegation, permissions, permission-sets]
level: advanced
status: docs-checked
description: "Delegate ZFS administration to users and groups with zfs allow and unallow, using permission sets, create-time grants and scoped local or descendant rules."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-allow.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegated administration

```
zfs allow [-dglu] user|group[,...] perm|@set[,...] dataset
zfs allow [-dl] -e|everyone perm|@set[,...] dataset
zfs allow -c perm|@set[,...] dataset
zfs allow -s @set perm|@set[,...] dataset
zfs allow dataset                       # display
zfs unallow [-dglru] ... 
```

Example: let a backup user snapshot and send.

```
zfs allow -u backup snapshot,mount,send,hold tank/data
```

## Scope

- `-l` local to the named dataset only; `-d` descendants only; neither or both means the dataset and all descendants.
- `-u user` / `-g group` disambiguate names; otherwise the name is tried as `everyone`, then user, then group.
- `-c` grants permissions to the creator of new child datasets (create-time permissions).

## Permission sets

`-s @name` defines a set (names start with `@`, up to 64 characters). Sets are evaluated dynamically, so edits apply immediately. `unallow -s @set` with no permissions deletes the set.

## Permissions

Subcommands (`snapshot`, `send`, `send:raw`, `receive`, `receive:append`, `clone`, `create`, `destroy`, `rollback`, `hold`, `release`, `diff`, `load-key`, `change-key`), quota and usage accounting, and individual properties. Several need `mount` as well (`snapshot`, `destroy`, `rollback`, `create`); `receive` is required for `receive -F`, while `receive:append` is a limited receive that cannot do `-F`.

## Limits

`unallow` removes grants but cannot deny; inherited permissions still apply. On Linux, `mount`, `unmount`, `mountpoint`, `canmount`, `rename` and `share` cannot be delegated.

## Checked

2026-11-03. Confirmed against zfs-allow(8): synopsis, scope flags, name resolution order, `-c`, `-s` set naming and 64-character limit, permission table, unallow behaviour and the Linux limits. Fixed the example, which omitted the `mount` permission that `snapshot` needs.
Method: documentation only; no commands were run.
