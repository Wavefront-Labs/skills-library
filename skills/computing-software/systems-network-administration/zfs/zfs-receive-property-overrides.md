---
id: computing-software.systems-network-administration.zfs.zfs-receive-property-overrides
name: zfs-receive-property-overrides
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, receive, property-override, exclude-property, origin, clone]
level: advanced
status: docs-checked
description: "Override or ignore properties during zfs receive with -o and -x, receive as a clone with -o origin, and know which properties cannot be set."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property overrides on receive

## -o property=value

Sets the property as if `zfs set` ran just before the receive. With `send -R`, descendants that had the property set on the sender inherit the value.

```
zfs send -R tank/data@a | ssh backup zfs receive -o mountpoint=/backup/data -o readonly=on pool/data
```

Restrictions:

- Naming the same property in multiple `-o` or `-x` options is an error.
- Set-once properties (`normalization`, `casesensitivity`) cannot be set, nor can `version` or `volsize`.
- If the send used `-c`, a `compression` override is recorded but does not change the data already compressed.
- `-o` can override encryption properties on the first receive, so an unencrypted stream can become encrypted. `keylocation` cannot be `prompt`, since stdin carries the stream; change it afterwards with `zfs set`.

## -x property

Ignore the stream's value for that property, as if it had been excluded. Inheritable properties are inherited; non-inheritable ones are set locally. On incremental updates, existing local settings are left alone. The `-o` restrictions also apply.

```
zfs receive -x mountpoint -x sharenfs pool/backup
```

Here the stream's `mountpoint` and `sharenfs` values do not affect the received datasets.

## -o origin=snapshot

Receives as a clone of that snapshot. For a full stream this creates a clone; the snapshot only needs to exist. For incremental streams the normal checks still apply.

## Checked

2026-11-03. Confirmed against zfs-receive(8): `-o` and `-x` semantics, restrictions (duplicates, set-once properties, `version`, `volsize`, `-c` compression, `keylocation=prompt`) and `-o origin=`. Reworded the backup-host sentence to what the page states.
Method: documentation only; no commands were run.
