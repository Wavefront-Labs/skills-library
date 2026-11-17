---
id: computing-software.systems-network-administration.restic.chunking-deduplication
name: chunking-deduplication
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, chunking, deduplication, rabin-fingerprint, polynomial, blob-size]
level: sme
status: docs-checked
description: "How restic splits files with content-defined chunking, why the polynomial matters for cross-repository deduplication, and blob size limits."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/design.rst
  - https://raw.githubusercontent.com/restic/restic/master/doc/045_working_with_repos.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chunking and deduplication

Restic splits file contents into blobs using content-defined chunking based on Rabin fingerprints computed over a 64-byte sliding window. Because boundaries depend on content rather than offsets, inserting data into a file only changes nearby chunks, and the rest deduplicate against the earlier version.

## Sizes

- Files smaller than 512 KiB are not split.
- Blobs range from 512 KiB to 8 MiB.
- The average target is 1 MiB.

## The polynomial

An irreducible polynomial drives the fingerprint. It is chosen at random when the repository is created and stored in `config` as `chunker_polynomial`.

Two repositories with different polynomials chunk the same file differently, so their blobs do not match. To keep deduplication when you `copy` data between repositories, create the destination with the same parameters:

```
restic -r /path/to/new-repo init --from-repo /path/to/old-repo --copy-chunker-params
```

## Privacy

The polynomial is random so that watermark attacks are much harder. The design page also notes that an attacker who can observe the chunk sizes of a known file could derive the polynomial, and that restic 0.18.0 mitigates this by randomly assigning chunks to pack files.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/design.rst, https://raw.githubusercontent.com/restic/restic/master/doc/045_working_with_repos.rst.

Method: documentation only; no commands were run.
