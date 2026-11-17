---
id: computing-software.general-digital-literacy.web-browsers.pinning-and-muting-tabs
name: pinning-and-muting-tabs
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, tabs, pinned-tabs, mute-tab, mute-site, browser]
level: intro
status: docs-checked
description: "Pin tabs you always keep open in Chrome, and silence noisy tabs in Safari and Edge, with the confirmed menu steps and shortcuts."
sources:
  - https://support.google.com/chrome/answer/2391819
  - https://support.google.com/chrome/answer/12929150
  - https://support.apple.com/guide/safari/mute-audio-in-tabs-ibrwae910b47/mac
  - https://support.microsoft.com/en-us/microsoft-edge/keyboard-shortcuts-in-microsoft-edge-50d3edab-30d9-c7e4-21ce-37fe2713cfad
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pin and mute tabs

**Goal:** email, calendar and chat stay open in small fixed tabs; a video somewhere stops blaring.

## Pin (Chrome)
- Right-click the tab > **Pin**. Pinned tabs are smaller and show only the site's icon. Unpin with right-click > **Unpin**.
- Pinned tabs are one of the things that stop Chrome's Memory Saver from deactivating a tab.
- Whether other browsers keep pinned tabs after a restart depends on their startup setting; check it (see the startup skill).

## Mute
- **Safari (Mac):** click the Audio button in the Smart Search field to mute the tab you are viewing; click the Audio button on the right side of any tab in the tab bar to mute that tab; Option-click the Audio button to keep the current tab playing and mute the others. Click and hold the Audio button to see which sites are playing audio and choose Mute This Tab or Mute Other Tabs.
- **Edge:** Ctrl+M toggles mute for the current tab (Windows and Mac).
- **Chrome:** after selecting several tabs, right-click and choose Mute or Unmute.

## Gotchas
- Too many pinned tabs make the tab strip as crowded as before; keep 3-6.
- Muted tabs stay muted until you unmute them; if a tab "has no sound" later, check its Audio button.
- Pinned web apps still log you out on schedule; that is the site's session policy.

## Verify
- [ ] Pinned tab shows only an icon and sits at the left of the strip.
- [ ] Muting one tab leaves other tabs playing.

## Checked
2026-10-27. Chrome Help (Manage tabs; Personalize Chrome performance), Apple Safari User Guide (Mute audio in tabs) and Microsoft's Edge keyboard shortcuts page were read. Confirmed Chrome Pin/Unpin and its icon-only appearance, pinned tabs blocking tab deactivation, Chrome Mute on selected tabs, the Safari mute controls and Edge Ctrl+M. Firefox and per-site autoplay settings are not covered because those pages could not be confirmed. Method: documentation only; no commands were run.
