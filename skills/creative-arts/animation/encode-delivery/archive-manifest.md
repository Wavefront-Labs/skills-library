---
id: creative-arts.animation.encode-delivery.archive-manifest
name: archive-manifest
category: creative-arts
field: animation
product: encode-delivery
tags: [archive-manifest, archive, archiving, project-archive, inventory, metadata, json, deliverables-inventory, retention, python]
level: practitioner
status: docs-checked
description: "Write a project archive manifest for an animated production: BagIt bag layout and fixity, bag-info metadata, plus an inventory file for software, rights, retention."
sources:
  - https://datatracker.ietf.org/doc/html/rfc8493
  - https://github.com/LibraryOfCongress/bagit-python
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project archive manifest

**Goal:** a person who never worked on the show can find, understand and reuse anything in the archive. Checksums prove bits are intact; the manifest says what the bits are.

## Bag structure (RFC 8493, BagIt)

A bag is a directory holding the payload in `data/`, a payload manifest named `manifest-<algorithm>.txt` (for example `manifest-sha256.txt`), and a `bagit.txt` declaration, plus optional tag files such as `bag-info.txt` and tag manifests `tagmanifest-<algorithm>.txt`.

- `bagit.txt` has exactly two lines, the version and the tag-file encoding (UTF-8 recommended).
- `bag-info.txt` holds human-oriented metadata; defined elements include Contact-Name, Bagging-Date (YYYY-MM-DD), Bag-Size and Payload-Oxum (octetstream sum of the payload).
- Implementations must support SHA-256 and SHA-512; the spec recommends also supporting MD5 and SHA-1 for compatibility.

Illustrative production layout (a convention, not part of BagIt) inside `data/`:

```
data/
  00_docs/     bible, credits, licences, cue sheets
  01_masters/  picture, textless, stems, timed text per episode
  02_edit/     AAF, OTIO, EDL, final project per episode
  03_assets/   characters, props, sets
  04_shots/    scene files and caches worth keeping
  05_colour/   OCIO config, LUTs, CDLs
  06_tools/    pipeline code at the tagged release, environment specs
  archive.json
```

## Creating and validating the bag (bagit-python)

`pip install bagit`, then `python -m bagit` (or `bagit.py`) turns an existing directory into a bag. Key/value options such as `--contact-name` are written to `bag-info.txt`; `--sha256` (also `--md5`, `--sha1`, `--sha512`) chooses manifest algorithms; `--processes N` calculates checksums in parallel; `--validate` validates a bag, with `--fast` for a quicker check.

```
python -m bagit --contact-name "Studio Archive" --sha256 SHOW_S01_ARCHIVE
python -m bagit --validate SHOW_S01_ARCHIVE
```

Write `archive.json` into the directory before bagging so the payload manifest covers it.

## archive.json (project convention)

BagIt does not define production metadata, so record it in your own JSON file, for example:

```json
{
  "production": "SHOW", "season": 1, "archived": "2026-11-09", "archivist": "<NAME>",
  "rights": {"owner": "<RIGHTS_HOLDER>", "music_restrictions": "see 00_docs/cue_sheets", "font_licences": "00_docs/fonts"},
  "software": {"blender": "<VERSION>", "ocio_config": "<CONFIG>", "resolve": "<VERSION>"},
  "episodes": [{"ep": "S01E01", "picture_master": "01_masters/S01E01/<FILE>", "edit": "02_edit/S01E01/<FILE>",
                 "frame_rate": "24/1", "audio": ["printmaster_51", "stereo", "me_51"]}],
  "retention": {"review_by": "<DATE>"}
}
```

Generate the episode list from the production tracker rather than by hand.

## What usually gets lost (practitioner checklist)

- Font files and licences used in titles; music licence terms.
- The exact OCIO config and LUTs.
- Pipeline code version.
- Which version of each shot was final.

## Verify

Run `--validate` on the finished bag; then have a colleague locate episode 5's music-and-effects stem using only the manifest.

## Checked

Method: 2026-11-09 read RFC 8493 (structure, file names, bag-info elements, algorithm support) and the bagit-python README (CLI options). Removed the PREMIS source (landing page not read) and unstated specifics; the folder layout and JSON fields are marked as conventions.
