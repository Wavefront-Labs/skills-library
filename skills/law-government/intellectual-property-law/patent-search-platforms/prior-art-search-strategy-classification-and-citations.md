---
id: law-government.intellectual-property-law.patent-search-platforms.prior-art-search-strategy-classification-and-citations
name: prior-art-search-strategy-classification-and-citations
category: law-government
field: intellectual-property-law
product: patent-search-platforms
tags: [intellectual-property-law, patent-search-platforms, prior-art-search, patentability-search, invalidity-search, fto-search, espacenet, patbase, derwent, dwpi, derwent-innovation, google-patents, patentscope, uspto-ppubs, orbit, cpc, ipc, classification-search, boolean, proximity-operators, truncation, patent-family, inpadoc, citation-analysis, forward-citations, backward-citations, non-patent-literature, search-report]
level: practitioner
status: docs-checked
description: "Search prior art on Espacenet, PatBase, Derwent and similar: concept tables, keyword plus CPC/IPC classification, family deduplication, citation chasing and a reproducible search report."
sources: ["35 U.S.C. 122 (https://www.law.cornell.edu/uscode/text/35/122)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prior-art search strategy, classification and citations

**Goal:** find the closest prior art efficiently and prove you looked properly, using
commercial (PatBase, Derwent Innovation, Orbit) or free (Espacenet, Google Patents,
WIPO PATENTSCOPE, USPTO Patent Public Search) platforms. Query syntax differs per
platform and changes between releases — field codes below are examples to check against
the platform's current help page.

## 1. Pick the search type — it changes scope
| Search | Question | Date cut-off | Documents |
|---|---|---|---|
| Patentability | Is our invention new/inventive? | Before our priority date | All publications, any country, any status |
| Invalidity | Can we kill their patent? | Before *their* priority date | All publications, plus products/sales evidence |
| Freedom-to-operate | Can we sell this? | None (in-force only) | Granted/pending in launch countries; claims matter |
| State of the art / landscape | What exists? | Optional | Broad, statistical |

## 2. Build a concept table
Break the invention into 2–4 core concepts. For each, list synonyms, broader and
narrower terms, spelling variants (US/UK), acronyms, and relevant classification codes.

| Concept | Keywords | CPC/IPC |
|---|---|---|
| A: wearable | wearable, wrist*, watch, band, strap | (look up in the CPC scheme) |
| B: glucose sensing | glucose, blood sugar, glycaem*/glycem* | (look up in the CPC scheme) |

Search concept A AND concept B; use OR within concepts. Start broad, narrow on volume.

## 3. Keyword technique
- **Truncation** (`sens*`) and wildcards — check which character the platform uses.
- **Proximity** beats AND for precision: words within n words of each other or in the same
  sentence/paragraph (platform-specific operators; check the platform's help page).
- Field limits: title/abstract/claims vs full text. Full text finds more but noisier;
  claims-only is useful for FTO.
- Remember non-English documents: rely on classifications, machine translations and
  family members in English.

## 4. Classification searching
Keywords miss documents using unexpected words; classifications don't.
- **CPC** (Cooperative Patent Classification) and **IPC** are the main schemes. Browse the scheme from known relevant documents: look at the
  codes on the three best hits and search those codes.
- Combine class + a light keyword filter for manageable sets.
- Watch class hierarchy: searching a group may or may not include subgroups depending on
  syntax.

## 5. Families and citations
- Collapse results to **one record per family** (simple or extended/INPADOC family) to
  avoid reviewing the same invention many times.
- **Backward citations** (what a key document cites) and **forward citations** (later
  documents citing it) are high-yield. Examiner citations especially.
- Search reports of related families show what examiners found.

## 6. Non-patent literature (NPL)
Journals, conference proceedings, standards documents, theses, product manuals, archived
websites (e.g. via web archives — record capture dates). In software and biotech, NPL
often holds the best art.

## 7. Report
Record for reproducibility: databases and dates searched, every query string with hit
counts, classifications used, review method, and the ranked list of relevant documents
with passages/figures mapped to claim elements. An undocumented search can't be defended
or rerun.

## Gotchas
- Publication date vs priority date: art must be public *before* the relevant priority date.
- US applications are published promptly after 18 months from the earliest filing date
  (35 U.S.C. 122(b)(1)(A)) — recent art may be invisible.
- Platform coverage varies; check each platform's coverage tables.
- Confidentiality: don't type unfiled invention details into tools whose terms you haven't
  checked.

## Verify
- [ ] Search type and correct cut-off date chosen.
- [ ] Concept table includes synonyms and CPC/IPC codes for each concept.
- [ ] Both keyword and classification strategies run; results deduplicated by family.
- [ ] Forward/backward citations of top hits reviewed; NPL searched.
- [ ] Search log with queries, dates and hit counts saved with the report.

## Checked
Checked 2026-10-24. Jurisdiction: international search practice with US publication rule. Source read 2026-10-24: 35 U.S.C. 122(b)(1)(A) (publication promptly after 18 months from the earliest filing date). The skill is otherwise search craft. Removed the unconfirmed CPC example codes, Espacenet proximity syntax, DWPI and PatBase claims, the CPC-user list and platform coverage and logging statements. General information, not legal advice.
Method: documentation only; no commands were run.
