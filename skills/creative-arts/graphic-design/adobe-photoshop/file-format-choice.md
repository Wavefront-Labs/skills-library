---
id: creative-arts.graphic-design.adobe-photoshop.file-format-choice
name: file-format-choice
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-export, file-format-choice, psb-large-document, psd, tiff, png, jpeg]
level: intro
status: draft
description: "Choose the right Photoshop save format: PSD vs PSB size limits, layered TIFF for print, PNG for transparency, JPEG for photos, and maximise compatibility."
sources:
  - https://helpx.adobe.com/photoshop/using/file-formats.html
  - https://helpx.adobe.com/photoshop/using/saving-images.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a file format

| Format | Use for | Limits / notes |
|---|---|---|
| **PSD** | Working master, layers, smart objects, placing in InDesign/Illustrator | Max 30,000 x 30,000 px and 2 GB |
| **PSB** (Large Document) | Huge banners, panoramas, files over 2 GB | Up to 300,000 x 300,000 px; fewer apps open it (InDesign places PSB in recent versions) |
| **TIFF** | Print delivery, archival, flattened or layered | LZW or ZIP lossless; 4 GB limit; layered TIFF confuses some RIPs - flatten for printers |
| **PNG** | Screen graphics, transparency, screenshots | Lossless; RGB only; no CMYK |
| **JPEG** | Photos for web/email/client preview | Lossy, 8-bit, no transparency; re-saving degrades |
| **PDF (Photoshop)** | Single-image proofs | Use InDesign for multipage documents |
| **WebP / AVIF** | Modern web delivery | Via Export As / Save a Copy in current versions |

## Rules
- Keep the PSD as master; deliver derivative formats. Never overwrite the master with a flattened JPEG.
- **Maximize PSD and PSB File Compatibility** (Preferences > File Handling): set to Always
  for files placed in other apps or previewed in Lightroom/Bridge (embeds a composite).
- Save a Copy (not Save As) for derivatives in current versions; JPEG/PNG via Save a Copy or Export As.
- 16-bit for heavy retouching/gradients; convert to 8-bit for JPEG.

## Gotchas
- A PSD over 2 GB will refuse to save - Photoshop prompts for PSB.
- Clients without Photoshop cannot open PSD/PSB; send PDF/JPEG proofs.

## Verify
- [ ] Master saved, derivatives named with size/use (`hero_1920_web.jpg`).
