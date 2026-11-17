---
id: humanities.genealogy-and-family-history.family-tree-software.managing-a-tree-and-gedcom-exchange
name: managing-a-tree-and-gedcom-exchange
category: humanities
field: genealogy-and-family-history
product: family-tree-software
tags: [family-tree-software, genealogy-software, gramps, rootsmagic, family-tree-maker, legacy-family-tree, heredis, macfamilytree, gedcom, gedcom-5-5-1, gedcom-7, gedcom-import, gedcom-export, data-loss, citations, source-templates, master-source, events, places, place-hierarchy, media-links, backups, merge-duplicates, tree-sync, ancestry-sync, reports, charts]
level: practitioner
status: draft
description: "Keep a master family tree in desktop software (Gramps, RootsMagic, Family Tree Maker): consistent entry, sources and places, backups, and GEDCOM export/import without silent data loss."
sources:
  - "FamilySearch, The FamilySearch GEDCOM Specification 7.0 (gedcom.io)"
  - "Gramps project wiki and user manual (gramps-project.org)"
  - "RootsMagic user documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managing a tree and GEDCOM exchange

**Goal:** a single, well-sourced master tree on your own machine that you control, and the
ability to move it between programs and websites without losing citations, notes or media links.

## 1. Choose and commit to a master
- **Gramps** (free, open source, Windows/macOS/Linux) — powerful, flexible event/citation model.
- **RootsMagic** (commercial, free "Essentials" tier) — strong sourcing, syncs with some
  online trees. **Family Tree Maker** (commercial) — syncs with Ancestry trees. Others: Legacy,
  Heredis, MacFamilyTree. *Feature and sync details change between versions; check current docs.*
- Pick **one master**. Online trees are copies; sync only in one direction you understand.

## 2. Consistent data entry
- **Names:** surname field as recorded at birth; married names as alternate names or events,
  not by overwriting.
- **Dates:** one format, with qualifiers the software understands (`abt 1842`, `bef 1850`,
  `bet 1840 and 1845`), and double dates for Old Style (`10 Feb 1720/21`).
- **Places:** full hierarchy, largest last, as the place was *at the time* ("Leeds, Yorkshire,
  England"). Use the place list/hierarchy feature so each place exists once; add coordinates.
- **Events with sources**, not bare facts: every birth/marriage/residence event gets a citation
  pointing to a master **source** (the record set) plus the specific detail (page, entry,
  image URL). Templates (Evidence Explained-style) help consistency.
- Keep facts and **conclusions** distinct; use notes for reasoning and conflicts.

## 3. Media
- Store document images in one project folder with a naming convention
  (`1851-census-leeds-smith-household.jpg`) and link them using **relative paths** where the
  program allows, so the folder can move between machines.

## 4. GEDCOM: the interchange format and its traps
- **GEDCOM 5.5.1** is still the most widely supported; **GEDCOM 7.0** (2021) adds proper
  media packaging (GEDZIP) and cleaner structures but support is uneven. *Check each program's
  import/export version.*
- Programs extend GEDCOM with custom tags (`_TAG`); others may drop or mangle them. Typical
  losses: source templates flattened, citation detail moved into notes, media links broken,
  custom events turned into generic ones, place coordinates lost, colour coding and tasks gone.
- **Test round-trip:** export a GEDCOM, import into a *new* empty file in the target program, and
  compare counts (people, families, sources, citations, media) and a few complex people by hand.
- Never import a GEDCOM into your master tree directly — import into a scratch file, review,
  then merge selectively.
- Export with living-person privacy options when sharing (names only, details suppressed).

## 5. Duplicates and merging
Use the duplicate finder, but merge only after comparing the evidence. Merging two different
same-name people is hard to undo — back up first.

## 6. Backups
- Use the program's own backup (which bundles the database) on a schedule, plus a separate
  GEDCOM export as a format-neutral archive, and copy the media folder. Keep 3 copies, one off-site.
- Restore-test occasionally.

## Gotchas
- Syncing with an online tree can pull in unvetted hints or overwrite edits; review sync logs.
- Character encoding: export UTF-8 to keep accents and non-Latin names.
- Some programs auto-correct place names to a modern gazetteer; check the setting.

## Verify
- [ ] One master tree identified; online trees treated as copies.
- [ ] Every event has a citation to a master source.
- [ ] Places entered once in a consistent hierarchy.
- [ ] GEDCOM round-trip tested with counts compared before relying on it.
- [ ] Backups (native + GEDCOM + media) exist and a restore has been tested.
