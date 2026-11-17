---
id: computing-software.systems-network-administration.borg.borg-compression-and-obfuscation
name: borg-compression-and-obfuscation
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, compression, lz4, zstd, zlib, lzma, auto-compression, obfuscate, chunker-params]
level: practitioner
status: docs-checked
description: "Choose Borg compression: lz4 default, zstd, zlib, lzma levels, auto mode for media, and size obfuscation specs, with the rule that chunks keep their original compression."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/help.html", "https://borgbackup.readthedocs.io/en/stable/usage/recreate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg compression

Set with `-C/--compression` on `borg create` (default lz4):

- `none`: no compression.
- `lz4`: very fast, low ratio.
- `zstd[,L]`: wide range; L 1-22, default 3; needs Borg 1.1.4+.
- `zlib[,L]`: medium; L 0-9, default 6.
- `lzma[,L]`: slow, high ratio; L 0-9, default 6; above 6 gains little.
- `auto,C[,L]`: test each chunk with lz4 and apply C only if compressible. Good for media.
- `obfuscate,SPEC,C[,L]`: pad sizes to hinder fingerprinting. Needs encryption, inflates the repo, chunks capped near 20 MiB. SPEC `1`-`6` random size factor, `110`-`123` random additive padding (1 KiB up to 8 MiB), `250` Padme padding (up to 12% overhead).

```
borg create --compression zstd,10 repo::a /data
borg create --compression auto,lzma,6 repo::a /media
borg create --compression obfuscate,3,auto,zstd,10 repo::a /data
```

Chunks mix freely across methods because deduplication works on source data. A chunk keeps the compression it was first stored with; change old data with `borg recreate --recompress --compression zlib,9 repo::archive` (the default recompress mode is `if-different`; `always` is needed to change only the level). Default chunker params are `buzhash,19,23,21,4095`.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/help (compression) and usage/recreate): compression specs, levels and defaults, auto and obfuscate SPEC values, recompress modes, default chunker params (create page). Removed: nothing.

Method: documentation only; no commands were run.
