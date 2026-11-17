---
id: humanities.history.quantitative-and-digital-history.building-a-dataset-from-historical-records
name: building-a-dataset-from-historical-records
category: humanities
field: history
product: quantitative-and-digital-history
tags: [quantitative-and-digital-history, digital-history, digital-humanities, quantitative-history, cliometrics, historical-data, data-entry, data-model, source-oriented, record-linkage, nominal-record-linkage, standardisation, coding-schemes, hisco, occupations, census-data, parish-registers, openrefine, spreadsheet, csv, sqlite, python, r, text-mining, topic-modelling, ocr, historical-gis, data-documentation]
level: practitioner
status: draft
description: "Turn historical records into analysable data: source-oriented transcription, keeping raw and coded values separate, standard coding schemes, record linkage, and documenting it all for reuse."
sources:
  - "Feinstein, C. & Thomas, M. Making History Count: A Primer in Quantitative Methods for Historians (2002)"
  - "Graham, S., Milligan, I. & Weingart, S. Exploring Big Historical Data: The Historian's Macroscope (2nd ed., 2022)"
  - "The Programming Historian (programminghistorian.org) lessons"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a dataset from historical records

**Goal:** convert registers, censuses, ledgers or texts into structured data you can
count, link and map — without losing the link back to the source or baking in decisions
you'll later regret.

## 1. Design before data entry
- Write down the **question** and the unit of analysis (a person, a household, a
  transaction, a ship voyage). The unit decides the table structure.
- Prefer a **source-oriented** model: transcribe each record as the source has it, one
  row per source entry, then derive analytical variables. Rebuilding from the source later
  is far more expensive than storing it once.
- Plan tables, not one giant sheet: e.g. `records` (one per entry), `persons`
  (after linkage), `places`, `sources`. A spreadsheet works for small projects;
  SQLite or a relational database for anything with linkage.
- Every row carries a **source reference** (archive, piece, folio, line) and a stable `id`.

## 2. Transcription rules
- Keep **raw** (as written) and **standardised** values in separate columns:
  `occupation_raw = "Ag Lab"`, `occupation_std = "agricultural labourer"`, `hisco = 62105`.
- Record uncertainty explicitly (a `flag` or `certainty` column), and blanks as blank vs
  "illegible" vs "not recorded" — they mean different things.
- Dates in ISO form (`1851-03-30`) plus a raw-date column for odd originals; note calendar.
- Double-key a sample (two people enter the same records) and measure disagreement.

## 3. Coding schemes
Use published schemes so results are comparable: **HISCO** for occupations (with HISCLASS
for social class), standard place gazetteers, ICD-style schemes for historical causes of death
(*check which version fits your period*). Store the scheme name and version.
Tools: **OpenRefine** is excellent for clustering variant spellings ("Ag Lab", "Agr Labr")
before coding.

## 4. Record linkage
- Linking the same person across sources (census 1851 → 1861, baptism → burial) uses
  name, age/birth year, birthplace, household context.
- Standardise names (phonetic codes like Soundex or Double Metaphone help, but over-match),
  allow ±2 years on ages, and require multiple agreeing fields.
- Keep a linkage table with a **confidence score** and the rule used; never overwrite
  the original records with linked identities.
- Report false-match and missed-match rates from a hand-checked sample.

## 5. Text mining (if your source is text)
OCR quality is the first problem; measure it on a sample before modelling. Topic models and
word frequencies reflect the corpus composition (which newspapers survived/digitised), so
describe the corpus and its gaps.

## 6. Analysis and documentation
- Describe denominators and missingness before any rate or trend.
- Keep a **codebook** (every field, values, rules) and a **changelog**; keep processing in
  scripts (Python/R) rather than manual spreadsheet edits, so it can be rerun.
- Deposit data with documentation in a repository if licence allows.

## Gotchas
- Survival bias: records that survive are not a random sample of records made.
- Spreadsheets mangle dates and leading zeros (and turn some codes into numbers); import as text.
- Ages in historical sources heap at round numbers (30, 40) — age heaping is itself measurable.
- Personal data of potentially living people (recent censuses) needs data-protection care.

## Verify
- [ ] Every row has a stable id and full source reference.
- [ ] Raw and standardised values are stored separately.
- [ ] Coding schemes named with versions; codebook complete.
- [ ] Linkage rules and error rates documented.
- [ ] Analysis reproducible from scripts.
