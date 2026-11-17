---
id: computing-software.systems-network-administration.zfs.zfs-userspace-quota
name: zfs-userspace-quota
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, userspace, groupspace, projectspace, quota, accounting]
level: practitioner
status: docs-checked
description: "Report per-user, per-group and per-project space and quota with zfs userspace, groupspace and projectspace, and filter, sort and script the output."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-userspace.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Space accounting by owner

```
zfs userspace [-Hinp] [-o field[,field]...] [-s field]... [-S field]... [-t type[,type]...] filesystem|snapshot|path
zfs groupspace  [same options]
zfs projectspace [-Hp] [-o field[,field]...] [-s field]... [-S field]... filesystem|snapshot|path
```

`groupspace` is identical to `userspace` but defaults to group types. `projectspace` takes no `-i`, `-n` or `-t`. The target may be a filesystem, a snapshot, or a path (the containing filesystem is used).

```
zfs userspace -o name,used,quota tank/home
zfs userspace -n -s used tank/home
```

## Flags

- `-H`: no headers, tab-delimited
- `-p`: exact numbers
- `-n`: numeric IDs instead of names
- `-i`: map SIDs to POSIX IDs (totals for an entity with both SMB and POSIX files combine under the POSIX entity)
- `-o`: choose fields from `type`, `name`, `used`, `quota`
- `-s` / `-S`: sort ascending or descending by field; repeatable. Default sort is `-s type -s name`
- `-t`: `all`, `posixuser`, `smbuser`, `posixgroup`, `smbgroup`

## Related properties

`userused@user`, `userobjused@user`, `userquota@user`, `userobjquota@user`. Set limits with `zfs set userquota@bob=10G tank/home`.

The target may also be a snapshot.

## Checked

2026-11-03. Confirmed against zfs-userspace(8): userspace, groupspace and projectspace synopsis, `-H`, `-i`, `-n`, `-o` fields, `-p`, `-s`/`-S` default sort, `-t` types and related properties, plus zfs-allow(8) for the userquota property family. Reworded the snapshot sentence.
Method: documentation only; no commands were run.
