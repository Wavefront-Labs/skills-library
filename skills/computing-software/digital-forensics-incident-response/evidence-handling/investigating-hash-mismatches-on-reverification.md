---
id: computing-software.digital-forensics-incident-response.evidence-handling.investigating-hash-mismatches-on-reverification
name: investigating-hash-mismatches-on-reverification
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hash-mismatch, hash-verification, evidence-integrity, disk-imaging, dfir]
level: advanced
status: draft
description: "Diagnose a hash mismatch between acquisition and re-verification: failing media, write-blocker issues, live acquisition, wrong scope, and how to document it."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.cftt.nist.gov/", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Investigating hash mismatches on re-verification

**Goal:** a mismatch is not automatically evidence tampering. Find the cause, document it, and
decide whether the evidence is still usable.

## Common causes
| Cause | Signature |
|---|---|
| Live system / mounted volume acquisition | Source hash differs every time; image is internally consistent |
| Failing media (bad sectors returning different data) | Acquisition log shows read errors; ddrescue map has bad areas |
| Write blocker not in path / OS wrote to drive | Changed sectors in filesystem metadata, journal, or `System Volume Information` |
| Different scope | Hashing whole disk vs a partition; HPA/DCO revealed on one pass only |
| E01 hash vs raw stream | Comparing hash of the .E01 container file with the media hash stored inside |
| Image segment corrupted in transfer/storage | `ewfverify` reports CRC errors in specific chunks |
| SSD background garbage collection / TRIM on power | Small differences in unallocated areas between two acquisitions of the same SSD |

## Diagnose
```bash
ewfverify -v image.E01             # recompute and compare to stored hash; reports chunk CRC errors
ewfinfo image.E01                  # acquisition hashes, errors, media size
cmp -l a.dd b.dd | head            # byte offsets that differ between two acquisitions
```
Map differing offsets to filesystem structures (`ifind -d <block>`, `fsstat`) to see what changed.

## Decide and document
- Record both hashes, the cause analysis, which artefacts lie in affected areas, and whether
  conclusions rely on them. Most findings remain valid if differing sectors are unrelated.
- If the original is available and stable, re-acquire and hash twice.
- Never "fix" a mismatch by re-hashing the image and overwriting the recorded value.

## Gotchas
- Verification hashes of the source taken *after* imaging (dc3dd `verb=on`) on failing drives often differ; expected.
- Live memory images can never be re-verified against the source.

## Verify
The report states the mismatch, cause, affected areas and the impact on findings.
