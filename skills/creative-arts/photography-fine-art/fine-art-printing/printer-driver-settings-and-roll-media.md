---
id: creative-arts.photography-fine-art.fine-art-printing.printer-driver-settings-and-roll-media
name: printer-driver-settings-and-roll-media
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, inkjet-printer, printer-driver-settings, roll-media, no-color-adjustment, print-quality-settings, decurl]
level: practitioner
status: draft
description: "Set Epson/Canon driver settings for application-managed colour, quality and media type, and handle roll paper: loading, decurl, cut and borderless."
sources: ["https://epson.com/ (SureColor P-series user guides)", "https://www.usa.canon.com/ (imagePROGRAF PRO user guides)", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Printer driver settings and roll media

## Driver for application-managed colour
- **Epson** (Windows): Main tab - Media Type as per profile; Print Quality: Quality Options (Level 4-5 or
  "Max Quality"); **Color Mode: Off (No Color Adjustment)**; High Speed (bidirectional) **off** for best quality.
- **Epson** (macOS): Color Matching panel - EPSON Color Controls; Printer Settings - Color Settings **Off (No Color Adjustment)**.
- **Canon** imagePROGRAF PRO: Color Mode / Matching - **None** (or "No color correction") and media type as per profile;
  Canon Professional Print & Layout plug-in handles this automatically.
- Save the configuration as a preset named by paper.

## Roll media
1. Load the roll with the correct core adapter; feed the leading edge straight; check skew.
2. Set roll width and media type on the printer panel; set remaining length tracking if available.
3. **Decurl**: modern printers decurl internally; otherwise roll prints face-out on a large tube for a day.
4. Cutting: auto-cutter for thin papers; manual cut (normal cut off) for thick fine-art media to avoid head
   damage/cracking.
5. Borderless prints only on supported widths; expect slight enlargement beyond the edges.
6. Leave drying time before rolling or stacking (glossy pigment prints can block/transfer).

## Gotchas
- Double colour management (application AND driver) = oversaturated/dark prints.
- Media type mismatch changes ink load - bleeding on matte or puddling on gloss.

## Verify
- [ ] Driver preset saved per paper; roll prints square, uncracked, flat after drying.
