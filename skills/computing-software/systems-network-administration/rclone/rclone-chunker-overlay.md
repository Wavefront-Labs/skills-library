---
id: computing-software.systems-network-administration.rclone.rclone-chunker-overlay
name: rclone-chunker-overlay
category: computing-software
field: systems-network-administration
product: rclone
tags: [chunker, chunk-size, overlay, composite-files, hashsums, metadata]
level: advanced
status: docs-checked
description: "Use the chunker overlay to split large files for backends with size limits: chunk naming, metadata, hashes and caveats."
sources: ["https://rclone.org/chunker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Chunker wraps a remote and transparently splits files larger than `chunk_size` (default 2G) into pieces on upload, reassembling them on download. Wrap a bucket for bucket-based remotes (`s3:bucket`), because only what sits inside the wrapped path is chunked.

## How it works

Chunks upload under temporary names and are renamed when the upload completes, so operations look atomic and can run in parallel. If an operation fails the hidden chunks are removed and the target stays intact. Listing groups chunks into composite entries and hides temporary ones. A composite file with a missing or invalid chunk produces a warning and the incomplete group is skipped, unless `--chunker-fail-hard` makes commands abort. Chunks can be concatenated by hand.

Default chunk names are `NAME.rclone_chunk.001`; change them with `name_format` using one `*` for the base name and `#` characters for the zero-padded number, optionally starting numbering from 0. Names that do not match the format are treated as normal files. `norename` transactions add a version suffix.

## Metadata and hashes

By default a JSON metadata object named after the file (fields `ver`, `size`, `nchunks`, `md5`, `sha1`, `txn`) is created for composite files only. Setting meta format `none` removes it, but then hashes report as UNSUPPORTED and missing-chunk errors, especially of the last chunk, are more likely. Choose one hash type, MD5 by default, matching the wrapped remote so listings are coherent. `md5all` or `sha1all` force a hash for every file by adding metadata to small files too, which can double the small-file count and cost.

## Caveat

Chunker always writes a temporary file then renames it, even below the threshold, which hurts throughput for many small files on some backends such as Box. Use chunker only for large files with `--min-size` and run a separate non-chunked command for the rest.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
