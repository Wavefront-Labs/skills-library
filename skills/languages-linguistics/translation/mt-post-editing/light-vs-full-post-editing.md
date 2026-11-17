---
id: languages-linguistics.translation.mt-post-editing.light-vs-full-post-editing
name: light-vs-full-post-editing
category: languages-linguistics
field: translation
product: mt-post-editing
tags: [mt-post-editing, mtpe, post-editing, pemt, machine-translation, nmt, neural-machine-translation, llm-translation, light-post-editing, full-post-editing, iso-18587, mt-errors, hallucination, omission, terminology, edit-distance, productivity, words-per-hour, deepl, google-translate, cat-tools, translation]
level: practitioner
status: draft
description: "Post-edit machine translation to the agreed level: light vs full PE criteria, the error patterns neural MT and LLMs make, a segment-by-segment method, and how to keep speed without missing errors."
sources: ["ISO 18587:2017 — post-editing of machine translation output", "TAUS post-editing guidelines (light/full quality levels)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Light vs full post-editing of machine translation

**Goal:** turn raw MT output into text that meets an agreed quality level — no more effort
than that level needs, no less — and catch the errors MT makes that read deceptively well.

## 1. Agree the level first
- **Light post-editing** ("good enough"): correct meaning is conveyed; fix mistranslations,
  omissions, additions, wrong terminology where it misleads, and anything offensive. Leave
  style that is awkward but understandable. Typical uses: internal docs, knowledge-base
  gisting, high-volume support content.
- **Full post-editing** ("publishable"): equivalent to human translation quality —
  correct meaning, terminology, grammar, punctuation, style guide, fluency and consistency.
  ISO 18587 describes full post-editing with requirements on post-editor competence.
Get it in writing, with the style guide, glossary and examples of acceptable output.
If the MT is so poor that post-editing is slower than translating, say so with a sample.

## 2. MT error patterns to hunt for
Neural MT and LLM output is **fluent**, so errors hide behind good grammar:
- **Omissions** — a clause, negation or list item silently dropped.
- **Additions/hallucinations** — plausible content not in the source (more common with LLMs
  and with short or noisy segments).
- **Negation and polarity flips**; modal shifts (*may* → *must*).
- **Terminology drift** — the same term rendered differently across segments; client terms
  ignored in favour of generic ones.
- **Numbers, units, dates, names, tags/placeholders** altered or reformatted.
- **Register/formality** — mixing *tu/vous* or *du/Sie* within a document.
- **Gender** defaults (e.g. professions assumed male); agreement errors over long distances.
- **Segment-level context loss** — pronouns and ellipsis resolved wrongly across sentence breaks.
- **Literal idioms** and false friends.

## 3. Method per segment
1. Read the **source first**, then the MT (reading MT first anchors you to its errors).
2. Decide: keep, edit, or retranslate. Edit minimally — rewriting acceptable MT wastes time
   in light PE and introduces new errors.
3. Check numbers/tags/terms explicitly; the eye skims them otherwise.
4. Run CAT QA (terminology, numbers, tags, consistency) after the batch.
5. For full PE, a final read of the target alone for flow.

## 4. Productivity and pricing awareness
- Track words per hour and **edit distance** (how much you changed) per job. Both show
  whether MT is helping. Post-editing throughput varies enormously by language pair, domain
  and engine quality. *Avoid accepting fixed "PE discounts" without measuring on a sample.*
- Fatigue lowers error detection; take breaks in long sessions.

## 5. Feedback loop
Report recurring MT errors to the client/LSP (terminology, formatting). Glossary injection or
engine customisation often fixes them at source.

## Gotchas
- Light PE that "fixes everything" is unbilled full PE; full PE that leaves MT flavour fails review.
- Fluency bias: a smooth sentence feels right — check it against the source anyway.
- MT can translate text inside tags or code; check placeholders as for localisation.
- Confidentiality: don't paste client content into public MT/LLM services unless permitted.
- Fuzzy TM matches and MT suggestions can conflict; follow the client's priority rule.

## Verify
- [ ] Agreed PE level, style guide and glossary are documented for the job.
- [ ] Every segment was compared source-first; omissions/additions/negations checked.
- [ ] CAT QA shows no number, tag or terminology mismatches.
- [ ] A sample reviewed against the level criteria (or an MQM-style score) passes.
- [ ] Throughput and edit distance logged for the job.

Related: `languages-linguistics.translation.translation-revision.bilingual-revision-and-mqm-error-typology`,
`languages-linguistics.translation.trados.translation-memory-termbase-and-project-packages`.
