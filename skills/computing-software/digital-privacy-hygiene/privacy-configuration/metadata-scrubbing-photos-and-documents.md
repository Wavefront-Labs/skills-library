---
id: computing-software.digital-privacy-hygiene.privacy-configuration.metadata-scrubbing-photos-and-documents
name: metadata-scrubbing-photos-and-documents
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, exif, gps-metadata, geotagging, document-metadata, exiftool, metadata-removal, pdf-metadata, photo-sharing, hidden-metadata]
level: intro
status: docs-checked
description: "Strip GPS and other metadata from photos with ExifTool before sharing, verify the result, and know that ExifTool cannot truly remove metadata from PDFs."
sources:
  - "https://exiftool.org/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata scrubbing: photos and documents

**Goal:** remove location, device and authorship metadata from a file before sharing it publicly, and confirm the
removal instead of trusting a tool's claim.

## What files carry
ExifTool reads and writes EXIF, GPS, IPTC, XMP, JFIF, MakerNotes, ICC profiles and many other metadata groups, and can
read timed GPS tracks embedded in MOV, MP4, M2TS and AVI video. A photo straight from a phone or camera can therefore
carry GPS position, so share only a copy you have inspected.

## Remove and verify with ExifTool
1. Inspect first: `exiftool photo.jpg` lists everything it finds.
2. Strip: `exiftool -all= photo.jpg` deletes all meta information. When writing, ExifTool keeps the original by adding
   `_original` to its file name. Keep a copy of the original, or validate the new file thoroughly, before erasing it.
   Share the cleaned file, never the `_original`.
3. Verify: run `exiftool photo.jpg` on the cleaned file and confirm the GPS and device tags are gone.
4. `-GROUP:all=` deletes one group only, for example when you want to keep colour profiles but drop GPS.

## PDFs are different
ExifTool's documentation states that changes to PDF files are reversible because the original metadata is never
actually deleted from them, so `exiftool -all=` on a PDF does not give you a clean file. For a PDF that must not leak
authorship or hidden content, use a tool that rewrites the file (for example printing or exporting to a fresh PDF) and
test the output. See also the sibling skill on properly redacting PDFs.

## Gotchas
- Platform behaviour (whether a social app, messenger or marketplace strips EXIF on upload) is not documented by the
  cited page and changes without notice. Test with your own upload and download round trip for anything sensitive.
- Email attachments and cloud share links send the file you attach, so clean the file before attaching it.
- Office documents carry author and revision data. Use the application's own document inspection feature and then
  verify the result yourself; the menu paths are not covered by the cited sources.

## Verify
- [ ] The file you share is not the original and `exiftool` on it shows no GPS or device tags.
- [ ] A PDF was rewritten, not just passed through `exiftool -all=`.

## Checked
Checked 2026-11-08 against the ExifTool home page: supported metadata groups, GPS in video, `_original` backup
behaviour, `-all=` and `-GROUP:all=` syntax, and the statement that PDF changes are reversible. Corrected: the old
skill called `exiftool -all=` on a PDF a verifiable strip, which the page contradicts. Removed: per-platform stripping
claims (Instagram, Facebook, X, WhatsApp, iMessage, Signal), OS and Office menu paths, `-overwrite_original` advice
and the EFF Deeplinks source (a blog index), none of which the cited page states.
Method: docs-only read of cited pages, 2026-11-08
