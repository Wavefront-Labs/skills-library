---
id: humanities.classics.epigraphy.squeezes-leiden-conventions-and-inscription-editing
name: squeezes-leiden-conventions-and-inscription-editing
category: humanities
field: classics
product: epigraphy
tags: [epigraphy, inscriptions, greek-epigraphy, latin-epigraphy, squeeze, paper-squeeze, raking-light, rti, reflectance-transformation-imaging, photogrammetry, leiden-conventions, diplomatic-transcription, restoration, lacuna, supplement, letter-forms, palaeography, dating, formulae, prosopography, ig, inscriptiones-graecae, cil, corpus-inscriptionum-latinarum, seg, annee-epigraphique, phi-greek-inscriptions, edh, edcs, epidoc, tei, stoichedon, lemma, editio-princeps]
level: advanced
status: draft
description: "Read and publish an ancient inscription: squeezes, raking-light and RTI photos, Leiden-convention transcription, restoration limits, dating by letter forms and formulae, and IG/CIL/SEG citation."
sources: ["Krummrey & Panciera, 'Criteri di edizione e segni diacritici', Tituli 2 (1980)", "Dow, Conventions in Editing (1969)", "Alison Cooley, The Cambridge Manual of Latin Epigraphy (2012)", "B. H. McLean, An Introduction to Greek Epigraphy (2002)", "EpiDoc Guidelines (current version)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Squeezes, Leiden conventions and editing an inscription

**Goal:** a reading of an inscription that records exactly what is on the stone, what
is restored and why, and a date and context argued from evidence.

## 1. Record the object
- **Autopsy** if at all possible: published photos miss worn strokes. Note material,
  dimensions (H × W × Th), letter heights per line, findspot and current location
  (museum inventory number), condition, and whether the text is complete.
- **Photography**: raking light from at least four directions (low angle, in a dark
  room or at dusk), with scale. **RTI** (reflectance transformation imaging) or
  photogrammetry gives an interactive surface you can re-light later.
- **Squeeze** (paper impression), only with permission and where the stone is sound:
  clean dust off with a soft brush, lay wet unsized filter paper on the face, beat it
  into the letters with a stiff brush, let it dry on the stone, peel off whole.
  Never on painted, flaking or fragile surfaces; never with chemicals. Squeezes reveal
  letters invisible to the eye. Many collections hold historical squeezes — ask.

## 2. Transcribe with the Leiden conventions
Core signs (Leiden 1931 as refined by Krummrey–Panciera; check the conventions your
corpus uses):
| Sign | Meaning |
|---|---|
| `[abc]` | letters lost, restored by editor |
| `[- - -]` or `[...]` | lost letters, unknown number / approx. number of dots |
| `(abc)` | abbreviation expanded by editor |
| `⟨abc⟩` | letters omitted by the cutter, added by editor |
| `{abc}` | letters cut in error, to be ignored |
| `⟦abc⟧` | letters deliberately erased in antiquity (e.g. damnatio memoriae) |
| `ạ` (underdot) | letter damaged, reading uncertain |
| `vac.` / `v` | intentionally blank space |
| `|` or line numbers | line division |
Give a **diplomatic** transcription (capitals, what you see) before the edited text
(lower case, word divided, accented for Greek).

## 3. Restore with discipline
- Count letter spaces. **Stoichedon** texts (letters in a grid) let you compute exactly
  how many letters are missing; otherwise estimate from average letter width.
- Restore from **formulae** (decree prescripts, funerary formulae `D(is) M(anibus)`),
  parallel texts and names attested in prosopographies.
- Mark restorations you are unsure of in the commentary, not by silent confidence. A
  restoration is a hypothesis; avoid building historical arguments on brackets.

## 4. Date
Combine: letter forms (e.g. Attic letters three-bar sigma, four-bar sigma; Latin
apices, ligatures, serifs), orthography, formulae, named officials (eponymous archons,
consuls) and archaeological context. Letter-form dating alone is approximate — give a
range.

## 5. Publish and cite
- Edition format: lemma (bibliography of previous editions: *ed. pr.*, then later),
  text, apparatus (differences from earlier readings), translation, commentary.
- Corpora: Greek **IG**, **SEG** (annual supplement); Latin **CIL**, *L'Année
  épigraphique* (**AE**). Databases: PHI Greek Inscriptions, EDH, EDCS, Trismegistos
  ids. Cite like `IG II² 1237` or `CIL VI 1527` and the database id.
- Encode in **EpiDoc** (TEI XML) for digital publication.

## Gotchas
- Earlier editors' restorations often get repeated as fact; read the apparatus history.
- Bracket conventions differ between older corpora and modern ones; read each preface.
- Status: draft; squeeze practice must follow the holding institution's rules.

## Verify
- [ ] Physical description with dimensions, letter heights and location recorded.
- [ ] Readings checked on raking-light images or a squeeze, not one photo.
- [ ] Transcription uses Leiden signs consistently; diplomatic text included.
- [ ] Each restoration has a stated basis and space count.
- [ ] Date given as a range with combined evidence; corpus and database ids cited.
