---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.extracting-files-from-smb-traffic
name: extracting-files-from-smb-traffic
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [smb-file-extraction, export-objects, smb2, wireshark, tshark, lateral-movement, file-carving, dfir]
level: practitioner
status: draft
description: "Recover files transferred over SMB2/3 from packet captures with Wireshark Export Objects and tshark --export-objects, and verify completeness and hashes."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html", "https://www.wireshark.org/docs/man-pages/tshark.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exporting SMB transferred files

**Goal:** pull tools, payloads and stolen documents out of SMB traffic in a pcap (lateral
movement via admin shares, data staging to file servers).

## Wireshark
File > Export Objects > **SMB...** lists each file: packet, hostname, content type
(`FILE (n/m) W [xx%]` shows read/write and how much of the file was captured), size, filename.
Select and Save, or Save All.

## tshark (scriptable)
```bash
mkdir smb_out
tshark -r capture.pcapng -q --export-objects smb,smb_out
sha256sum smb_out/* > smb_out.sha256
```
Also available for `http`, `imf` (email), `tftp`, `dicom`, `ftp-data`.

## Find what was transferred first
```
smb2.cmd == 5 && smb2.filename                      # CREATE requests with filenames
smb2.cmd == 9                                       # WRITE (to the server): uploads
smb2.cmd == 8                                       # READ: downloads
smb2.tree contains "ADMIN$" || smb2.tree contains "C$"
smb2.filename matches "(?i)\\.(exe|dll|ps1|bat|zip|7z|rar)$"
```
Statistics > Conversations (TCP 445) shows which host pairs moved the most data.

## Completeness
- Export Objects reports partial percentages; a file < 100% will be truncated or contain
  zero-filled gaps (missing reads/writes, capture drops). Hash and analyse anyway but mark it
  partial.
- SMB 3 **encryption** (`smb2.flags` with transform header, `SMB2_TRANSFORM` / protocol ID
  `0xFD 'S' 'M' 'B'`) hides content; you need the session key (from the server or memory) to
  decrypt: Preferences > Protocols > SMB2 > Secret session keys.
- SMB signing does not prevent extraction.
- Compressed SMB 3.1.1 transfers may need recent Wireshark versions.

## Tie to host artefacts
Match exported filename and hash with host evidence: `\\host\ADMIN$\<name>.exe` service
creation (7045), file creation in `\Windows\` on the target, 5145 share access events.

## Self-check
Every exported file has a hash, a source/destination host, a direction (read vs write), a time
and a completeness percentage.
