---
id: languages-linguistics.translation.translation-revision.bilingual-revision-and-mqm-error-typology
name: bilingual-revision-and-mqm-error-typology
category: languages-linguistics
field: translation
product: translation-revision
tags: [translation-revision, revision, bilingual-revision, review, proofreading, translation-qa, quality-assurance, lqa, mqm, multidimensional-quality-metrics, error-typology, severity, error-score, iso-17100, four-eyes, qa-tools, xbench, verifika, cat-qa, feedback, reviser, translation-quality]
level: practitioner
status: draft
description: "Revise another translator's work: bilingual comparison in fixed passes, MQM-style error categories and severities, automated QA, and feedback that fixes errors without rewriting preferences."
sources: ["MQM (Multidimensional Quality Metrics) framework, themqm.org", "ISO 17100:2015 — revision as a required step", "Mossop, Revising and Editing for Translators (Routledge)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bilingual revision and MQM error typology

**Goal:** a revised translation that is correct and fit for purpose, a defensible quality
score where one is required, and feedback that makes the translator better — while resisting
the urge to replace their good choices with your own.

## 1. Terms
- **Revision** (ISO 17100): a second linguist compares target against source (bilingual).
- **Review**: monolingual check of the target for domain/purpose (often by a subject expert).
- **Proofreading**: final check of the formatted output (typos, layout).
Clarify which one you're being paid for.

## 2. Pass structure (bilingual revision)
1. **Setup**: read the brief, style guide, glossary, reference material and the translator's
   queries/notes.
2. **Automated QA** (CAT built-in QA, or tools such as Xbench/Verifika): numbers, tags,
   terminology, untranslated segments, double spaces, inconsistency (same source → different
   target, and vice versa). Triage false positives; fix real ones.
3. **Bilingual comparison**, segment by segment: meaning, omissions, additions, terminology,
   grammar. Source first, then target.
4. **Monolingual read** of the target alone for flow, register and consistency.
5. **Final checks**: changed segments re-read; formatting in the final file/preview.

## 3. Classify errors (MQM-style)
MQM defines a hierarchy of issue types; common top-level dimensions include:
- **Accuracy/Terminology**: mistranslation, omission, addition, untranslated, wrong term.
- **Linguistic conventions**: grammar, spelling, punctuation.
- **Style**: register, awkwardness, house-style violations.
- **Locale conventions**: number, date, currency, address formats.
- **Design/markup**: tags, truncation, layout.
Severity levels (typical): **minor** (doesn't affect meaning or usability), **major**
(changes meaning or would confuse/annoy the reader), **critical** (could cause harm, legal or
safety risk, or block use). Scores are often penalty points per words (e.g. minor 1, major 5,
critical 25 — *weights vary by client scorecard; use theirs*), normalised and compared to a
pass threshold.

## 4. Preference vs error
Before changing anything, ask: *is it wrong, or just not how I'd say it?* Preferential changes:
- waste time and are a common source of new errors;
- inflate the error count unfairly;
- annoy translators and erode trust.
Mark them as "preferential/optional" or leave them. Exception: the client's style guide
explicitly requires your version.

## 5. Feedback
- Use tracked changes or the CAT tool's revision mode so every change is visible.
- Comment on **patterns**, not every instance: "dates in US format throughout — client wants
  DD/MM/YYYY".
- Give a reason and, where relevant, a source (glossary entry, style-guide section).
- Note what was done well; feedback that is only red ink gets ignored.
- If you're unsure, query rather than change.

## Gotchas
- Introducing errors: changing one word without fixing agreement elsewhere in the sentence.
- Reviewing only the target misses omissions — always compare.
- QA tool fatigue: hundreds of false positives make reviewers skip real ones; tune settings.
- Scorecard gaming: splitting one error into several, or rating everything major.
- Time: thorough bilingual revision commonly runs at a fraction of translation speed;
  quote accordingly. *No universal rate is given here.*

## Verify
- [ ] The job type (revision/review/proofread) and scorecard were agreed in advance.
- [ ] Automated QA run and every flag resolved or justified.
- [ ] Every change is tracked and classified by category and severity.
- [ ] Preferential edits are marked as such or omitted.
- [ ] Feedback summary lists patterns with sources, plus strengths.

Related: `languages-linguistics.translation.mt-post-editing.light-vs-full-post-editing`,
`languages-linguistics.translation.memoq.livedocs-termbases-and-qa-workflow`.
