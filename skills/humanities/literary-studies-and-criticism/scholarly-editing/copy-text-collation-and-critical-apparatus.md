---
id: humanities.literary-studies-and-criticism.scholarly-editing.copy-text-collation-and-critical-apparatus
name: copy-text-collation-and-critical-apparatus
category: humanities
field: literary-studies-and-criticism
product: scholarly-editing
tags: [scholarly-editing, textual-scholarship, textual-criticism, critical-edition, copy-text, greg-bowers, rationale-of-copy-text, social-text, mcgann, documentary-edition, genetic-criticism, witnesses, collation, collatex, juxta, hinman-collator, optical-collation, variants, substantives, accidentals, emendation, critical-apparatus, textual-notes, historical-collation, lemma, siglum, tei, tei-critical-apparatus, digital-edition, bibliography, descriptive-bibliography, cse]
level: advanced
status: draft
description: "Edit a literary text: identify witnesses, choose copy-text (Greg-Bowers or alternatives), collate by hand or with CollateX, classify variants and write an apparatus in lemma ] reading form or TEI."
sources: ["W. W. Greg, 'The Rationale of Copy-Text', Studies in Bibliography 3 (1950-51)", "G. Thomas Tanselle, A Rationale of Textual Criticism (1989)", "Jerome McGann, A Critique of Modern Textual Criticism (1983)", "MLA Committee on Scholarly Editions, guidelines", "TEI P5 Guidelines, ch. 12 Critical Apparatus", "CollateX documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Copy-text, collation and critical apparatus

**Goal:** a reliable text whose every departure from its sources is recorded, so a
reader can reconstruct each witness from your apparatus. For the music-specific
version of this craft see
humanities.musicology.music-source-studies.collation-and-critical-editions-of-music.

## 1. Find and describe the witnesses
- List every manuscript, typescript, proof, and edition published in the author's
  lifetime (plus later ones with possible authority). Give each a **siglum**
  (MS, 1814, 1818 or A, B, C).
- For printed books, copies of the *same* edition can differ (stop-press corrections):
  collate several copies of key editions. Descriptive bibliography (format, collation
  formula, issue/state) belongs in the textual introduction.

## 2. Choose an editorial approach — and say why
- **Copy-text (Greg–Bowers)**: take one witness (classically the earliest close to the
  author's manuscript) as the base for **accidentals** (spelling, punctuation,
  capitalisation), and admit later **substantive** variants (words) where you judge
  them authorial revisions. Produces an eclectic text of "final intention".
- **Best-text / documentary**: reproduce one witness faithfully, correcting only
  evident errors — used where authority is diffuse or the document itself matters.
- **Social text (McGann)** and **genetic** editions: present a historical version or the
  process of composition rather than an ideal text.
- Versions: some works (e.g. revised poems) are better edited as separate versions.
Name the approach in the textual introduction; reviewers judge consistency against it.

## 3. Collate
- **By hand**: read aloud with a partner, one holding the base text. Slow but catches
  punctuation. Mark every difference on a collation sheet.
- **Optically**: for copies of one edition, a comparator (the Hinman collator historically,
  or overlaying aligned page images) reveals press variants.
- **Computationally**: transcribe witnesses (carefully — transcription errors become
  false variants), then align with **CollateX** (Python/Java; outputs tables, TEI,
  graphs) or Juxta. Example: `pip install collatex` then use its `Collation` and
  `collate()` functions — check the current API docs. Always review the alignment.
Record every variant first; classify later.

## 4. Emend and record
- Emend only with a reason: an error (a dropped line, a compositor's misreading) or
  your policy's admission of a later reading. Log each emendation.
- Apparatus entry form (common print convention):
  `23.14 grey] MS; gray 1818` — page.line, **lemma** (the reading in your text), the
  closing square bracket, sources agreeing, then variant readings and sigla.
- Typical sections: **emendations list**, **historical collation** (all substantive
  variants in authoritative witnesses), **line-end hyphenation list** (which hyphens are
  in the copy-text vs created by your typesetting), textual notes for hard decisions.
- In **TEI**: `<app><lem wit="#MS">grey</lem><rdg wit="#E1818">gray</rdg></app>`
  with witnesses declared in `<listWit>`; choose a linking method (parallel
  segmentation is easiest to render).

## Gotchas
- Spelling modernisation is a policy decision; announce it and apply it uniformly.
- An OCR transcript used for collation must be proofread against page images first.
- A "corrected" reading that matches your expectations is the most dangerous kind; ask
  what the witness could plausibly say.
- Status: draft; apparatus conventions vary by series (check the series style sheet).

## Verify
- [ ] All witnesses listed with sigla and bibliographical description.
- [ ] Editorial approach stated and followed consistently.
- [ ] Collation checked (second person or second method).
- [ ] Every departure from copy-text is listed as an emendation with reason.
- [ ] From the apparatus, a reader could reconstruct any witness's readings at a given point.
