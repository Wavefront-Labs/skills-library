---
id: creative-arts.graphic-design.adobe-indesign.live-captions-from-metadata
name: live-captions-from-metadata
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, live-captions, static-captions, caption-setup, xmp-metadata, image-credits, photo-credits, indesign-graphics]
level: practitioner
status: draft
description: "Generate InDesign captions and photo credits from image XMP metadata: Caption Setup, live vs static captions, caption variables, and filling metadata in Bridge or Lightroom."
sources:
  - https://helpx.adobe.com/indesign/using/captions.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live captions from metadata

**Goal:** captions and credits that come from the image files themselves, so a catalogue or photo book
gets accurate text without retyping.

## 1. Put the metadata in the images
- In Adobe Bridge (File Info) or Lightroom, fill **Title**, **Description**, **Creator**, **Copyright Notice**,
  Headline, Credit Line. Use metadata templates for shared credits.
- Save. InDesign reads XMP from PSD, TIFF, JPEG, AI and PDF.

## 2. Caption Setup
- Object > Captions > **Caption Setup**:
  - **Metadata Caption:** text before, metadata field (Description, Creator, ...), text after. Add rows for
    several fields (`Photo: <Creator>`).
  - **Position:** below, above, left or right of the image; offset.
  - **Paragraph Style** for the caption, **Layer**, and Group Caption with Image.

## 3. Make captions
- Select images, Object > Captions > **Generate Live Caption** (updates when metadata or the link changes)
  or **Generate Static Caption** (plain text, editable, does not update).
- Captions on place: in the Place dialog check **Create Static Captions**.
- Live caption text is a **caption variable** (Type > Text Variables > Define > Metadata Caption); one
  variable cannot break across lines, so long descriptions need static captions.

## 4. Edit
- Right-click a live caption > **Convert to Static Caption** to edit wording.
- Missing metadata shows `<No data from link>` in live captions; preflight or search for it.

## Gotchas
- Live captions update from the image the frame is linked to; if the caption frame is moved away from
  the image (not grouped and not touching), it shows the wrong or no data.
- Static captions do not update when images are replaced; regenerate them at final stage.
- Fill metadata at source: InDesign cannot write XMP back to the image.

## Verify
- [ ] Every caption shows real text (search for `No data from link`).
- [ ] Credits match the licence terms for each image.
