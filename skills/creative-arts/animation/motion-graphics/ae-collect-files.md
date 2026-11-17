---
id: creative-arts.animation.motion-graphics.ae-collect-files
name: ae-collect-files
category: creative-arts
field: animation
product: motion-graphics
tags: [collect-files, render-queue, after-effects, project-packaging, reduce-project, remove-unused-footage, missing-footage, fonts, handoff, archive]
level: practitioner
status: draft
description: "Package After Effects projects for handoff, farm rendering or archive: Reduce Project, Remove Unused Footage, Collect Files, fonts and plug-in lists, relink checks."
sources:
  - https://helpx.adobe.com/after-effects/using/projects.html
  - https://helpx.adobe.com/after-effects/using/collect-files.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collect Files and project packaging

**Goal:** an AE project that opens on another machine (colleague, farm node, archive restore in five
years) with every footage file found and nothing missing.

## Steps

1. **Clean**: File - Dependencies - Remove Unused Footage; File - Dependencies - Reduce Project
   (with the final comps selected) to drop comps not used; Consolidate All Footage (merge duplicates).
2. **Check**: File - Dependencies - Find Missing Footage / Missing Effects / Missing Fonts. Resolve
   all before collecting.
3. **Collect**: File - Dependencies - **Collect Files**. Options: For All Comps / For Selected Comps,
   Collect Source Files: All / For Selected Comps / None (project only), "Reduce Project", "Change
   render output to folder", "Enable Watch Folder render".
4. AE writes a folder with the `.aep`, a `(Footage)` folder, and a report `.txt` listing fonts and
   effects used.

## Add what Collect Files does not

- **Fonts**: listed in the report but not copied (licensing). Include font names/versions and licence
  location in the package notes; use Adobe Fonts where possible.
- **Third-party plugins**: listed; note versions. A farm node without the plugin renders red X frames
  or fails.
- Scripts/presets used for the look (`.ffx`), expressions libraries, mogrts.

## For farm rendering

Collected projects use relative paths, so they can sit on the farm's share. Alternatively keep
footage on the shared storage and use path mapping; collecting duplicates large footage.

## Gotchas

- Image sequences collect as many files; long projects with renders inside can be huge. Decide whether
  renders are footage (collect) or outputs (don't).
- Proxies are collected as well if set; disable proxies first if not needed.
- Opening a collected project in a newer AE version converts it; keep the original version noted.

## Verify

Open the collected project on a different machine (or after renaming the original footage folder):
no missing footage, effects or fonts warnings; render one frame of each final comp.
