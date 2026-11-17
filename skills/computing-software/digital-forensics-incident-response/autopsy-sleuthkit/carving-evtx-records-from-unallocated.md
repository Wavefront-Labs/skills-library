---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.carving-evtx-records-from-unallocated
name: carving-evtx-records-from-unallocated
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [evtx-carving, file-carving, windows-event-logs, log-clearing, dfir]
level: advanced
status: draft
description: "Carve Windows EVTX chunks and records from unallocated space, memory and pagefile after logs were cleared or rolled, then parse and validate them."
sources: ["https://github.com/libyal/libevtx/blob/main/documentation/Windows%20XML%20Event%20Log%20(EVTX).asciidoc", "https://github.com/williballenthin/EVTXtract", "https://github.com/omerbenamram/evtx"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carving EVTX records from unallocated space

**Goal:** after `wevtutil cl Security` (event 1102) or normal rollover, old event records often
remain in unallocated clusters, VSS, pagefile or memory. Carving recovers them.

## EVTX structure
- File header `ElfFile\x00`; 64 KiB **chunks** with header `ElfChnk\x00`; records with magic
  `**\x00\x00` (0x2A2A0000), record number, FILETIME, and BinXML. Chunks are self-contained
  (string and template tables inside), so a carved chunk parses on its own.

## Carving
```bash
blkls -o <off> image.dd > unalloc.bin          # unallocated clusters of the volume
# EVTXtract: finds chunks and also orphan records whose templates must be recovered
evtxtract unalloc.bin > carved.xml
# bulk_extractor evtx scanner / generic: carve ElfChnk chunks
bulk_extractor -E evtx -o be_out unalloc.bin
# parse carved chunks with a tolerant parser
evtx_dump -o jsonl be_out/evtx/*.evtx > carved.jsonl     # omerbenamram/evtx
```
- Also run against `pagefile.sys`, `hiberfil.sys` (decompressed), memory images, and VSS-extracted older `.evtx` files.

## Validation and deduplication
- Deduplicate by (Channel, EventRecordID, TimeCreated, Computer) against the current logs.
- Record numbers form sequences: carved records filling a gap in the live log's record numbers support that the gap was cleared.
- Orphan records rebuilt with guessed templates may mis-assign fields: verify key fields in hex.

## Gotchas
- Chunk checksums may fail for partially overwritten chunks; tolerant parsers still extract records - flag them.
- SSDs with TRIM leave little unallocated data; memory and VSS are then better sources.

## Verify
Carved events are deduplicated, flagged as carved in the timeline, and key ones verified at byte level.
