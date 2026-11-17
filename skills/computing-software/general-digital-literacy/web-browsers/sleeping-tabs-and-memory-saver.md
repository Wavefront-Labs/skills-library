---
id: computing-software.general-digital-literacy.web-browsers.sleeping-tabs-and-memory-saver
name: sleeping-tabs-and-memory-saver
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, tabs, browser, sleeping-tabs, memory-saver, tab-discarding]
level: intro
status: docs-checked
description: "Cut browser memory and battery use with Chrome Memory Saver and Edge sleeping tabs, and exclude sites that must stay active."
sources:
  - https://support.google.com/chrome/answer/12929150
  - https://support.google.com/chrome/answer/157179
  - https://support.google.com/chrome/answer/1385029
  - https://support.microsoft.com/en-us/edge/learn-about-performance-features-in-microsoft-edge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sleeping tabs and memory saver

**What happens:** inactive tabs are paused or deactivated to free memory; selecting the tab brings it back.

## Chrome (Memory Saver)
More > Settings > **Performance**: turn **Memory Saver** on and choose a level: *Moderate*, *Balanced* (recommended) or *Maximum* (tabs become inactive after a longer, optimal or shorter period respectively). To keep a site active, next to **Always keep these sites active** select **Add**, then add current sites or enter an address. Turn on **Inactive tabs appearance** to show a ring around the icon of inactive tabs. Chrome's help says these prevent deactivation: active audio or video, calls, screen sharing, page notifications, active downloads, partially filled forms, pinned tabs and connected USB or Bluetooth devices. Memory Saver is not available on Chrome for iOS or Android.

## Edge (sleeping tabs)
Settings and more > Settings > **System and performance** > **Performance**:
- **Automatically put tabs to sleep** on; **Put inactive tabs to sleep after a set time** (the default is two hours).
- **Fade inactive tabs** toggle controls the fading of sleeping tabs.
- **Always keep these sites active**: select Add site, type the full URL, then Add.
- Sleeping is skipped for the active tab, a tab playing audio, one capturing screen or camera or microphone, one inspected by DevTools, and sites on your list. Energy saver, when active, can put inactive tabs to sleep after 30 minutes or less.

## Sites to exclude
Web chat, music players, sites with unsaved form input, live dashboards and video calls. Chrome lists partially filled forms among things that prevent deactivation, but keep unsaved work saved anyway.

## Gotchas
- A slow PC with many tabs: Memory Saver helps, but closing tabs helps more (Chrome's speed-up help also says to close unused tabs).
- Chrome Task Manager (Shift+Esc on Windows) shows which tabs and extensions use memory.
- Firefox and Safari are not covered here (see Checked).

## Verify
- [ ] Browser memory in the system task manager drops after tabs have been idle; excluded sites keep running.

## Checked
2026-10-27. Chrome Help (Personalize Chrome performance; keyboard shortcuts) and Microsoft's "Learn about performance features in Microsoft Edge" were read. Confirmed the menu paths, option names, levels, default interval and exclusions above. Firefox and Safari are not covered because they could not be confirmed. Method: documentation only; no commands were run.
