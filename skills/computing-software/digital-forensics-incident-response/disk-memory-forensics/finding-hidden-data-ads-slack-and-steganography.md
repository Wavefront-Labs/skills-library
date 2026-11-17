---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.finding-hidden-data-ads-slack-and-steganography
name: finding-hidden-data-ads-slack-and-steganography
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [steganography, alternate-data-streams, file-slack, hidden-data, anti-forensics, stegdetect, zsteg, dfir]
level: practitioner
status: docs-checked
description: "Find data hidden in NTFS alternate data streams, file slack (blkls -s) and PNG/BMP steganography (zsteg), and know which detections are leads rather than conclusions."
sources: ["https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/c54dec26-1551-4d3a-a0ea-4fa40f848eb3", "https://www.sleuthkit.org/sleuthkit/man/blkls.html", "https://github.com/zed-0xff/zsteg"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden data: ADS, slack and steganography

**Goal:** systematically check the places data hides on a seized system and record each finding with its location and provenance.

## NTFS alternate data streams
- Every NTFS file has at least the main stream. A stream's full name is `<filename>:<stream name>:<stream type>`; the default data stream has no name, so `sample.txt::$DATA` is the normal content. A named stream such as `sample.txt:bar:$DATA` holds separate data. Any legal file name characters, including spaces, are legal in a stream name.
- Directories have a default `$I30` stream of type `$INDEX_ALLOCATION` and can also carry named data streams. Alternate data streams are not normally visible but can be seen with `dir /R` on the command line.
- Check every file or directory with a named `$DATA` stream; judge by stream name, size and content. Extract the stream and hash it as evidence.

## File slack
`blkls` (The Sleuth Kit) copies file system data units. By default it copies unallocated blocks; `-s` copies only the slack space; `-e` copies every block; `-a` allocated and `-A` unallocated; `-o` gives the sector offset of the file system in the image; `-f` and `-i` set file system and image type (autodetected if omitted). Examples: `blkls -s -o <SECTOR_OFFSET> image.dd > slack.raw` then search the output with your usual string and carving tools.

## Steganography (least common, hardest)
- Look first for tool evidence: steganography programs installed or executed, downloads, and pairs of near-identical images with different hashes. This is more reliable than statistical detection.
- `zsteg` detects hidden data in PNG and BMP: LSB steganography, zlib-compressed data, OpenStego, Camouflage 1.2.1, and LSB with the Eratosthenes set. `zsteg -a file.png` tries all known methods; `zsteg -E <NAME> file.png` extracts a payload by the name shown in the results (for example `1b,rgb,lsb`). Its analysis limit defaults to 256 bytes (`-l 0` removes it).
- A zsteg hit is a lead; confirm by extracting the payload and identifying it.

## Not covered by the cited pages
Hidden partitions, HPA/DCO and encrypted container detection were removed from this skill because the sources do not cover them; consult tool documentation (disk partition tools, vendor ATA references) before relying on any procedure.

## Self-check
For every hidden-data finding you have the location (stream, offset, block), extracted content with hash, and the tool or user action that put it there.

## Checked
2026-11-08. Confirmed against Microsoft MS-FSCC section 5.1 (NTFS streams), the blkls man page and the zsteg README. Removed as unconfirmed: MFTECmd columns, istat/icat inode syntax, benign stream names, mmls/dd/hdparm/gdisk steps, entropy heuristics, stegseek, steghide, binwalk, foremost and detector false-positive claims, and image end marker values.
Method: documentation only; no commands were run.
