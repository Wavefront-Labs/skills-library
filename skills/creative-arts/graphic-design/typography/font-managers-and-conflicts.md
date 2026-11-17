---
id: creative-arts.graphic-design.typography.font-managers-and-conflicts
name: font-managers-and-conflicts
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, opentype, font-management, font-manager, font-activation, auto-activation, duplicate-fonts, font-cache, document-fonts-folder, extensis-connect, fontbase]
level: practitioner
status: draft
description: "Manage a working font library: font manager activation, auto-activation, document fonts folders, duplicate and version conflicts, and clearing font caches."
sources:
  - https://helpx.adobe.com/indesign/using/using-fonts.html
  - https://support.apple.com/guide/font-book/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Font managers, activation and conflicts

**Goal:** the right version of each font active when needed, no duplicates fighting, and files opening with the fonts they were set in.

## Why a font manager
Hundreds of installed fonts slow apps and menus, and different versions of the same family (Helvetica from the OS,
a client's Helvetica Neue LT, Neue Haas Grotesk) cause reflow and substitution. A manager keeps fonts in a library,
activated only when needed.

## Options
- **Extensis Connect (Suitcase), FontBase, RightFont, Typeface**: library, sets per project, **auto-activation plug-ins**
  for Adobe apps (fonts activate when a document opens).
- macOS **Font Book**: basic activation/deactivation, validation, duplicate resolution.
- Windows: Settings > Personalization > Fonts; managers add per-project activation.
- **Adobe Fonts** sync via Creative Cloud app; documents auto-activate missing Adobe Fonts on open.

## Document fonts folder (Adobe)
InDesign (and Illustrator/Premiere for packages): a folder named **`Document fonts`** next to the INDD activates
those fonts for that document only - created by File > Package. Good for archives and handoffs (licence permitting).

## Conflicts and fixes
- **Duplicates/versions:** keep one version active; validate fonts (Font Book: File > Validate) and remove corrupt
  ones. Note version numbers in the project font register.
- **Same name, different foundry** (e.g. Garamond from Adobe vs Monotype): metrics differ -> reflow. Use the exact
  font from the original file (Type > Find Font shows foundry/version info via font tooltip or Package report).
- **Font cache corruption** (garbled text, menus showing wrong fonts): quit apps, clear system font caches (macOS:
  `sudo atsutil databases -remove` then restart; Windows: stop the Font Cache service, delete
  `%WINDIR%\ServiceProfiles\LocalService\AppData\Local\FontCache` files, restart) and Adobe font caches
  (delete `AdobeFnt*.lst` files in the Adobe app folders).
- PostScript Type 1 fonts are no longer supported in Adobe apps since 2023 - replace with OpenType versions.

## Verify
- [ ] Only project fonts and system essentials active; no duplicate families.
- [ ] Files open without missing-font warnings and without reflow vs the PDF of record.
