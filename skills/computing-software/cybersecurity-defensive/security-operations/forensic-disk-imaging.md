---
id: computing-software.cybersecurity-defensive.security-operations.forensic-disk-imaging
name: forensic-disk-imaging
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, disk-imaging, write-blocker, hash-verification, chain-of-custody, bit-stream-image]
level: advanced
status: docs-checked
description: "Acquire a forensically sound bit-stream disk image with write blocking, before-and-after hash verification and documentation, per NIST SP 800-86 principles."
sources: ["https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forensic disk imaging

**Goal:** a bit-for-bit copy of a disk that you can prove is unchanged, acquired without
altering the original. Principles below come from NIST SP 800-86 (2006); check your tool
vendor's documentation for exact commands and your jurisdiction's evidence rules.

## Decide first
- Logical backup or bit stream image? A bit stream image is a bit-for-bit copy including free and slack
  space; it needs more storage and time than a logical backup. If evidence may be needed for prosecution
  or disciplinary action, take a bit stream image.
- Volatile first: for a live system, acquiring volatile data should generally take priority over
  non-volatile data (SP 800-86). Capture memory before shutdown.
- Disk-to-disk copy: contents can be viewed directly but needs a second, similar medium. Disk-to-file:
  easy to move and back up, but needs a tool able to read or restore the image.

## Acquisition steps
1. Label the original medium and record model, serial number and capacity.
2. Use a write-blocker (hardware or software) so the original cannot be written to: connect the medium to
   the write-blocker and the write-blocker to the imaging computer, with write blocking on for every
   attached device.3. Compute and record a message digest of the original **before** imaging.
4. Create the image with your forensic tool.
5. Compute the digest of the copy and compare with the original; then compute the original again to show the
   imaging did not alter it. Document all results. (SP 800-86 predates current guidance on hash algorithms:
   use a current approved algorithm rather than MD5 or SHA-1.)
6. Store the original securely as evidence; do all analysis on a copy.
7. Document every step so another analyst could reproduce the duplicate: hardware and software used with
   name, version and licence information, times, and examiner. This supports chain of custody.

## Gotchas
- Destination media must be able to hold the source; use new or forensically wiped media.
- Never mount evidence read-write.
- A hash mismatch on re-verify means the copy or the source changed: investigate and document, do not
  silently re-image.

## Verify
- [ ] Source and image digests recorded and matching (or the discrepancy explained).
- [ ] Chain of custody form signed for the original and the image.
- [ ] A working copy is used for analysis; the master image is stored read-only.

## Checked
2026-11-01. Confirmed in NIST SP 800-86 (sections on bit stream imaging, write-blockers, message digests,
volatile data priority, documentation and chain of custody). Removed: ewfacquire, dc3dd, ewfverify, FTK
Imager, ddrescue and mount commands, KAPE/Velociraptor and cloud snapshot procedures, TRIM and WAN-speed
claims, E01 format claims. CFTT tool-testing claim removed (page not read).
Method: documentation only; no commands were run.
