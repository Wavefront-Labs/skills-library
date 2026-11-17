---
id: computing-software.cybersecurity-defensive.security-operations.file-metadata-analysis
name: file-metadata-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [file-metadata-analysis, investigation-data-sources, exiftool, pe-analysis, mark-of-the-web, digital-forensics, timestamps]
level: practitioner
status: draft
description: "Analyse file metadata in investigations: filesystem timestamps, PE headers and signatures, Office/PDF metadata, EXIF, Zone.Identifier mark-of-the-web and hashes."
sources: ["https://exiftool.org/", "https://learn.microsoft.com/en-us/windows/win32/debug/pe-format", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/6e3f7352-d11c-4d76-8c39-2516a9df36e8"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# File metadata analysis

## Filesystem
- NTFS: $STANDARD_INFORMATION (MACB, user-modifiable via timestomping) vs $FILE_NAME timestamps
  (harder to alter). $SI earlier than $FN creation, or zeroed sub-seconds, suggests timestomping.
- Linux ext4: mtime, ctime, atime, crtime (`stat`, `debugfs -R 'stat <inode>'`).
- Copy vs move semantics change which timestamps update; interpret with care.

## Origin markers
- **Zone.Identifier** ADS (mark of the web): `Get-Content file.exe -Stream Zone.Identifier` shows
  `ZoneId=3` plus `ReferrerUrl`/`HostUrl` - where the file was downloaded from.
- macOS `com.apple.quarantine` and `kMDItemWhereFroms` xattrs (`xattr -l`, `mdls`).

## Executables
- PE header: compile timestamp (can be faked, but useful for clustering), imphash, sections and
  entropy, Rich header, PDB path (developer usernames/project names), version info.
  Tools: `pefile`, `pecheck`, `Detect It Easy`, `sigcheck -a -h`.
- Authenticode signature: signer, certificate validity, counter-signature timestamp; signed by
  stolen or revoked certificates is common.

## Documents and images
- `exiftool -a -G1 file.docx`: Author, LastModifiedBy, Company, Template, create/modify dates,
  application version. OOXML `docProps/core.xml` and `app.xml` directly.
- PDFs: Producer/Creator, XMP history; `pdfinfo`, `pdf-parser.py`.
- Images: EXIF GPS, camera model, software; often stripped by messaging apps.

## Hashes
SHA-256 for identity; ssdeep/TLSH for similarity; check reputation without uploading sensitive files.

## Gotchas
- All metadata is attacker-editable to some degree; corroborate with logs.
- Copying files to analysis systems can change timestamps; work on images or read-only copies.

## Verify
Findings record which metadata source supports each claim and whether it is corroborated by an
independent artefact.
