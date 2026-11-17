---
id: computing-software.systems-network-administration.zfs.zfs-send-compressed-large-blocks
name: zfs-send-compressed-large-blocks
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, send, compressed, large-blocks, embedded-data, replication]
level: advanced
status: docs-checked
description: "Use zfs send -c, -L and -e to send compressed data, large blocks and embedded data, and avoid streams the receiver rejects."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compressed, large-block and embedded sends

## -c, --compressed

Sends WRITE records with data compressed as on disk. The receiver needs a matching `lz4_compress` or `zstd_compress` feature. If `large_blocks` is enabled and `-L` is not given, data is decompressed before sending. The receiver does not recompress with `-o compress=`; data stays as sent and the new property applies to future writes. Uncompressed data may still compress on receipt unless `-o compress=off`.

## -L, --large-block

Allows blocks larger than 128 KiB. It has no effect if `large_blocks` is disabled or no such block was written, and the receiver needs `large_blocks` enabled. It is required when `large_microzap` is active.

Warning: omitting `-L` on the first replication splits large blocks on receive. Later reverse incrementals are then rejected, and recovery requires a full receive into a new dataset. Adding `-L` to a failing send does not fix it.

## -e, --embed

Uses WRITE_EMBEDDED records for blocks stored compactly via `embedded_data`. The receiver needs `embedded_data` plus matching compression features. Streams made with `-e` cannot be received as encrypted datasets.

## Combined example

```
zfs send -Lce tank/data@a | ssh backup zfs receive pool/data
```

The receiving pool needs the matching features (`large_blocks`, `embedded_data`, and `lz4_compress` or `zstd_compress` when active on the sender). The man page advises using `-L` from the first replication onwards if the direction of replication may ever be reversed.

## Checked

2026-11-03. Confirmed against zfs-send(8) (`-c`, `-L`, `-e` behaviour, receiver feature requirements, `large_microzap`) and zfs-receive(8) (large-block receive failure, `-o compress=`). Removed the unsupported `-Lce` default recommendation and the `zpool get all` advice.
Method: documentation only; no commands were run.
