---
id: creative-arts.graphic-design.adobe-indesign.idml-interchange
name: idml-interchange
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, idml, save-back, interchange, corrupt-file-recovery, affinity-publisher-import, quarkxpress-import, archiving]
level: practitioner
status: draft
description: "Use IDML to open InDesign files in older versions and other apps (Affinity, Quark), repair misbehaving documents, archive projects, and check what changes after a round trip."
sources:
  - https://helpx.adobe.com/indesign/using/saving-documents.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IDML for interchange and repair

**Goal:** InDesign documents that open elsewhere and survive version changes, plus a cure for quirky files.

## What IDML is
InDesign Markup Language: a zipped package of XML describing the whole document (pages, stories, styles, swatches).
File > Save As > **InDesign CS4 or later (IDML)**, or File > Export > InDesign Markup (IDML).

## Uses
- **Open in older InDesign:** an INDD saved in a newer version will not open in an older one; IDML usually will
  (CS4 and later). Features the older version lacks are dropped or converted - check.
- **Other applications:** Affinity Publisher, QuarkXPress (recent versions) and some translation/CAT tools import IDML.
  Translation agencies often prefer IDML for text extraction and reinsertion.
- **Repair:** odd crashes, slowdowns, or corrupt-feeling documents are often fixed by exporting IDML and opening it
  (InDesign rebuilds the document structure). Old trick, still effective.
- **Archiving:** include an IDML in the package (File > Package > Include IDML) - future-proof and human-readable XML.

## After a round trip, check
- Text reflow (composition differences between versions; especially with different composer/hyphenation dictionaries).
- Links (paths kept; images are not embedded in IDML).
- Newer features: variable fonts, GREP style changes, column rules, newer table features.
- Page count and overset text (Preflight).

## Gotchas
- IDML does not contain images or fonts - package them alongside.
- Opening IDML creates a new untitled document; save it as INDD with a new name - do not overwrite the original until checked.
- Third-party apps' IDML import is partial: expect manual fixes of tables, effects and text wraps.

## Verify
- [ ] The IDML opens in the target version/app with matching page count and no overset text.
- [ ] Spot-check reflow on text-heavy pages before replacing the original.
