---
id: creative-arts.graphic-design.adobe-illustrator.placing-linked-and-embedded-images
name: placing-linked-and-embedded-images
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-linked-images, links-panel, place-image, embed, unembed, crop-image, effective-ppi, relink, package]
level: practitioner
status: draft
description: "Place images in Illustrator as links or embeds: the Links panel, relinking, effective resolution after scaling, Crop Image, unembedding and packaging links for handoff."
sources:
  - https://helpx.adobe.com/illustrator/using/importing-artwork-files.html
  - https://helpx.adobe.com/illustrator/using/managing-linked-embedded-images.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Placing, linking and embedding images

**Goal:** raster images in Illustrator layouts that stay light, update when the source changes, print at
the right resolution and travel with the file.

## Place
- File > **Place** (Ctrl/Cmd+Shift+P). **Link** checked = file references the image (default, recommended);
  unchecked = embedded copy. **Template** puts it on a dimmed locked layer. Multiple files load the place gun.
- Drag and drop from the desktop links by default; Alt/Option-drag embeds in some versions. Check Links panel.
- PSD options on place: convert layers to objects (embedded only) or flatten to a single image.

## Links panel (Window > Links)
- Shows each image, status icons (missing, modified), and info: **PPI** (effective), dimensions, scale,
  colour space, path.
- **Relink**, **Go To Link**, **Update Link**, **Edit Original** (opens in Photoshop; save and Illustrator
  updates).
- **Embed Image(s)** and **Unembed** (writes a PSD/TIFF out and links to it).

## Resolution
- Effective PPI = actual PPI / scale. A 300 ppi image scaled to 200% is 150 ppi. Print targets ~300 ppi
  effective (240+ is often acceptable for photos; 1200 ppi for 1-bit line art).
- Scale in Photoshop for large changes rather than in Illustrator.

## Crop Image
- Select a placed raster, Control/Properties panel > **Crop Image**. Discards pixels outside the crop
  (linked images become embedded after cropping). Set PPI in the crop options to downsample.
  Use instead of a clipping mask when hidden pixels are not needed.

## Handoff
- File > **Package** copies linked images and fonts into a folder (see illustrator-package skill).
- Embedding everything makes one large file but avoids missing links when sharing a single AI/PDF.

## Gotchas
- Missing link warning on open: relink immediately; otherwise the preview prints at low resolution.
- Linked images with spaces or special characters in paths break on some servers.
- Embedded images cannot be edited in Photoshop with Edit Original.
- Images in RGB in a CMYK print document are converted at output; check colour first.

## Verify
- [ ] Links panel: no missing or modified icons; effective PPI meets the output spec.
- [ ] Package folder opens on another machine with no warnings.
