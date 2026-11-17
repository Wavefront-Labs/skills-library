---
id: computing-software.systems-network-administration.audiobookshelf.mobile-listen-history
name: mobile-listen-history
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [mobile-app, listen-history, sync, android, recovery]
level: practitioner
status: docs-checked
description: "Use the Audiobookshelf Android app Listen History to recover a lost position and diagnose sync problems."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/mobile-apps/listen-history.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/listening-sessions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open the three-dot menu on a library item and choose **History**. Rows show time, event type, position in the book, and a sync indicator when the event should sync.

Sync indicator: a green cloud is success, a red exclamation is failure. A failure only means the server lacks the latest position; it is still stored locally.

Event types: `Play`, `Pause`, `Save`, `Seek`, `Sync`. `Save` events are collapsed into one row with a count, because they are more frequent.

Recovery: tap the book timestamp on a row to jump to that position. Use this after an accidental seek to another place or chapter, or when the server syncs and overwrites local progress.

Pair it with the server's Listening Sessions page, which shows the device used, when deciding where an overwrite came from.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Listen History page and Listening Sessions page.

Method: documentation only; no commands were run.
