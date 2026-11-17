---
id: creative-arts.photography-fine-art.adobe-lightroom.sync-and-auto-sync
name: sync-and-auto-sync
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, auto-sync, lightroom-presets, sync-settings, copy-paste-settings, lightroom-classic]
level: practitioner
status: draft
description: "Apply edits across many photos in Lightroom Classic with Sync, Auto Sync, Previous and copy/paste settings, choosing which settings to include."
sources: ["https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Synchronize develop settings)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sync and Auto Sync

## Sync (Develop module)
1. Edit one photo; select it first (the **most-selected**, brighter frame), then Ctrl/Cmd-click or Shift-click others in the filmstrip.
2. Click **Sync...** (bottom of right panel). Tick only what should transfer: e.g. Basic Tone, Color Grading, Lens Corrections; untick White Balance, Crop, Spot Removal, Masks unless intended.
3. Synchronize. Alt/Option+Sync skips the dialog using last choices.

## Auto Sync
- Flip the switch beside Sync (or Ctrl/Cmd-click Sync). Every slider change on the active photo applies to all selected photos live.
- Ideal for a bracket or a set in identical light. **Turn it off afterwards**; forgotten Auto Sync is the classic way to ruin a shoot's edits.

## Other ways
- **Previous** (Ctrl/Cmd+Alt/Option+V): applies all settings from the previously selected photo.
- **Copy/Paste** (Ctrl/Cmd+Shift+C / +V): choose settings once, paste to many (works in Library Grid too).
- Library Quick Develop: relative adjustments (Exposure +1/3) to many photos without equalising them.

## Masks and spots
- AI mask components recompute per image; brush strokes and spots copy positions exactly. Check each photo after syncing these.

## Gotchas
- Sync with Crop ticked copies the crop rectangle; varying framing will be cut.
- Syncing Upright mode re-analyses each frame; syncing "Upright transforms" copies exact values.

## Verify
- [ ] Survey view of synced photos shows matching tone/colour; spot-check one for crop and masks.
