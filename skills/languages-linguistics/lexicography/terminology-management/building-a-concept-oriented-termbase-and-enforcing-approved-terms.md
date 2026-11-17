---
id: languages-linguistics.lexicography.terminology-management.building-a-concept-oriented-termbase-and-enforcing-approved-terms
name: building-a-concept-oriented-termbase-and-enforcing-approved-terms
category: languages-linguistics
field: lexicography
product: terminology-management
tags: [terminology-management, termbase, term-base, glossary, terminology, concept-oriented, term-record, iso-704, iso-1087, tbx, iso-30042, term-extraction, term-candidates, preferred-term, admitted-term, deprecated-term, forbidden-term, multiterm, trados, memoq, phrase-tms, qa-checks, xbench, translation, localisation, controlled-language]
level: advanced
status: draft
description: "Build and govern a termbase: one record per concept with preferred, admitted and forbidden terms, extraction from your corpus, TBX exchange, and enforcement in authoring and translation QA."
sources: ["ISO 704 Terminology work — Principles and methods", "ISO 30042 TermBase eXchange (TBX)", "ISO 1087 Terminology work — Vocabulary"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a concept-oriented termbase and enforcing approved terms

**Goal:** everyone — writers, translators, support staff, software — uses the same agreed
term for the same thing in every language, and you can prove which term is approved and why.
(House-style glossaries for a single writing team are covered in
`media-communication.technical-writing.style-guides.house-style-and-terminology-management`;
this skill is the multilingual, database side.)

## 1. Concept first, not word first
A termbase entry represents **one concept**, with all its terms in all languages beneath it.
This is the core rule from ISO 704 and the reason termbases beat bilingual word lists.
- Same word, two concepts (e.g. *port* as a network endpoint vs a harbour) → **two entries**.
- Two words, one concept (*e-mail*, *email*, *electronic mail*) → **one entry, several terms**
  with different statuses.
Write a short **definition** for each concept; without one, translators guess and duplicates
creep in.

## 2. Design the record
Keep the data categories few and actually filled. A workable core:
- **Concept level:** ID, subject field/product, definition (with source), notes, image if helpful.
- **Language level:** definition in that language if needed.
- **Term level:** term, part of speech, **usage status** (*preferred*, *admitted*,
  *deprecated/forbidden*), context sentence, source, date, approver.
This mirrors the TBX structure (concept entry → language section → term section).
Decide **who approves** each language and record it.

## 3. Find the terms (extraction)
- Run **term extraction** on your documentation, UI strings and existing translation
  memories; tools rank candidates by frequency and "termhood" (multi-word noun phrases that
  are specific to your domain).
- Expect noise: review candidates with a subject expert. Prioritise **high-frequency,
  high-risk** terms — UI labels, safety terms, legal and product names.
- Mine **inconsistencies**: the same source term translated three ways in your TM is a
  termbase entry waiting to happen.
- Start small: 200 well-researched entries beat 5,000 unreviewed ones.

## 4. Exchange and tools
- **TBX (ISO 30042)** is the XML interchange format; most translation environments (Trados
  MultiTerm, memoQ, Phrase and others) import/export it, though dialect support varies — test a
  round trip with a few entries before migrating thousands. CSV/Excel import is common but
  loses structure; map columns carefully.
- Keep **one master** termbase; tool-specific copies are exported from it, never edited separately.

## 5. Enforce
- **Authoring:** controlled-language checkers or editor plug-ins flag forbidden terms as
  writers type.
- **Translation:** the CAT tool shows approved terms in context; **QA checks** (built into the
  CAT tool or tools such as Xbench) flag segments where the source term appears but the
  approved target term doesn't, and where forbidden terms appear.
- **Feedback loop:** a simple request form for new terms or disputes, with a turnaround
  promise; otherwise people work around the termbase.

## Gotchas
- Status without reason: record *why* a term is forbidden (legal, brand, ambiguity) so it
  isn't reintroduced.
- Inflected languages: QA checks on exact forms raise false alarms; use fuzzy/stem matching
  options where available.
- Product renames: deprecate the old term (don't delete) so legacy content can be found.
- Termbases decay: schedule reviews per product release.

## Verify
- [ ] Every entry has one concept, a definition and at least one preferred term.
- [ ] No two entries share the same concept; ambiguous words are split.
- [ ] Forbidden terms carry a reason and the approved alternative.
- [ ] TBX round trip tested in your CAT tool without loss of status fields.
- [ ] QA run on a recent translation flags forbidden or missing approved terms as expected.
