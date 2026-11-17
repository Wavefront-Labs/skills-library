---
id: computing-software.systems-network-administration.zfs.zfs-receive-basics
name: zfs-receive-basics
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, receive, recv, naming, rollback, force, unmount]
level: practitioner
status: docs-checked
description: "Receive ZFS streams safely: target naming with -d and -e, -F rollback behaviour, -u to skip mounting, and -n -v dry runs."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Receiving streams

```
zfs receive [-FhMnsuv] [-d|-e] [-o origin=snapshot] [-o property=value] [-x property] filesystem|volume|snapshot
```

`zfs recv` is an alias. It reads a stream from stdin and creates a snapshot; a full stream also creates the filesystem. An incremental stream needs an existing destination whose newest snapshot matches the stream's source. For zvols, the device link is destroyed and recreated, so the volume is briefly unavailable.

## Naming

- Snapshot target: that exact name is used.
- Filesystem or volume target: a snapshot named like the sent one is created inside it.
- `-d`: drop the first path element of the sent name (usually the pool) and keep the rest under the target.
- `-e`: keep only the last element (the source filesystem's name).

## Flags

- `-F`: roll back to the newest snapshot first. For incremental replication streams, also destroy snapshots and filesystems missing on the sender.
- `-n -v`: dry run showing the name that would be used.
- `-u`: do not mount the received filesystem.
- `-h`: do not receive holds.
- `-v`: show stream info and timing.
- `-M`: force unmount (not supported on Linux).

```
zfs send -R tank/data@a | ssh backup zfs receive -Fduv pool/backup
```

Deduplicated send streams are no longer supported; convert old ones with `zstream redup`.

## Checked

2026-11-03. Confirmed against zfs-receive(8): synopsis, `recv` alias, incremental requirements, zvol behaviour, naming rules for snapshot/filesystem targets and `-d`/`-e`, and the `-F`, `-n`, `-u`, `-h`, `-v`, `-M` descriptions.
Method: documentation only; no commands were run.
