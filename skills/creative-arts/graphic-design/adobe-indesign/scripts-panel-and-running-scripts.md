---
id: creative-arts.graphic-design.adobe-indesign.scripts-panel-and-running-scripts
name: scripts-panel-and-running-scripts
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-scripts, indesign-automation, scripts-panel, extendscript, jsx, uxp-scripts, idjs, applescript, vbscript, undo-script]
level: practitioner
status: draft
description: "Install and run InDesign scripts: the Scripts panel and user scripts folder, bundled sample scripts, ExtendScript vs UXP, keyboard shortcuts for scripts, and safe testing."
sources:
  - https://helpx.adobe.com/indesign/using/scripting.html
  - https://developer.adobe.com/indesign/uxp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running scripts and the Scripts panel

**Goal:** use scripts to remove repetitive layout chores (fit frames, clean text, export per page) safely.

## Where scripts live
- Window > Utilities > **Scripts**. Folders: **Application** (bundled samples) and **User**.
- Right-click User > **Reveal in Explorer/Finder** to open the user Scripts Panel folder, then drop `.jsx`
  (ExtendScript), `.idjs` (UXP JavaScript), `.scpt` (AppleScript, macOS) or `.vbs` (Windows) files there.
  They appear immediately; subfolders become groups.

## Running
- Double-click a script. Many need a selection or an open document first; read the header comment.
- Assign shortcuts: Edit > Keyboard Shortcuts > Product Area **Scripts**.
- A well-written script wraps its work in one undo step (`app.doScript(..., UndoModes.ENTIRE_SCRIPT)`);
  older scripts may need many undos, so save before running.

## Useful bundled samples
- **SplitStory / BreakFrame**: unthread a story into separate frames.
- **MakeGrid**: divide a frame into a grid of frames.
- **AddGuides**, **AlignToPage**, **CornerEffects**, **PlaceMultipagePDF**, **FindChangeByList** (batch
  find/change from a text list), **ExportAllStories**, **SelectObjects**.

## ExtendScript vs UXP
- ExtendScript (`.jsx`) is the long-standing engine with the largest base of community scripts.
- UXP scripts (`.idjs`, InDesign 18.5+) use modern JavaScript; Adobe develops this path going forward.
- Edit ExtendScript in VS Code with the Adobe ExtendScript Debugger extension.

## Safety
- Run unknown scripts on a copy; scripts can delete content and access files.
- Prefer scripts from known sources (Adobe samples, established community authors) and read the code.
- Save before running; check overset and links afterwards.

## Gotchas
- A script fails silently when nothing is selected; check its expected selection.
- Scripts written for old versions may hit renamed properties (master spreads are now parent pages in the UI,
  but the DOM still uses `masterSpreads`).

## Verify
- [ ] Script appears in the User folder and runs on a test copy with the expected result.
- [ ] Single Undo reverts it, or the original was saved before running.
