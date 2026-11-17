---
id: creative-arts.graphic-design.adobe-photoshop.assign-vs-convert-profile
name: assign-vs-convert-profile
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-color-management, color-modes, assign-vs-convert-profile, assign-profile, convert-to-profile, untagged-images, missing-profile, embed-profile, srgb]
level: practitioner
status: draft
description: "Know when to Assign a profile (reinterpret numbers) vs Convert to Profile (keep appearance) in Photoshop, and handle untagged or mismatched images."
sources:
  - https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assign vs convert profile

**Goal:** never accidentally change how an image looks when moving it between colour spaces.

## The difference
- **Edit > Assign Profile:** keeps the pixel **numbers**, changes their **meaning** - so the
  **appearance changes**. Use only to correct a wrong or missing tag (tell Photoshop what the
  numbers really are).
- **Edit > Convert to Profile:** keeps the **appearance** (as closely as the destination gamut
  allows), changes the **numbers**. Use to move an image into another space (Adobe RGB -> sRGB
  for web, RGB -> printer CMYK).

Rule of thumb: **Convert** to change destination; **Assign** only to fix labelling.

## Untagged and mismatched images
- **Missing profile on open:** phone screenshots, web images and many stock JPEGs are untagged
  but almost always sRGB - choose "Assign working RGB: sRGB" or assign sRGB afterwards. Camera
  JPEGs set to Adobe RGB usually carry a tag or EXIF hint.
- **Embedded profile mismatch:** keep the embedded profile, or convert to your working space -
  both preserve appearance. Never "discard the embedded profile" unless you know it is wrong.
- **Client says colours look different in your file:** check whether one side assigned instead
  of converted; compare with Edit > Assign Profile preview toggling between candidate profiles.

## Exporting
- Web/screen: convert to sRGB and **embed** the profile (Export As: Convert to sRGB + Embed Color Profile).
- Print: deliver in the profile agreed with the printer, embedded.
- File > Save As: tick **Embed Color Profile** (ICC Profile) - untagged deliveries cause the same problem downstream.

## Gotchas
- Assigning Adobe RGB to an sRGB image makes it look oversaturated; the reverse makes it dull.
- Copying layers between documents with different profiles: Photoshop converts the pasted pixels
  by default (Edit > Paste preserves appearance). Dragging layers between differently tagged
  documents shows a profile mismatch warning in some versions - read it.

## Verify
- [ ] Document profile (status bar) is correct for the image's origin.
- [ ] Conversions done with Convert to Profile; profile embedded in every delivery.
