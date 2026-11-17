---
id: computing-software.systems-network-administration.kopia.kopia-compression
name: kopia-compression
category: computing-software
field: systems-network-administration
product: kopia
tags: [compression, zstd, s2, benchmark, content-stats]
level: practitioner
status: docs-checked
description: "Choose and enable Kopia compression per policy, benchmark algorithms and measure savings; compression is off by default."
sources: ["https://kopia.io/docs/advanced/compression/", "https://kopia.io/docs/faqs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compression is controlled by policy and is disabled by default. Enable it globally or per source; a change applies going forward and never rewrites data already uploaded.

```console
kopia policy set --global --compression=zstd
kopia policy set /path/to/source --compression=s2-default
```

Accepted values include `none`, `deflate-best-compression`, `deflate-best-speed`, `deflate-default`, `gzip`, `gzip-best-compression`, `gzip-best-speed`, `pgzip`, `pgzip-best-compression`, `pgzip-best-speed`, `s2-better`, `s2-default`, `s2-parallel-4`, `s2-parallel-8`, `zstd`, `zstd-better-compression` and `zstd-fastest`. The FAQ calls zstd one of the top algorithms. Policies also set minimum and maximum file size and extensions to compress.

## Choosing

Run `kopia benchmark compression --data-file=<file>` to compare all variants on your own data. In the documented sample on a highly compressible 466 MB file, s2 was fastest (about 4 GiB/s) but compressed least, zstd compressed far more but at about 300 MiB/s, and pgzip balanced the two. Once compression throughput exceeds your I/O throughput, extra compression is effectively free, so a slower, tighter algorithm is better when I/O is the bottleneck.

Memory: s2 grows roughly linearly with input; pgzip allocates what it needs quickly and plateaus. For small files with little RAM, s2, deflate and gzip are the most memory-friendly.

## Measuring

`kopia content stats` shows savings across the repository and `kopia content list --json` shows sizes before and after per content. The deprecated LZ4 algorithm is no longer readable in newer versions, so migrate such data using a version that still supports it.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Compression (benchmark command, sample output figures, LZ4 note, content stats and content list --json) and FAQ (disabled by default, applies going forward, zstd one of the top algorithms, accepted values).
Method: documentation only; no commands were run.
