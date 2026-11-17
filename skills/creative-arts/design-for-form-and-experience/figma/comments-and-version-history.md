---
id: creative-arts.design-for-form-and-experience.figma.comments-and-version-history
name: comments-and-version-history
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-comments, version-history, figma-collaboration, named-versions, mentions, comment-resolution, restore-version, figma]
level: practitioner
status: docs-checked
description: "Collaborate in Figma with comments (pins, mentions, resolve) and version history (autosaves, named versions, restore, branching alternatives)."
sources:
  - https://help.figma.com/hc/en-us/articles/360038006754-View-a-file-s-version-history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments and version history

## Comments
- Drop a pin on the canvas or a layer, type, and **@mention** people. **Resolve** threads when done.
- Convention (team practice, not a Figma rule): prefix with intent (**Question:**, **Blocker:**, **Nit:**), say which breakpoint or state, mention the owner, and **resolve with a reply** stating the decision.
- **FigJam** has comments for workshops (`creative-arts.design-for-form-and-experience.figma.running-figjam-workshops`).

## Version history
- Figma saves an **autosave checkpoint every 30 minutes**, and also after connection loss or a crash.
- **Save to Version History** (Ctrl+Alt+S on Windows, Cmd+Option+S on Mac) names a version with a title and description; you can also name an existing version later. Titles over 25 characters are clipped; descriptions under 140 characters show fully.
- **Restore** is non-destructive: Figma saves the current state as a checkpoint first. Comments from all versions are kept. Creating, naming, deleting or restoring needs edit access.
- **Duplicating** a version makes a new file without the original's comments or history.
- **Retention:** drafts and the Starter plan keep up to 30 days; paid plans get the full history of existing files.
- Pair with **branching** (`creative-arts.design-for-form-and-experience.figma.branching-and-merging-library-files`) for ongoing review of library changes, and **sections** for status (`creative-arts.design-for-form-and-experience.figma.organising-figma-pages-with-sections`).

## Practices
Name versions at every review and handoff; resolve comments before marking Ready for dev; archive resolved threads in decision log; avoid using comments for long discussions (move to chat or a doc and link).

## Verify
- [ ] Comments carry intent, owner and resolution; no unresolved blockers at handoff.
- [ ] Milestone versions are named and recoverable.
- [ ] Team notification settings agreed.

## Checked
2026-11-01. Confirmed on the Figma Help Center page on version history: 30-minute autosave, naming and its limits, shortcut, non-destructive restore, duplicate behaviour, retention by plan, edit-access requirement. Removed: all comment-feature claims (shortcut C, attachments, reactions, filters, notification settings, observation mode), the menu path and Ctrl+Alt+H, since the comments page was not read.
Method: documentation only; no commands were run.
