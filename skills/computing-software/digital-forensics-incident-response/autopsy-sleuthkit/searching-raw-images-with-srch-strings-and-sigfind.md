---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.searching-raw-images-with-srch-strings-and-sigfind
name: searching-raw-images-with-srch-strings-and-sigfind
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [sigfind, sleuthkit, file-signatures, raw-image, dfir]
level: practitioner
status: docs-checked
description: "Locate lost boot sectors, superblocks and partition tables in raw images by hex signature with sigfind, and keep search offsets traceable."
sources: ["https://www.sleuthkit.org/sleuthkit/man/sigfind.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Searching raw images (sigfind)

**Goal:** physical searches that ignore the filesystem, so allocated, deleted, slack and unallocated content are all covered, with offsets you can map back to files or structures.

## Signature search with sigfind
`sigfind [-b bsize] [-o offset] [-t template] [-lV] [hex_signature] file` searches a file for a hex signature at a given offset within each block. The manual says it can be used to search for lost boot sectors, superblocks and partition tables. The file can be any raw data.

- `-b bsize`: block size to search in; default 512, and it must be a multiple of 512.
- `-o offset`: offset within the block where the signature must exist; default 0.
- `-t template`: a named template that defines the signature value and offset. Run `sigfind` with no options to list the supported templates.
- `-l`: the signature is stored little-endian, so it is reversed before matching.
- The `hex_signature` argument is required unless `-t` is used.

Examples from the manual:
```bash
sigfind -o 510 -l AA55 disk.dd      # boot sector signature at offset 510, given little-endian
sigfind -t fat disk.dd              # FAT template
```
Use it to find the start of a wiped or deleted partition or a lost filesystem structure, then record the block offset it reports.

## Gotchas
- Compressed or encrypted content will not match a plain signature or text search; extract or decompress first.
- Keep the exact signature, block size and offset arguments in case notes for reproducibility.

## Self-check
Every hit has an offset that has been mapped to a structure, file or unallocated region, and the parameters used are recorded.

## Checked
Checked 2026-11-09 against the sigfind manual page (synopsis, options, defaults, description, examples). Removed: srch_strings and grep keyword-search recipes, blkls and blkcalc usage, UTF-16 search advice, specific NTFS, ext and 55AA signature examples, and the list of built-in templates, none of which the cited page states; the old claim that `-o` defaults to 510 was wrong (default is 0).
Method: documentation only; no commands were run.
