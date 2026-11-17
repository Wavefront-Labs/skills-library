---
id: computing-software.digital-forensics-incident-response.evidence-handling.imaging-with-guymager
name: imaging-with-guymager
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [guymager, disk-imaging, forensic-acquisition, ewfacquire, dfir]
level: practitioner
status: draft
description: "Acquire drives with Guymager: device identification, E01/AFF/dd options, case metadata, split size, dual verification and reading the .info log."
sources: ["https://guymager.sourceforge.io/", "https://github.com/libyal/libewf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Imaging with Guymager

**Goal:** fast, multi-threaded acquisition on Linux forensic distributions (CAINE, Tsurugi,
Paladin bundles alternatives) with built-in verification and a reportable log.

## Workflow
1. Launch with root privileges (`sudo guymager`); devices list shows model, serial, size, and
   whether HPA/DCO is detected.
2. Right-click the source > **Acquire image**.
3. Format: **Expert Witness Format (E01)** with case number, evidence number, examiner,
   description, notes (stored in the E01 header); or Linux dd raw; or AFF (deprecated).
4. Split size: e.g. 2 GiB (FAT32 targets need < 4 GiB) or 0 for single file on ext4/NTFS/exFAT.
5. Hash: tick MD5 and SHA-256; tick **Verify image after acquisition** and **Re-read source
   after acquisition** (dual verification compares source re-read and image read-back).
6. Destination on a separate evidence drive.

## Output
- `<name>.E01...` segments and `<name>.info`: device details, hashes calculated during
  acquisition, verification hashes, bad sectors, duration. Keep `.info` with the image and in the case record.

## Configuration
- `/etc/guymager/guymager.cfg` (or local cfg) controls compression level (`EwfCompression`),
  thread count, and whether devices are shown read-only; check it is the distribution default
  you validated.

## Gotchas
- Guymager does not write-block by itself; use a hardware write blocker or a distribution that sets devices read-only.
- Bad sectors are filled with zeros and listed in `.info`; report them.
- "Re-read source" on a failing drive adds stress; disable for damaged media and use ddrescue instead.

## Verify
`.info` shows matching acquisition and verification hashes; `ewfverify` on the evidence store copy passes.
