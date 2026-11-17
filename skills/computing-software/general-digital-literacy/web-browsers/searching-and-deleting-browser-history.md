---
id: computing-software.general-digital-literacy.web-browsers.searching-and-deleting-browser-history
name: searching-and-deleting-browser-history
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-history, delete-history, search-history, my-activity, privacy]
level: intro
status: docs-checked
description: "Find a page you visited last week in Chrome, Edge or Safari history, and delete single entries, a time range or everything, including across synced devices."
sources:
  - https://support.google.com/chrome/answer/95589
  - https://support.microsoft.com/en-us/microsoft-edge/view-and-delete-browser-history-in-microsoft-edge-00cf7943-a9e1-975a-a33d-ac10ce454ca4
  - https://support.apple.com/guide/safari/clear-your-browsing-history-sfri47acf5d6/mac
  - https://support.microsoft.com/en-us/microsoft-edge/keyboard-shortcuts-in-microsoft-edge-50d3edab-30d9-c7e4-21ce-37fe2713cfad
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search and delete history entries

**Goal:** re-find a page you forgot to bookmark, or remove a specific visit without wiping everything.

## Open history
- Chrome: `Ctrl+H` (Mac `Cmd+Y`), or More > History > History. Chrome's History lists pages from the last 90 days.
- Edge: `Ctrl+H` opens History on Windows, or use Settings and more > History.
- Safari: the History menu (shortcut not listed on Apple's shortcuts page).

## Search it
- Type words from the page title or address into the history search bar.
- Chrome also has a **By group** tab that clusters related visits; in a group, More > Open all in new tab group reopens them.
- Chrome address bar: type `@history`, then Tab or Space, then keywords.

## Delete selectively
- **Single entry or a few sites (Chrome):** History > tick the box next to each item > **Delete** (top right). In a group: More > Remove from history, or Remove all from history.
- **A time range:** Chrome More > **Delete browsing data**; Edge Settings and more > Settings > Privacy, search, and services > Clear browsing data > **Choose what to clear** (Ctrl+Shift+Delete in both); choose the time range, tick **Browsing history**, delete. Safari: History > **Clear History**, then choose how far back.
- **Address-bar suggestion (Chrome on Windows):** press Down arrow to highlight it, then Shift+Delete.

## Synced devices and account activity
- Chrome: with history synced, deleting history in Chrome also deletes it on your other signed-in devices. Your Google search history is stored separately in your Google Account and is deleted there.
- Edge: turn sync off first to clear only the current device; with sync on, synced items clear everywhere. Data in the Microsoft cloud is managed on the privacy dashboard.
- Safari: with iCloud set up for Safari, clearing history removes it from your other Apple devices too.

## Gotchas
- Private windows do not save history, but your network operator (school, employer, ISP) and the sites visited may still see activity.
- Clearing history does not delete records the sites themselves keep, and Safari's Clear History keeps downloaded files.

## Verify
- [ ] Searching history for the removed site returns nothing on each synced device.

## Checked
2026-10-27. Chrome Help (Check or delete your Chrome browsing history; Incognito), Microsoft's Edge history page and Apple's Safari User Guide (Clear your browsing history) were read. Confirmed the menu paths, the 90-day Chrome history, @history search, By group, and the sync behaviour above. Firefox is not covered because its support site could not be read. Method: documentation only; no commands were run.
