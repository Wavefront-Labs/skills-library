---
id: creative-arts.graphic-design.adobe-photoshop.actions-and-batch-processing
name: actions-and-batch-processing
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-automation, photoshop-actions, batch-processing, droplets, conditional-actions]
level: practitioner
status: draft
description: "Record robust Photoshop actions and run them with File > Automate > Batch or droplets: modal controls, insert menu item, conditional actions and error logging."
sources:
  - https://helpx.adobe.com/photoshop/using/creating-actions.html
  - https://helpx.adobe.com/photoshop/using/processing-batch-files.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Actions and batch processing

**Goal:** repeat a sequence (resize, convert, sharpen, save) across hundreds of files reliably.

## Recording robust actions
1. Actions panel > New Set, then New Action; optional function-key shortcut.
2. Record. Do the steps on a sample file. Stop.
3. Make it resolution- and orientation-independent:
   - Use Image > Image Size with percentages, or **File > Automate > Fit Image** (fits long edge).
   - Units in Preferences as **percent** before recording moves/selections.
   - Use **Insert Menu Item** for steps that don't record (e.g. View commands).
4. Toggle dialog (modal) icon on a step to pause for user input.
5. **Insert Conditional** (flyout): e.g. "If document is landscape, play action X else Y".
6. Insert Stop with a message for manual steps.

## Batch (File > Automate > Batch)
- Set + Action; Source folder (Include All Subfolders, Suppress File Open Options, Suppress
  Color Profile Warnings).
- Destination Folder + **Override Action "Save As" Commands** - only works if the action itself
  contains a Save As step; otherwise files are not saved where you expect.
- File Naming tokens (document name + serial number + extension).
- Errors: **Log Errors to File** instead of stopping.

## Droplets
File > Automate > Create Droplet - drag files onto the icon to run the action.

## Gotchas
- Actions record layer names; renamed layers break steps ("object not available").
- Save As steps record the folder path; Override fixes this in Batch.
- Test on copies; Batch overwrites if destination = source.

## Verify
- [ ] Batch on 5 mixed files (portrait/landscape, RGB/CMYK) produces correct output, empty error log.
