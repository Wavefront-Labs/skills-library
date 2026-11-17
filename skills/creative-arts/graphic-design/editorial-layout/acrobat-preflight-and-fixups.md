---
id: creative-arts.graphic-design.editorial-layout.acrobat-preflight-and-fixups
name: acrobat-preflight-and-fixups
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, pdf-x, print-ready-pdf, acrobat-preflight, preflight-profiles, fixups, ghent-workgroup, pdf-x-verification, print-production, prepress]
level: advanced
status: draft
description: "Check print PDFs with Acrobat Pro Preflight: PDF/X verification, Ghent Workgroup profiles, reading the report, safe fixups vs fixing at source, and reports."
sources:
  - https://helpx.adobe.com/acrobat/using/preflight-tool-acrobat-pro.html
  - https://www.gwg.org/ghent-pdf-output-suite/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acrobat preflight and fixups

**Goal:** prove the PDF you send meets the standard and the printer's spec - including things layout-app preflight cannot see.

## Run it (Acrobat Pro > Print Production > Preflight)
- Profiles grouped by purpose: **PDF/X compliance** ("Verify compliance with PDF/X-4"), Digital printing, Prepress,
  and imported profiles. Ghent Workgroup (GWG) specs (e.g. GWG 2022 Sheetfed CMYK) are widely used industry checks -
  import the printer's profile (.kfp) if they provide one.
- Click Analyze. Results: red X errors, yellow warnings, info; expand to see objects, click to show them on the page.

## What it catches that InDesign may not
- RGB or spot colours **inside placed PDFs/AI files**; unintended spot colours.
- Images below a resolution threshold (including those in nested PDFs).
- Fonts not embedded; text below minimum size; thin lines (hairlines < 0.25 pt).
- **Total area coverage** above the limit (see output preview skill).
- White objects set to overprint (they disappear), black text not overprinting.
- Missing trim/bleed boxes; content outside bleed.

## Fixups
Single fixes (wrench icon) and profiles with fixups: convert colours to the output intent, embed missing fonts,
set TrimBox/BleedBox, convert to PDF/X-4, flatten transparency, remove hidden content, etc.
- Fixups are fine for **technical** issues (boxes, metadata, conformance). For **content** issues (wrong colours,
  low-res images, missing bleed), fix in the source document and re-export - fixups can produce surprising results
  (e.g. colour conversions shifting brand colours).
- Run fixups on a **copy**; re-run verification afterwards.

## Report
Report > Create report (PDF summary with comments/layers) - attach to the delivery or keep for disputes.

## Gotchas
- "Verify compliance" only checks the standard; a valid PDF/X can still be wrong for this job (wrong page size, no bleed) -
  check the printer's spec too.
- Some preflight profiles flag RGB images as errors even in PDF/X-4 workflows where RGB is legal; use the right profile.

## Verify
- [ ] Printer's/GWG profile shows no errors; PDF/X verification passes.
- [ ] Any fixup applied to a copy and re-verified; content issues fixed at source.
