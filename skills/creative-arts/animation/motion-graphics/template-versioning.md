---
id: creative-arts.animation.motion-graphics.template-versioning
name: template-versioning
category: creative-arts
field: animation
product: motion-graphics
tags: [template-versioning, motion-templates, graphics-package, mogrt, creative-cloud-libraries, naming, changelog, series-graphics, version-control]
level: practitioner
status: draft
description: "Version and distribute a series graphics package (AE projects and mogrts) so episodes stay consistent: naming, changelogs, locking, libraries, and updating cut episodes."
sources:
  - https://helpx.adobe.com/premiere-pro/using/working-with-motion-graphics-templates.html
  - https://helpx.adobe.com/creative-cloud/help/libraries.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioning a graphics package

**Goal:** every episode uses the right version of the show's titles, lower thirds and end cards; a
design fix reaches all episodes predictably; old episodes can be re-rendered as they were.

## Package structure

```
SHOW_GFX/
  ae/   SHOW_GFX_master_v007.aep          # all template comps
  mogrt/ SHOW_LowerThird_v007.mogrt  SHOW_TitleCard_v007.mogrt ...
  fonts/ (licensed copies or Adobe Fonts list)
  CHANGELOG.md
```

- One version number for the whole package (simpler than per-template versions for small teams).
- Mogrt file names include the version; Premiere shows the file's internal name, so set the template
  name to include the version as well.

## Change process

1. Change in the master AE project, bump version, write a changelog line (what changed, which
   episodes are affected).
2. Export mogrts to the shared library (Creative Cloud Library or a network folder Premiere watches).
3. Editors: new episodes use the new version; in-progress episodes replace instances (right-click
   in Premiere - Replace with Motion Graphics Template, or re-drop and copy text).
4. Locked episodes: only update when the change is a fix that must ship (spelling, legal), and log it.

## Consistency checks

- Episode delivery checklist includes "graphics package version". Graphics QC compares a frame from
  each template per episode against the reference stills for that version.
- Keep a reference render (PNG stills + a short MOV) per template per version.

## Gotchas

- A mogrt embeds a copy of the AE comp; fixing the master does nothing to existing Premiere instances.
- Fonts updated by the foundry can reflow text; pin font versions in the package.
- Do not let editors save modified copies of templates into the shared library; one owner publishes.

## Verify

Open two episodes' Premiere projects and list template versions used (Project panel / Essential
Graphics): they match the delivery log and the changelog explains every difference.
