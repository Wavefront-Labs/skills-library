---
id: languages-linguistics.translation.technical-translation.terminology-consistency-and-controlled-language
name: terminology-consistency-and-controlled-language
category: languages-linguistics
field: translation
product: technical-translation
tags: [technical-translation, translation, manuals, user-manual, specifications, datasheet, scientific-translation, terminology, termbase, glossary, terminology-consistency, controlled-language, simplified-technical-english, ste, asd-ste100, units, measurements, number-formats, safety-warnings, ansi-z535, iso-3864, cat-tools, translation-memory, iso-17100, reference-material]
level: practitioner
status: draft
description: "Translate manuals and specs accurately: glossary first, one term per concept, controlled-language source respected, numbers and units handled correctly, ambiguities queried."
sources: ["ISO 17100:2015 — translation services requirements", "ASD-STE100 Simplified Technical English specification", "Byrne, Technical Translation (Springer 2006)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terminology consistency and controlled language in technical translation

**Goal:** a translated manual, specification or technical paper that an engineer or
end user can act on safely: every concept named the same way every time, numbers and units
correct, instructions unambiguous.

## 1. Before translating: prepare
- **Read the whole document** and any reference material: previous translations, the
  client's glossary, the product UI strings (the manual must match the localised UI exactly).
- **Understand the thing**: look at drawings, photos, videos of the product. You can't
  translate "the pawl engages the ratchet" well without knowing what a pawl is.
- **Build or extend a project glossary** (termbase): source term, target term, definition or
  context, source of authority (standard, client, manufacturer), status (approved/proposed).
  Seed it from industry standards and the client's existing documents, not from a general dictionary.

## 2. One concept, one term
- Technical writing deliberately uses one term per concept; synonyms in a translation
  suggest different parts or actions ("bolt" vs "screw" are not stylistic variants).
- Never vary terms for elegance. Repetition is correct.
- If the *source* is inconsistent (two names for one part), query the client and record the
  answer in the glossary.
- Run a terminology QA check in your CAT tool (term verification against the termbase)
  before delivery.

## 3. Controlled-language sources
If the source is written in a controlled language (e.g. ASD-STE100 Simplified Technical
English: approved vocabulary, one meaning per word, short sentences, imperative
instructions), keep the target equally plain: one instruction per sentence, active voice,
action first. Some clients have a target-language controlled style too — ask.

## 4. Numbers, units, formats
- Decimal and thousands separators by locale: 1,234.5 (en-US) vs 1 234,5 (fr-FR) vs
  1.234,5 (de-DE). Never "fix" numbers inside part numbers, version strings or code.
- **Do not convert units** unless instructed; if converting, keep precision sensible and
  put the original in brackets if the client agrees. Torque, pressure and temperature
  errors are safety issues.
- Dates, tolerances (±), ranges (en dash vs "to"), and dimension order follow target conventions.
- Leave code, commands, file names, UI labels (unless localised), and placeholders untouched.

## 5. Safety messages
Hazard statements (DANGER / WARNING / CAUTION / NOTICE) follow standards (e.g. ANSI Z535,
ISO 3864 and regional regulations). Use the established target-language signal words the
client or regulator requires; don't invent new ones. *Which standard applies depends on market
and product type — confirm with the client.*

## 6. Queries
Keep a query sheet: segment ID, source, issue, proposed solution. Send batched queries early,
not at delivery. Record answers in the glossary/TM so they persist.

## Gotchas
- **Over-trusting the TM**: a 100% match from another product line may use a different term.
- **Abbreviations**: expand or keep per glossary; don't create new target abbreviations.
- **Gender/number agreement** with UI strings can force rephrasing in inflected languages.
- **Text expansion** (often +15–30% from English into Romance/Germanic languages) breaks
  layouts in tables and callouts — flag to DTP.
- Figures and screenshots may contain text that also needs translating.

## Verify
- [ ] A glossary exists; every key term in the delivery matches it (CAT term check passes).
- [ ] UI references match the localised software strings exactly.
- [ ] Numbers, units, part numbers and placeholders compared source vs target (CAT number check).
- [ ] Safety messages use approved signal words and wording.
- [ ] All queries resolved or listed in the delivery note.

Related: `languages-linguistics.translation.trados.translation-memory-termbase-and-project-packages`,
`languages-linguistics.translation.memoq.livedocs-termbases-and-qa-workflow`,
`media-communication.technical-writing.style-guides.house-style-and-terminology-management`.
