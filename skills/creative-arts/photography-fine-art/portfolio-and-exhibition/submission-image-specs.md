---
id: creative-arts.photography-fine-art.portfolio-and-exhibition.submission-image-specs
name: submission-image-specs
category: creative-arts
field: photography-fine-art
product: portfolio-and-exhibition
tags: [portfolio-and-exhibition, submission-image-specs, open-calls, file-naming, srgb-export, callforentry]
level: practitioner
status: draft
description: "Prepare image files for submissions and open calls: pixel dimensions, file size, colour space, naming, metadata, PDFs and checking a platform's rendering."
sources: ["https://www.callforentry.org/", "https://www.slideroom.com/", "https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Submission image specs

## Follow the call exactly
Pixel dimensions, file size limit, format, naming and number of images are often checked automatically or by a coordinator; non-compliant entries are skipped.

## Defaults when the call gives none
- JPEG, **sRGB**, quality 80-90.
- **1920 px on the long side** (CaFE recommends at least 1200 px; many platforms accept up to 3000-5000 px and 5 MB).
- 72-300 ppi metadata is irrelevant for screens; pixel dimensions matter.
- No borders, watermarks, signatures or text on the image unless requested.

## Naming
- Use the call's pattern; otherwise `Lastname_Firstname_01_Title.jpg` with two-digit numbers matching the image list/sequence.
- No spaces or special characters for web uploads.

## Metadata
- Embed title, year and copyright in IPTC; some platforms show it. Strip GPS for sensitive locations.

## Image list
- Number, title, year, medium, dimensions (as exhibited, framed), edition, price if requested. Match numbering to filenames.

## PDF portfolios
- One image per page at fixed size, statement on page 1, compressed to under the limit (Acrobat: Reduce File Size or export at 150-200 ppi equivalent).

## Check
- Upload and view in the platform's preview; some platforms recompress or convert colour. Upload in sRGB to avoid dull colour.
- Lightroom: make an export preset per platform ("CaFE 1920 sRGB").

## Verify
- [ ] Each file meets the stated pixel and size limits, opens with sRGB profile, and names match the image list numbering.
