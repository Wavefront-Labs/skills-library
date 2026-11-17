---
id: humanities.musicology.music-source-studies.collation-and-critical-editions-of-music
name: collation-and-critical-editions-of-music
category: humanities
field: musicology
product: music-source-studies
tags: [music-source-studies, source-studies, critical-edition, scholarly-edition, urtext, music-editing, editorial-method, manuscript, autograph, copyist, early-print, first-edition, collation, variants, critical-report, kritischer-bericht, stemma, stemmatics, filiation, watermark, paper-study, rastrology, rastrum, hand-identification, rism, sigla, editorial-intervention, ficta, musica-ficta, mei, sketch-studies]
level: advanced
status: draft
description: "Edit music from sources: locate witnesses via RISM, describe paper, watermarks and hands, collate variants, build a stemma or source hierarchy, and write a critical report."
sources: ["James Grier, The Critical Editing of Music (1996)", "RISM cataloguing guidelines", "Alan Tyson, Mozart: Studies of the Autograph Scores (1987) — paper and watermark method", "Neue Mozart-Ausgabe / Beethoven-Werke editorial guidelines (published prefaces)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collation and critical editions of music

**Goal:** a text of the music that a reader can trust, with every editorial decision
traceable to a source or flagged as the editor's.

## 1. Find all witnesses
- Search **RISM** (series A/I prints, A/II manuscripts), library catalogues and the
  composer's thematic catalogue for every manuscript and early print, including parts
  and arrangements. Note library sigla and shelfmarks (`A-Wn Mus.Hs.12345`).
- Classify: autograph, authorised copy (copyist corrected by composer), first edition,
  later editions, performance parts, sketches. Get high-resolution scans of each.

## 2. Describe each source physically
- **Paper**: format, size, **watermarks** (photograph with transmitted light; compare
  with watermark repertories), **rastrology** — the stave-ruling pattern (staves per
  page, total span in mm) which identifies paper batches and copyists' shops.
- **Hands**: composer vs copyists; distinguish ink colours and later annotations
  (who added that dynamic?).
- **Prints**: engraver's plate number, publisher's address on the title page, and
  issue/state differences. Plate numbers date prints via publisher chronologies.
Combining paper, hand and plate evidence is how sources get dated; Tyson's work on
Mozart's autographs is the model.

## 3. Establish relationships
Collate a test passage across all sources: pitches, rhythms, slurs, articulation,
dynamics, text underlay, beaming. **Shared errors** (not shared correct readings)
reveal descent — a slip copied by two later sources shows they derive from it or a
common ancestor. Draw a **stemma**, or for composer-revised works, a source hierarchy
(principal source + subsidiary sources). Be explicit: many works exist in more than
one authentic version; don't conflate them into a text that never existed.

## 4. Edit
- Choose the **principal source** and state why.
- Normalise per a written policy: clefs, beaming, accidental conventions, stem direction.
- **Distinguish editorial additions typographically**: square brackets, dashed slurs,
  small type — and say which means what in the preface. Musica ficta goes above the
  stave in early music.
- Don't "fix" inconsistencies that may be intended (parallel passages with different
  articulation can be deliberate); report them.
- Encoding the edition in **MEI** allows variants to be stored alongside the text
  (see humanities.musicology.music-encoding-and-notation-tools.engraving-mei-encoding-and-music21-analysis).

## 5. The critical report
- Source descriptions (sigla, location, date, description, relationship).
- Editorial principles.
- **Commentary table**: bar, part/stave, beat, source, reading, decision.
  e.g. `m. 47, Vn I, beat 3: A (autograph) has f♯''; B (first ed.) f''; edition follows A.`
- Separate significant variants from trivial ones if the report would otherwise drown
  the reader, but say where the full collation lives.

## Gotchas
- An urtext label on an edition is a marketing term unless the report supports it.
- Scans can hide erasures and pencil; check doubtful readings in the original.
- Measure rastra in millimetres from the top line of the top stave to the bottom line
  of the bottom stave, consistently, on several pages.
- Status: draft; method summarised from editorial literature; series conventions vary.

## Verify
- [ ] All known sources are listed with sigla and dated with evidence.
- [ ] Principal source chosen and justified; relationships diagrammed.
- [ ] Every editorial addition is visible in the score and explained in the preface.
- [ ] Commentary entries cite bar, part, source and decision.
- [ ] Doubtful readings were checked against originals, not just scans.
