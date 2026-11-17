---
id: computing-software.general-digital-literacy.web-browsers.restoring-tabs-and-sessions
name: restoring-tabs-and-sessions
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, tabs, restore-session, reopen-closed-tab, continue-where-left-off, recently-closed, history, crash-recovery]
level: intro
status: docs-checked
description: "Get back closed tabs after an accidental close, and set Chrome and Safari to continue where you left off; Edge's recently closed list is covered too."
sources:
  - https://support.google.com/chrome/answer/157179
  - https://support.google.com/chrome/answer/95314
  - https://support.apple.com/guide/safari/keyboard-shortcuts-and-gestures-cpsh003/mac
  - https://support.apple.com/en-us/102192
  - https://support.microsoft.com/en-us/microsoft-edge/browse-inprivate-in-microsoft-edge-cd2c9a48-0bc4-b98e-5e46-ac40c84e27e2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring tabs and previous sessions

**Goal:** never lose a set of tabs to an accidental close.

## Just closed
- `Ctrl+Shift+T` (Mac `Cmd+Shift+T`) reopens previously closed tabs in the order they were closed (Chrome and Edge). Safari: `Shift-Cmd-T` reopens the last closed tab and also the last closed window.
- Edge: Settings and more > History > **Recently closed**.

## Start-up behaviour
- **Chrome:** Settings > **On startup** > **Continue where you left off**. Cookies and data are saved, so sites you were signed in to open signed in; to avoid that, turn on Settings > Privacy and security > Site settings > Additional content settings > On-device site data > *Delete data sites have saved on your device when you close all windows*.
- **Safari (Mac):** Safari > Settings > General > **Safari opens with** (options include all windows from your last session). Some options appear only if "Close windows when quitting an app" is selected in Desktop & Dock settings. Hold Shift while opening Safari to skip reopening windows once.

## Gotchas
- Edge InPrivate windows do not let you reopen their closed tabs from Recently closed.
- A session restore is a convenience, not a backup. For an important set of tabs, press Ctrl+Shift+D (Chrome or Edge; Cmd+Shift+D on Mac) to save all open tabs in a new bookmark folder.

## Verify
- [ ] Close the browser with 3 tabs open and relaunch: all 3 return.

## Checked
2026-10-27. Chrome Help (keyboard shortcuts; Set your homepage and startup page), Apple Support (Safari shortcuts; Control which windows Safari reopens) and Microsoft's InPrivate page were read. Confirmed the reopen shortcuts, Chrome and Safari startup settings, the Safari Shift-key behaviour and Edge's Recently closed menu. Firefox and Edge's startup setting are not covered because they could not be confirmed. Method: documentation only; no commands were run.
