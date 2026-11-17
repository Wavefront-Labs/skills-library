---
id: computing-software.systems-network-administration.zfs.zfs-send-resume-token
name: zfs-send-resume-token
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, send, receive, resume, receive-resume-token, interrupted]
level: advanced
status: docs-checked
description: "Resume an interrupted ZFS replication with zfs receive -s and zfs send -t using the receive_resume_token, or discard partial state with receive -A."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resumable replication

Large transfers over unreliable links should be received with `-s`, which keeps partial state if the stream is interrupted.

```
zfs send tank/data@a | ssh backup zfs receive -s pool/data
```

This needs the `extensible_dataset` feature.

## Resume

1. Read the token from the receiving dataset:

```
ssh backup zfs get -H -o value receive_resume_token pool/data
```

2. Restart the stream with it:

```
zfs send -t <token> | ssh backup zfs receive -s pool/data
```

`zfs send -t` also accepts `-P`, `-V`, `-e`, `-n` and `-v`. Add `-n -v` first to see what would be sent.

## Partially received state

`zfs send -S filesystem` sends the partially received state of a filesystem whose resumable receive was interrupted, using the last fully received snapshot as the incremental source if one exists.

## Give up

```
zfs receive -A pool/data
```

aborts the interrupted `-s` receive and deletes its partial state, after which you can start a fresh send.

## Checked

2026-11-03. Confirmed against zfs-send(8) (`-t`, `-S`, accepted flags) and zfs-receive(8) (`-s`, `-A`, `extensible_dataset`, `receive_resume_token`), and zfs-get(8) for `-H -o value`. Removed the unsupported advice about reusing tokens.
Method: documentation only; no commands were run.
