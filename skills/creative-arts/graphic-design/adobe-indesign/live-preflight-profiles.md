---
id: creative-arts.graphic-design.adobe-indesign.live-preflight-profiles
name: live-preflight-profiles
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, preflight-profile, live-preflight, effective-resolution-check, overset-check, color-space-check, embed-profile]
level: practitioner
status: draft
description: "Build InDesign Live Preflight profiles that catch real print problems (missing links, low ppi, RGB or spot misuse, overset, small text, bleed) and embed them for the team."
sources:
  - https://helpx.adobe.com/indesign/using/preflighting-files-handoff.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live preflight profiles

**Goal:** problems flagged the moment they happen, against the printer's actual requirements, not discovered at export.

## The panel
Window > Output > Preflight (or double-click the dot in the status bar). Green = no errors for the active profile;
red = errors, listed by category with page links. Turn **On** for every document.

## Make a profile (panel menu > Define Profiles > +)
Name it after the job/printer (`Printer-X offset coated`). Useful checks:
- **Links:** Links missing or modified; OPI links.
- **Color:** Color spaces and modes not allowed (tick RGB if the printer wants CMYK only; or allow RGB for a
  PDF/X-4 workflow); **Spot color setup** (max number of spot colours, e.g. 0 or 1); Overprinting applied in InDesign;
  Overprinting of [Registration]/white.
- **Images and Objects:** **Image Resolution** min colour/greyscale 250-300 ppi, 1-bit 800+; **Non-proportional scaling**
  of placed objects; Uses transparency (if the workflow flattens); **Bleed/Trim hazard** (live area check: objects
  within e.g. 3 mm of trim) and objects not reaching the bleed.
- **Text:** **Overset text**; Font missing; **Minimum type size** (e.g. 6 pt, and stricter for reversed/knock-out
  text); Cross-reference problems; Paragraph style/character style overrides if you enforce style use.
- **Document:** page size and orientation; number of pages required (multiples of 4); blank pages; bleed and slug setup.

## Share profiles
- Panel menu > Define Profiles > profile menu > **Export Profile** (.idpp) - distribute to the team or get one from the printer.
- **Embed Profile** in the document so anyone opening it preflights against the same rules.
- Set "Use embedded profile" vs working profile in Preflight Options.

## Workflow
Fix errors as they appear; before export, Preflight panel must show **No errors**. Some warnings (e.g. transparency)
may be acceptable - document why.

## Gotchas
- The default [Basic] profile checks only missing links, overset text and missing fonts - not enough for print.
- Placed PDF/AI images are checked at their own embedded resolution (vector passes); check placed PDFs separately.
- Preflight cannot see problems inside placed images (RGB inside PDFs, small text in AI files) - use Acrobat preflight on the final PDF too.

## Verify
- [ ] Job-specific profile active and embedded; panel shows No errors.
- [ ] Profile values match the printer's spec sheet.
