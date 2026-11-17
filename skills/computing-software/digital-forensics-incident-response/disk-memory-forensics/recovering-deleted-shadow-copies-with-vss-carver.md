---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.recovering-deleted-shadow-copies-with-vss-carver
name: recovering-deleted-shadow-copies-with-vss-carver
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [vss-carver, volume-shadow-copy, vss, anti-forensics, dfir]
level: advanced
status: draft
description: "Recover shadow copy stores deleted by ransomware or attackers using vss_carver: carving catalog and store blocks, rebuilding, and mounting with vshadowmount."
sources: ["https://github.com/mnrkbys/vss_carver", "https://github.com/libyal/libvshadow"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovering deleted shadow copies with vss_carver

**Goal:** `vssadmin delete shadows /all /quiet` removes the catalog, but store data blocks often
remain in unallocated space. vss_carver (Minoru Kobayashi) rebuilds them.

## Workflow
```bash
# 1. raw image of the volume (or full disk + offset)
mmls disk.dd
# 2. carve VSS catalog and store blocks; writes a carved catalog and store file
python vss_carver.py -t RAW -o $((206848*512)) -i disk.dd -c catalog.bin -s store.bin
# 3. optionally review/sort carved entries (vss_catalog_manipulator.py list / move / remove)
python vss_catalog_manipulator.py list catalog.bin
# 4. mount the carved stores with the patched libvshadow (vshadowmount supporting -c/-s)
vshadowmount -o $((206848*512)) -c catalog.bin -s store.bin disk.dd /mnt/vss_carved
ls /mnt/vss_carved          # vss1..N, mount each read-only as NTFS
```
- Use the libvshadow fork referenced by the vss_carver project, which accepts carved catalog/store files.

## Expectations
- Recovery is partial: overwritten store blocks produce corrupted files; validate every artefact (hash/structure).
- Ransomware that encrypted the volume after deleting shadows may have overwritten much of the unallocated space; but many families only encrypt file contents, leaving freed VSS blocks intact.

## Use
- Recover pre-encryption copies of files, registry hives, event logs and `$MFT` from before the attack.
- Timeline across recovered stores (see VSS timelining) to show attacker activity before deletion.

## Gotchas
- Carving is slow on large volumes; run on a copy of the image with plenty of disk space for output.
- Work only on images, never live volumes.

## Verify
Recovered stores mount, NTFS metadata parses, and key files open correctly before you rely on them.
