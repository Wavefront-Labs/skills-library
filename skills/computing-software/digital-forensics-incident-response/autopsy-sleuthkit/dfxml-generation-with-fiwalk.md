---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.dfxml-generation-with-fiwalk
name: dfxml-generation-with-fiwalk
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [fiwalk, the-sleuth-kit, dfxml, file-inventory, dfir]
level: practitioner
status: draft
description: "Produce Digital Forensics XML inventories with fiwalk: every file's metadata and byte runs, hashing, ARFF/CSV output, and diffing images with idifference."
sources: ["https://github.com/sleuthkit/sleuthkit/tree/develop/tools/fiwalk", "https://github.com/dfxml-working-group/dfxml_python", "https://www.sleuthkit.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DFXML generation with fiwalk

**Goal:** generate a machine-readable inventory of every allocated and deleted file in an image -
names, inode, MACB times, sizes, hashes, and byte runs (physical locations) - for scripting,
comparison and reporting.

## Run
```bash
fiwalk -X image.xml image.dd                 # DFXML output
fiwalk -X image.xml -f image.E01             # -f: report file system type; works with E01 via TSK
fiwalk -z -M -X image.xml image.dd           # -z no metadata extraction from contents, -M MD5 (use -1 for SHA-1)
fiwalk -T image.dd                           # text output
```
(Check `fiwalk -h` for your build: options vary between the standalone and TSK-bundled versions.)
Each `<fileobject>` includes `filename`, `inode`, `alloc`/`unalloc`, `mtime/atime/ctime/crtime`,
`filesize`, `hashdigest`, and `<byte_runs>` with image offsets.

## Uses
- **Diff two images or snapshots** (before/after, two VSS stores):
```bash
python idifference.py --summary before.xml after.xml      # dfxml_python tools: new, deleted, renamed, modified files
```
- Map a carved block or a YARA hit offset back to the file containing it (byte runs).
- Feed hashes into NSRL/known-bad filtering scripts; build custom reports with `dfxml` Python library.
- Exchange inventories with other labs in a tool-neutral format.

## Gotchas
- Large images produce very large XML; stream-parse (dfxml `iterparse`) rather than loading into memory.
- Hashing every file is slow; start without `-M` if you only need metadata.

## Verify
Spot-check several `<fileobject>` entries against `istat` output for the same inode.
