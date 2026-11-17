---
id: creative-arts.graphic-design.adobe-indesign.overriding-parent-items
name: overriding-parent-items
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, parent-pages, parent-item-overrides, override-all-parent-items, detach-selection, remove-local-overrides, allow-parent-item-overrides, hide-parent-items]
level: practitioner
status: draft
description: "Override, detach, hide and reset InDesign parent items correctly: Ctrl/Cmd+Shift+click, Override All, Remove Local Overrides, protecting items from override."
sources:
  - https://helpx.adobe.com/indesign/using/masters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overriding and detaching parent items

**Goal:** change parent elements on specific pages without breaking the link for everything else.

## Override (keeps the link)
- **Ctrl/Cmd+Shift+click** a parent item on a document page: it becomes editable on that page. Attributes
  you change (e.g. text content, image) become local; attributes you do not touch still update from the parent.
- Pages panel menu > **Override All Parent Page Items** (Alt+Shift+Ctrl+L / Opt+Shift+Cmd+L) for a whole spread.
- Typical use: placeholder frames on parents (image frames, headline frames) that get filled per page.

## Detach (breaks the link)
Pages panel menu > Parent Pages > **Detach Selection From Parent** (or Detach All Objects). The item becomes
an ordinary page object; parent changes no longer reach it. Use rarely - it defeats the system.

## Reset
- **Remove Selected Local Overrides** / Remove All Local Overrides: returns items to the parent version
  (local content lost).
- Re-applying the parent to a page (Apply Parent with "keep" behaviour) can leave overridden copies behind
  plus fresh parent items - doubled folios are the classic symptom. Remove local overrides first.

## Hide and protect
- **Hide Parent Items** (Pages panel menu) on a page hides all parent items there (e.g. full-bleed image page).
- On the parent, select an item and untick **Allow Parent Item Overrides on Selection** (Pages panel menu)
  for things that must never change (legal footer, logo) - a dotted frame edge indicates protected items.

## Seeing what is what
- View > Extras > Show Frame Edges: parent items have dotted frame edges on document pages.
- Overridden items have solid edges.

## Gotchas
- Overriding a threaded parent text frame breaks threading in non-obvious ways - prefer Primary Text Frame
  (see threading skill).
- Moving an overridden item is a local change; later parent moves will not move it.

## Verify
- [ ] No doubled parent items on pages (check frames and folios).
- [ ] Protected items cannot be overridden; overrides only where content is page-specific.
