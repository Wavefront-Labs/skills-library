---
id: computing-software.systems-network-administration.restic.pack-and-index-format
name: pack-and-index-format
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, pack-files, index, blob, tree, zstandard, repository-format]
level: sme
status: docs-checked
description: "Understand restic pack files, blob types, header layout, compression, and index file contents, for debugging and tooling."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/design.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pack and index format

## Pack files

A pack is a series of independently encrypted blobs followed by an encrypted header and a length:

```
EncryptedBlob1 || ... || EncryptedBlobN || EncryptedHeader || Header_Length
```

`Header_Length` is a 4-byte little-endian integer at the end of the file, so reading the tail of a pack is enough to index it.

Blob type tags in the header:

- `0b00` data blob
- `0b01` tree blob
- `0b10` compressed data blob
- `0b11` compressed tree blob

Each entry has the encrypted length, the plaintext hash, and for compressed blobs also the plaintext length. Compression uses zstandard and requires repository format 2. Data and tree blobs must live in separate packs.

## Unpacked files

Indexes, locks and snapshots are single encrypted files. In format 1 the plaintext is JSON; in format 2 it starts with an encoding byte (`[` or `{` for plain JSON, `2` for zstd-compressed JSON).

## Index

An index file is JSON with `supersedes` (IDs of replaced indexes) and `packs`, each pack listing blobs with `id`, `type`, `offset`, `length` and, for compressed blobs, `uncompressed_length`. Index files are kept to about 8 MiB, and a pack may appear in more than one index.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/design.rst.

Method: documentation only; no commands were run.
