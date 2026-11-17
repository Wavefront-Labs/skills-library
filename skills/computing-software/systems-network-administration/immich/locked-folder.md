---
id: computing-software.systems-network-administration.immich.locked-folder
name: locked-folder
category: computing-software
field: systems-network-administration
product: immich
tags: [locked-folder, pin, session, privacy, visibility]
level: intro
status: docs-checked
description: "Hide sensitive Immich assets behind a PIN-protected Locked Folder: unlock duration, where locked assets can reappear, and moving them back out."
sources:
  - https://docs.immich.app/features/locked-folder
  - https://docs.immich.app/features/command-line-interface
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep selected photos and videos out of normal views and behind a PIN.

Move assets in from the asset actions menu. Access to the Locked Folder requires a PIN.

Unlocking:

- Unlocking gives the current session temporary elevated access to locked assets.
- The initial grant lasts 15 minutes. If the session is still in use near the end, the expiry can be extended for a short time.
- While unlocked, locked assets may also appear where relevant, such as search results or utilities like Review large files.
- Selecting Lock ends elevated access immediately, and the assets disappear from those views again.
- Signing out also ends access because the session is destroyed.

Moving assets out: while the session is unlocked, move assets back out of the Locked Folder. They return to normal visibility.

Uploads can go straight into it: the CLI option `--visibility locked` sets the visibility of uploaded assets, alongside `archive`, `timeline` and `hidden`.

Because unlocking is per session, select Lock when you finish, especially on shared computers.

## Checked

2026-11-09. Confirmed against the Locked Folder page (PIN, session unlock, 15 minute initial grant, extension, Lock and sign-out, moving out) and the CLI page (`--visibility` choices archive, timeline, hidden, locked).
Method: documentation only; no commands were run.
