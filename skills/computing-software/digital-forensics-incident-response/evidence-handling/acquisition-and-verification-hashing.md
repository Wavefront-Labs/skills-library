---
id: computing-software.digital-forensics-incident-response.evidence-handling.acquisition-and-verification-hashing
name: acquisition-and-verification-hashing
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hash-verification, hashing, evidence-integrity, sha256, ewfverify, dfir]
level: practitioner
status: draft
description: "Hash forensic images at acquisition and verify them later: acquisition vs verification hashes, E01 internal hashes, ewfverify, manifests and what to do on mismatch."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://github.com/libyal/libewf/wiki"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acquisition and verification hashing

**Goal:** prove the image you analyse is bit-for-bit what you acquired, and that it matches
the source at acquisition time.

## Two hashes, two meanings
- **Acquisition (source) hash**: computed over data as read from the source during imaging.
- **Verification hash**: recomputed over the written image afterwards. Match = image
  faithfully written. Source re-hash after imaging (if the source is still available and
  write-blocked) proves the source did not change.

## Tools
```bash
# raw image with dc3dd: hashes while imaging, logs to file
dc3dd if=/dev/sdb of=evid001.dd hash=sha256 hash=md5 log=evid001.log
sha256sum evid001.dd                         # verification
# E01: hashes stored in the image (MD5 and optional SHA1/SHA256)
ewfacquire -d sha256 /dev/sdb               # prompts for case info
ewfverify evid001.E01                       # recomputes and compares stored hash
ewfinfo evid001.E01                         # shows stored hashes and acquisition metadata
# Windows
Get-FileHash -Algorithm SHA256 .\evid001.dd
```
FTK Imager writes a `.txt` report with computed and verified hashes; keep it with the image.

## Manifest
For every case keep `manifest.sha256` (`sha256sum *.E01 *.dd > manifest.sha256`) in the
evidence folder and verify (`sha256sum -c manifest.sha256`) before analysis and before
transfer.

## On mismatch
- Image vs its own verification: re-copy from the master or re-acquire; investigate the
  storage (bad sectors, failing USB enclosure).
- Source re-hash differs: failing drive (bad sectors read differently), or the source was
  live/changing (live system, SSD background garbage collection). Document; this is expected
  for live acquisitions, which have no repeatable source hash.
- Bad sectors: imaging tools fill unreadable sectors with zeros and log them; record the
  sector list.

## Verify
Report lists algorithm, value, tool and version, time for acquisition and verification
hashes, and any bad-sector log.
