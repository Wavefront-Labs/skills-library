---
id: computing-software.ux-hci-design.usability-heuristics.status-save-and-sync-state
name: status-save-and-sync-state
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [save-state-indicator, offline-sync-status]
level: practitioner
status: draft
description: "Design visible saved, saving, failed and offline states so users never wonder whether work was kept."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Save and sync state
Show one persistent, low-noise indicator with distinct states:
1. **Saving** - transient, appears after a short delay to avoid flicker.
2. **Saved** - with a timestamp or "All changes saved".
3. **Failed** - persistent, says what happened and offers retry; keep the local copy.
4. **Offline** - states that edits are queued and will sync.

## Rules
- Autosave removes the need for a Save button, but still show the state.
- Never silently drop data on failure; keep the unsent draft and warn on leaving (`beforeunload`) only while unsaved.
- Announce state changes to assistive tech with `role="status"` (polite).

## Verify
- [ ] Kill the network mid-edit: user sees a failed/offline state and nothing is lost on reconnect.
