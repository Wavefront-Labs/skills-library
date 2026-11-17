---
id: creative-arts.animation.encode-delivery.checksum-fixity
name: checksum-fixity
category: creative-arts
field: animation
product: encode-delivery
tags: [checksums, archive, archiving, fixity, md5, sha256, xxhash, md5sum, mhl, file-integrity, data-transfer]
level: practitioner
status: draft
description: "Prove files arrived and stay intact: generate and verify MD5/SHA-256/xxHash manifests, MHL for media transfers, and periodic fixity checks on archives."
sources:
  - https://mediahashlist.org/
  - https://www.dpconline.org/handbook/technical-solutions-and-tools/fixity-and-checksums
  - https://xxhash.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checksums and fixity

**Goal:** proof that a file is bit-for-bit what was sent or archived. Every copy (render
storage to edit, studio to client, disk to LTO) should produce a checksum manifest at the source
and verify it at the destination; archives get re-checked on a schedule.

## Choosing a hash

| Hash | Use |
|---|---|
| xxHash64 / XXH3 | fastest; media transfer verification (camera/DIT world, MHL) |
| MD5 | ubiquitous; still fine for detecting corruption (not for security) |
| SHA-256 | when a client or archive policy requires it; tamper evidence |

## Manifests with standard tools

```bash
# create, relative paths, from the package root
cd DELIVERY && find . -type f ! -name manifest.md5 -print0 | sort -z | xargs -0 md5sum > manifest.md5
# verify at destination
cd DELIVERY && md5sum -c --quiet manifest.md5 && echo ALL OK
# SHA-256 equivalent
find . -type f ! -name manifest.sha256 -print0 | sort -z | xargs -0 sha256sum > manifest.sha256
```

Windows PowerShell: `Get-FileHash -Algorithm SHA256 file.mov`.

## MHL (Media Hash List)

ASC MHL is the industry format for media transfers: an XML (or chain of generations) listing
each file's hash, size and date. Tools: `ascmhl` (open source CLI), Silverstack, Hedge, ShotPut Pro.
```bash
ascmhl create /Volumes/DELIVERY -h xxh64
ascmhl verify /Volumes/DELIVERY
```
Each copy appends a generation, giving a chain of custody.

## Fixity for archives

- Store the manifest with the data and separately (in the asset database).
- Re-verify archives on a schedule (e.g. yearly for disk, at each migration for LTO) and before
  any restore is relied on.
- A changed hash with no recorded change = corruption: restore from the other copy.

## Gotchas

- Hash the file after it is closed: hashing a file still being written gives a valid-looking
  wrong hash.
- Do not copy-then-hash the destination alone; hash at source first or you are verifying a
  copy against itself.
- Renaming files breaks manifests that list names; regenerate or use path-mapped verification.

## Verify

Deliberately alter one byte of a test file in a copy; verification must fail and name that file.
