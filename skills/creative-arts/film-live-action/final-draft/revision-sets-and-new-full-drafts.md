---
id: creative-arts.film-live-action.final-draft.revision-sets-and-new-full-drafts
name: revision-sets-and-new-full-drafts
category: creative-arts
field: film-live-action
product: final-draft
tags: [final-draft, film-live-action, revision-setup, revision-sets, revision-set-names, unlock-pages, new-full-draft, revision-reset, clear-revisions, revision-colours, production-revisions]
level: practitioner
status: draft
description: "Configure Final Draft revision sets (names, colours, marks, styles) for a production, switch sets per round, and reset to a new full draft: clear marks, unlock pages and renumber deliberately."
sources:
  - "https://www.finaldraft.com/support (Final Draft 13 user guide - Production menu - Revisions, Lock Pages)"
  - "https://www.finaldraft.com/learn/ (Final Draft learning resources - production drafts)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revision sets and new full drafts in Final Draft

**Goal:** each round of production changes is marked with the right name, colour and
mark; and when the production calls for a fresh full draft, the script is reset
cleanly without breaking anyone's breakdown by accident.

Menu names are from Final Draft 12/13 (Production menu); older versions differ - confirm
in your copy.

## 1. Set up the revision sets
Open **Production > Revisions...** (the Revisions dialog). Each row is a **revision set**:
- **Name** - the colour name the production uses ("Blue Revision", "Pink Revision").
- **Mark** - the character in the right margin (default `*`); some productions use a
  different mark per set so cumulative changes are distinguishable.
- **Color** - text colour on screen (and optionally in print) for revised text.
- **Style** - optional bold/underline for revised text.
Edit the list to match the production's colour order (first AD / production office
decides; the standard US order is White, Blue, Pink, Yellow, Green, Goldenrod, Buff,
Salmon, Cherry, then double colours). Save the setup into a **template** so every
episode/script for the show starts identical.

## 2. Each revision round
1. Confirm pages and scene numbers are locked (Production menu shows *Unlock* options
   when locked).
2. Select the **current revision set** in the Revisions dialog and turn on
   **Revision Mode** (Production > Revision Mode / *Mark Revisions*).
3. Edit. Check the revised-page header shows the set name and date
   (Document > Header and Footer with the revision fields).
4. Print/PDF **Revised Pages** only for distribution; keep the full script as
   the master.
Decide with the production whether to **keep previous marks** (cumulative) or clear
them before each new colour.

## 3. Starting a new full draft
When the production asks for a clean draft (e.g. after many colours, or a new
episode block's "Double White"):
1. Save a copy of the current script with its colour in the filename (archive).
2. **Clear revision marks** (Production > *Clear Revised* / *Clear Revision Marks* -
   choose all sets).
3. **Unlock pages** (Production > Unlock Pages) so A-pages reflow into normal pages.
4. Scene numbers: either keep them (usual mid-shoot - departments still reference
   them) or, only if production explicitly asks, **renumber** (Production > Scene
   Numbers, uncheck *Keep existing numbers*).
5. Relabel the title page ("Full Draft - Double White - date"), re-lock pages, and issue
   the full PDF.

## Gotchas
- Editing with the wrong set active; a Pink change marked Blue.
- Renumbering scenes mid-shoot - every schedule and call sheet breaks.
- Unlocking pages without clearing marks: the whole script looks revised.
- Different team members with different revision set lists; use the shared template.

## Verify
- [ ] Revision set list matches the production's colour order; saved as a template.
- [ ] Current set selected before each round; headers show set and date.
- [ ] Archive copy saved before reset; marks cleared; pages unlocked then re-locked.
- [ ] Scene numbers kept unless the production requested renumbering.
