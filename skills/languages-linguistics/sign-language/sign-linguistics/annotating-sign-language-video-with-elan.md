---
id: languages-linguistics.sign-language.sign-linguistics.annotating-sign-language-video-with-elan
name: annotating-sign-language-video-with-elan
category: languages-linguistics
field: sign-language
product: sign-linguistics
tags: [sign-linguistics, sign-language-linguistics, corpus-annotation, elan, glossing, id-glosses, tiers, controlled-vocabulary, lexical-database, signbank, hamnosys, sign-writing, signwriting, stokoe-notation, handshape, location, movement, orientation, non-manuals, sign-phonology, corpus-linguistics, inter-annotator-agreement, eaf]
level: advanced
status: draft
description: "Annotating sign-language video in ELAN: tier design, ID-glosses against a lexical database, non-manual tiers, notation choice (HamNoSys, SignWriting) and agreement checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Annotating sign-language video — ELAN tiers, ID-glosses and notation

**Goal:** turn recordings of signing into a searchable, consistent annotated corpus that
supports phonological, morphological and syntactic analysis.

> Draft. Practice drawn from published annotation guidelines of national sign-language
> corpus projects (e.g. BSL, Auslan, NGT, DGS corpora) as generally described; menu
> names in ELAN may differ by version. Adapt to your project's own guideline document.

## 1. Why ID-glosses are the backbone
Sign languages have no standard written form, so English-word glosses are the
annotation currency. The trap: one sign glossed three ways ("CAR", "DRIVE", "VEHICLE")
makes the corpus unsearchable. Fix: **ID-glosses** — a single unique label per lexical
sign, kept in a lexical database (e.g. a Signbank-style database) with a citation video.
Every token in the corpus points to one ID-gloss, regardless of its meaning in context.

## 2. ELAN setup
1. Create the `.eaf` file, link the video(s); for multi-camera recordings, sync them via
   a clap/flash visible in all angles.
2. Define **tier types** with **controlled vocabularies** where possible (glosses, handshape
   codes, non-manual values) so annotators pick, not type.
3. Typical tiers per signer (prefix each with the signer ID, e.g. `S1_`):
   - `RH-IDgloss`, `LH-IDgloss` — one tier per hand (signs can overlap/one hand holds).
   - `Translation` — free translation, aligned to clause/utterance.
   - `Mouth` (mouthing vs mouth gesture), `Brows`, `Head`, `Eyegaze` — non-manuals.
   - `Clause`/`Syntax` and `CA` (constructed action) tiers for higher-level analysis.
   - Optional `Notation` tier (HamNoSys/SignWriting) for phonological work.
4. Use **symbolic subdivision / referring tiers** for dependent annotations so they
   inherit the time span of the parent gloss.

## 3. Segmentation rules (write them down)
- Sign **onset**: the first frame where the handshape is formed and the hand begins the
  lexical movement (not the transition from the previous sign).
- Sign **offset**: last frame before the hand starts transitioning away.
- Decide and document how to treat holds, buoys (one hand held while the other signs),
  fingerspelling (one annotation per word, prefix like `FS:`), pointing (`PT:` plus target
  type), depicting signs (`DS:` plus classifier type), gestures (`G:`).
- Frame-accurate segmentation is slow; many projects accept a tolerance (e.g. a few frames)
  — state yours.

## 4. Notation choices
- **Stokoe notation:** historical ASL phonological notation (handshape, location,
  movement); limited for other languages.
- **HamNoSys:** language-independent phonetic notation of handshape, orientation,
  location, movement; machine-readable; steep learning curve.
- **SignWriting:** featural visual script used by some communities and educators; more
  readable to signers, less standardised for analysis.
- For most corpus work, ID-glosses + feature tiers are enough; reserve full notation for
  phonological studies.

## 5. Quality control
- **Double-annotate a sample** (e.g. 10%) with two annotators; compute agreement on
  gloss labels and boundaries (Cohen's kappa or similar for labels, onset/offset
  difference distribution for timing).
- **Gloss audit:** export all gloss values, sort, and find near-duplicates (`CAR`/`CAR2`/
  `car`) and glosses not in the lexical database.
- Use ELAN's multi-file search and export to tab-delimited text for statistics.
- Track annotation guideline versions; re-annotate older files when rules change.

## 6. Ethics and data
Signers are identifiable from video — faces carry grammar and can't be blurred without
destroying data. Get explicit consent for each use (research, public release, ML
training); involve Deaf researchers and community in design and annotation.

## Gotchas
- Glossing meaning-in-context rather than the lexical ID.
- Mixing both hands on one tier, losing two-handed simultaneity.
- Non-manuals left until "later" — never done.
- Uncontrolled free-text tiers → spelling variants.

## Verify
- [ ] Every gloss value exists in the lexical database (zero orphans in the audit).
- [ ] Two annotators agree above your project's threshold on a sample.
- [ ] Onset/offset rule is written and applied the same in random spot checks.
- [ ] Consent covers every planned use of the video.
