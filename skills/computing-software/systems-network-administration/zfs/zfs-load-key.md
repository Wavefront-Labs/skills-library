---
id: computing-software.systems-network-administration.zfs.zfs-load-key
name: zfs-load-key
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, load-key, unload-key, encryption, keylocation, keystatus]
level: practitioner
status: docs-checked
description: "Load and unload ZFS encryption keys with zfs load-key and unload-key, test keys with -n, and use -L, -r and -a."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-load-key.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading and unloading keys

```
zfs load-key [-nr] [-L keylocation] -a|filesystem
zfs unload-key [-r] -a|filesystem
```

Loading a key makes the filesystem and children that inherit `keylocation` accessible and sets `keystatus` to available. It does not mount; use `zfs mount -l` to prompt for the key and mount in one step.

```
zfs load-key tank/secure
zfs mount tank/secure
```

## load-key flags

- `-n`: dry run. Checks the key is correct without loading it; works even if it is already loaded.
- `-r`: also load keys for all descendant encryption roots.
- `-a`: load keys for all encryption roots in all imported pools.
- `-L keylocation`: use this location instead of the `keylocation` property, without changing the property. With `-r` or `-a`, only `prompt` is allowed.

## unload-key

Removes access to the dataset and children inheriting `keylocation`. The dataset must be unopened and unmounted. `keystatus` becomes unavailable. `-r` and `-a` work as above.

```
zfs unmount tank/secure
zfs unload-key tank/secure
```

`zfs unmount -u` unloads keys for encryption roots it unmounts.

## Checked

2026-11-03. Confirmed against zfs-load-key(8) (load-key and unload-key synopsis, `-n`, `-r`, `-a`, `-L`, keystatus, mount not implied) and zfs-mount(8) (`-l`, `unmount -u`). Removed the `zpool import -l` claim, which no fetched page confirms.
Method: documentation only; no commands were run.
