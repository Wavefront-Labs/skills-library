---
id: computing-software.systems-network-administration.zfs.zfs-change-key
name: zfs-change-key
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, change-key, encryption-root, passphrase, pbkdf2iters, keyformat]
level: advanced
status: docs-checked
description: "Change a ZFS user key or passphrase with zfs change-key, adjust keyformat and pbkdf2iters, and make a dataset inherit its parent's key with -i."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-load-key.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing keys

```
zfs change-key [-l] [-o keylocation=value] [-o keyformat=value] [-o pbkdf2iters=value] [-o user:prop=value] filesystem
zfs change-key -i [-l] filesystem
```

The existing key must already be loaded, unless you pass `-l`, which loads the key first (equivalent to `load-key` then `change-key`).

```
zfs change-key tank/secure
zfs change-key -o keyformat=passphrase -o pbkdf2iters=<iterations> tank/secure
```

## What changes

Only the wrapping user key changes; data is not re-encrypted. The command can change `keylocation`, `keyformat` and `pbkdf2iters` and set user properties. Changing `keyformat` or `pbkdf2iters` is only possible through this command after creation. A dataset that was not an encryption root becomes one.

## Inherit a parent's key

```
zfs change-key -i tank/secure/child
```

makes an encryption root inherit its parent's key. This is valid only for an encryption root whose parent is encrypted.

## Practices

- If the old user key was compromised, changing it does not necessarily protect existing or newly written data: the master key stays the same and the old wrapped master key is not overwritten on disk. The man page recommends securely erasing the drives, creating a new pool and copying the data back.
- Change keys on the encryption root, so all children that inherit it follow.
- After changing, confirm with `zfs get keylocation,keyformat,pbkdf2iters,encryptionroot tank/secure`.

## Checked

2026-11-03. Confirmed against zfs-load-key(8) (change-key synopsis, `-l`, `-i`, `-o`, no re-encryption, encryption root behaviour, `encryptionroot` property, master-key warning). Removed the unsupported advice to raise `pbkdf2iters` over time and replaced a specific iteration count with a placeholder.
Method: documentation only; no commands were run.
