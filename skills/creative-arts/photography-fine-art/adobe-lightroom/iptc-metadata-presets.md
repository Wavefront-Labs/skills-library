---
id: creative-arts.photography-fine-art.adobe-lightroom.iptc-metadata-presets
name: iptc-metadata-presets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, iptc-metadata, lightroom-library, metadata-presets, copyright-metadata, iptc-core, lightroom-classic]
level: practitioner
status: draft
description: "Create IPTC metadata presets in Lightroom Classic for copyright, creator contact and rights usage, apply them at import, and check what Export writes."
sources: ["https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata", "https://helpx.adobe.com/lightroom-classic/help/photo-video-import-options.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Metadata basics and actions)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPTC metadata presets

## Build the preset
Metadata panel > Preset > **Edit Presets...** Fill only what is constant; leave per-image fields (Headline, Caption, Location) blank or unticked so they do not overwrite.
- **IPTC Copyright**: Copyright = `(c) 2026 Firstname Lastname. All rights reserved.`; Copyright Status = Copyrighted; Rights Usage Terms = `No use without written licence. Contact name@example.com`; Copyright Info URL = your licensing page.
- **IPTC Creator**: Creator, Job Title, Address, City, Country, Phone, Email, Website. Copyright Office and image-search tools read these.
- Optional: **IPTC Image** > Credit Line (how the credit should read), Source.
Save as `Copyright YYYY` and make a new one each January (the year matters for registration records).

## Apply
- At import: Apply During Import > Metadata.
- Afterwards: select photos > choose the preset in the Metadata panel. Ticked fields overwrite; empty ticked fields **clear** existing values.
- Edit per image with the Metadata panel set to "IPTC" or "Location" view; captions via the Caption field (shows as Description in IPTC).

## Export control
Export dialog > Metadata > Include: **Copyright Only**, Copyright & Contact Info Only, All Except Camera Raw Info, All Except Camera & Camera Raw Info, or All Metadata. Tick Remove Person Info / Remove Location Info to strip faces and GPS for public sharing.

## Gotchas
- Social platforms strip most IPTC; the metadata still matters for files sent to galleries, press and registration.
- Metadata changes are not written to raws until saved to XMP (Ctrl/Cmd+S, or auto-write in Catalog Settings).

## Verify
- [ ] `exiftool -IPTC:all -XMP-dc:all exported.jpg` shows copyright, creator and rights terms.
