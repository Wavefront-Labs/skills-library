---
id: computing-software.systems-network-administration.bash.compression-tools-gzip-xz-zstd
name: compression-tools-gzip-xz-zstd
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, pigz, zstd, xz, gzip, bzip2, compression-levels, pzstd, parallel-compression]
level: practitioner
status: docs-checked
description: "Choose and use gzip/pigz, bzip2, xz and zstd: speed vs ratio, multithreading (-T0), levels, streaming over ssh, integrity tests and decompress-anywhere concerns."
sources:
  - https://github.com/facebook/zstd/blob/dev/programs/zstd.1.md
  - https://www.gnu.org/software/tar/manual/html_node/gzip.html
  - https://man.archlinux.org/man/xz.1
  - https://zlib.net/pigz/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compression tools compared

## What the vendor docs state
| Tool | Documented facts |
|---|---|
| gzip / `pigz` | pigz is a parallel implementation of gzip, a replacement that uses multiple cores when compressing |
| zstd | default level 3; `-T0` uses the detected number of physical cores; `--ultra` unlocks levels 20-22; integrity check on by default |
| xz | default preset `-6`; `-T0` uses as many threads as the CPU supports; default check CRC64 |
| bzip2 | not covered by this skill's sources: check its own manual before relying on specifics |

Relative speed and ratio depend on the data: benchmark on your own data rather than trusting a table.

## Commands
```bash
zstd -T0 -3 big.tar -o big.tar.zst ; zstd -d big.tar.zst ; zstdcat big.tar.zst | tar x
tar -I 'zstd -T0 -10' -cf etc.tar.zst /etc            # -I = --use-compress-program (any compressor)
tar --zstd -xf etc.tar.zst
xz -T0 -9e file ; xz -l file.xz                        # -l lists information about .xz files
zstd --long=27 -T0 vm.img                              # --long enables long-distance matching; bare --long defaults to 27
```
`zstdcat` is equivalent to `zstd -dcf`. A compress program given to `tar -I` must read stdin and write stdout, and decompress when run with `-d`.
Streaming over the network: `tar -cf - /data | zstd -T0 -3 | ssh backup 'cat > data.tar.zst'`.
For fast LAN links, compression can be the bottleneck: use a low level or none.

## Integrity
`xz -t` and `zstd -t` test files without extracting. xz stores an integrity check computed from the uncompressed data (CRC64 by default; headers always CRC32). zstd adds an integrity check by default.

## Gotchas
- Compressing already-compressed data (jpg, mp4, zst) wastes CPU. zstd has an opt-in flag to compress only files that are not already compressed.
- Per the xz man page, `xz -9` needs about 674 MiB to compress and 65 MiB to decompress in single-threaded mode; multi-threaded mode needs significantly more.
- Single-threaded and multi-threaded xz produce different output; only multi-threaded output (for example from `-T0`) can be decompressed using multiple threads. Single-threaded gives the smallest file.
- Check that target systems have `zstd` installed before using it for archives that must open anywhere; otherwise use gzip.

## Verify
- [ ] The tool's `-t` test passes on the archive; decompressed checksum equals the source.

## Checked
Date: 2026-11-02. Confirmed against the zstd man page source (default level 3, -T0, --long default 27, --ultra to 22, -t, default integrity check, zstdcat, opt-in skip of compressed files), the xz man page (-6 default, -T0, memory table 674/65 MiB for -9, -t, -l, CRC64 default, threaded vs single output), the pigz home page (parallel gzip) and the GNU tar manual (--zstd, -I). Removed: speed/ratio table values, gzip/bzip2 -t and -k specifics, pbzip2, unpigz, pigz flag details, RHEL 7 claim (none stated in the sources).
Method: documentation only; no commands were run.
