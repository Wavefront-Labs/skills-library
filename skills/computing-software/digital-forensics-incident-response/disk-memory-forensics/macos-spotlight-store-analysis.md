---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-spotlight-store-analysis
name: macos-spotlight-store-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [spotlight-forensics, spotlight, macos-forensics, mdutil, spotlight-parser, dfir]
level: advanced
status: draft
description: "Analyse the macOS Spotlight store: locations of .Spotlight-V100 and per-user stores, parsing store.db with spotlight_parser, useful metadata attributes, and deleted-file evidence."
sources: ["https://github.com/ydkhatri/spotlight_parser", "https://github.com/ydkhatri/mac_apt", "https://developer.apple.com/documentation/coreservices/file_metadata/mditem/common_metadata_attribute_keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS Spotlight store analysis

Spotlight indexes file metadata (and some content) into databases that persist after files are deleted until the index entry is purged. It can show files that once existed, where they came from, and when they were last used.

## Locations
- Volume store: `/System/Volumes/Data/.Spotlight-V100/Store-V2/<UUID>/` (Catalina and later; older: `/.Spotlight-V100`). Key files: `store.db` and `.store.db`.
- Per-user stores: `~/Library/Metadata/CoreSpotlight/` (app-donated items such as Mail, Messages, Notes) and `~/Library/Caches/com.apple.helpd/`.
- External volumes have their own `.Spotlight-V100` unless indexing was disabled (`mdutil -s /Volumes/X`).

## Parsing
`spotlight_parser.py` (Yogesh Khatri) reads `store.db` offline:
```bash
python spotlight_parser.py /case/Store-V2/<UUID>/store.db /case/out -p
```
Outputs a TSV of every indexed item with its attributes and a reconstructed path where the parent chain resolves. mac_apt includes a SPOTLIGHT plugin that runs across volume and user stores.

## Attributes worth reading
| Attribute | Meaning |
|---|---|
| `kMDItemWhereFroms` | Download source URL and referrer |
| `kMDItemLastUsedDate` / `_kMDItemLastUsedDate_Ranking` | Last opened via Launch Services |
| `kMDItemUseCount` / `kMDItemUsedDates` | Open count and dates |
| `kMDItemDateAdded` | When placed in its folder |
| `kMDItemFSCreationDate`, `kMDItemContentModificationDate` | File system times at index time |
| `kMDItemDisplayName`, `_kMDItemFileName` | Name, even if the file is gone |
| `kMDItemAuthors`, `kMDItemTextContent` (if content indexed) | Document metadata/content |

## Investigative uses
- Files on removable media that were opened and later removed (index entries on the Mac volume or the stick's own store).
- Downloaded tools and their source URL after deletion (cross-check with quarantine events).
- Evidence of documents a departing employee viewed.

## Live system
`mdls <file>` shows attributes for existing files; `mdfind 'kMDItemWhereFroms == "*example.com*"'` queries the live index. Live querying requires TCC access and changes nothing on disk, but collect the raw store for the record.

## Gotchas
- Store format changes across macOS versions; use a parser updated for the source OS.
- Index entries without a resolvable parent show only an inode/ID; correlate with FSEvents for the path.
- Users can exclude folders (Privacy list in `VolumeConfiguration.plist`); missing entries may be configuration, not deletion.

## Verify
Items you report from Spotlight are corroborated by another source (FSEvents, quarantine events, KnowledgeC) or flagged as Spotlight-only.
