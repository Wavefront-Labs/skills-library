---
id: computing-software.digital-forensics-incident-response.evidence-handling.fuzzy-hashing-with-ssdeep-and-tlsh
name: fuzzy-hashing-with-ssdeep-and-tlsh
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [ssdeep, fuzzy-hashing, tlsh, similarity-hashing, malware-clustering, dfir]
level: practitioner
status: draft
description: "Use fuzzy hashing (ssdeep, TLSH) to find similar files and malware variants: generating, comparing, thresholds, and limits compared with cryptographic hashes."
sources: ["https://ssdeep-project.github.io/ssdeep/", "https://github.com/trendmicro/tlsh"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fuzzy hashing with ssdeep and TLSH

**Goal:** find files that are *similar* (modified documents, recompiled malware variants)
where cryptographic hashes only find exact copies.

## ssdeep (context-triggered piecewise hashing)
```bash
ssdeep -r /cases/014/export/files > known.ssd        # hash a set
ssdeep -m known.ssd suspicious.bin                  # match against the set (score 0-100)
ssdeep -r -d /samples/                              # cluster: pairwise matches within a dir
ssdeep -r -p /samples/                              # pretty clusters
```
Score is a match strength, not a percentage similarity; >~50 is usually meaningful, but
calibrate per file type. Works best for files of similar size; poor on small files (< 4 KB)
and on compressed/packed content.

## TLSH (Trend Micro locality-sensitive hash)
```bash
tlsh -f a.exe          # hash (needs >= 50 bytes, more robust above a few hundred)
tlsh -c a.exe -f b.exe # distance: 0 = identical; lower = more similar (< ~100 often related)
```
Better resistance to small insertions and supports indexing for large corpora; VirusTotal
exposes both ssdeep and TLSH for samples.

## Uses in DFIR
- Find variants of a malware sample across collected binaries or a sample repository.
- Locate modified versions of a leaked document.
- Group web shells or scripts with small edits.
- Imphash and rich header complement fuzzy hashes for PE files.

## Limits
- Not admissible as proof of identity; only leads. Confirm similarity with diffing (bindiff,
  diffoscope) or manual analysis.
- Packing/encryption destroys similarity; hash the unpacked payload.

## Verify
Test on a known pair (original document and an edited copy) to confirm thresholds in your
environment before relying on results.
