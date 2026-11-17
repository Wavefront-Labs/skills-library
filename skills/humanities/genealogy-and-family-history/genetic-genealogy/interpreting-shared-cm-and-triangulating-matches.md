---
id: humanities.genealogy-and-family-history.genetic-genealogy.interpreting-shared-cm-and-triangulating-matches
name: interpreting-shared-cm-and-triangulating-matches
category: humanities
field: genealogy-and-family-history
product: genetic-genealogy
tags: [genetic-genealogy, genealogy, dna, autosomal-dna, atdna, centimorgans, cm, shared-cm, shared-cm-project, dna-painter, what-are-the-odds, wato, segments, chromosome-browser, triangulation, leeds-method, match-clustering, shared-matches, endogamy, pedigree-collapse, ydna, mtdna, x-dna, ancestry-dna, 23andme, myheritage, ftdna, gedmatch, ethnicity-estimates]
level: practitioner
status: draft
description: "Read autosomal DNA matches: what shared cM can and can't tell you, using the Shared cM Project ranges, clustering with the Leeds method, triangulating segments, and handling endogamy."
sources:
  - "Bettinger, B. The Shared cM Project (v4, 2020) and DNA Painter's Shared cM tool"
  - "Bettinger, B. & Wayne, D. P. (eds) Genetic Genealogy in Practice (NGS, 2016)"
  - "International Society of Genetic Genealogy (ISOGG) Wiki"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interpreting shared cM and triangulating matches

**Goal:** use autosomal DNA matches to test or discover relationships, combined with
documentary research, without over-reading the numbers.

## 1. What the test gives you
- **Autosomal DNA (atDNA):** inherited from all ancestral lines, useful to roughly 5th–6th
  cousins; the main tool. Tested at Ancestry, 23andMe, MyHeritage, FamilyTreeDNA.
- **Y-DNA** (direct paternal line, men only) and **mtDNA** (direct maternal line) answer
  narrower questions over longer spans.
- **Ethnicity estimates** are not evidence for specific relationships. Ignore them for
  proof work.

## 2. Shared centimorgans → possible relationships
- A cM is a measure of genetic length; the total you share with a match predicts a **range**
  of relationships, not one. Example ranges (Shared cM Project v4, approx.):
  - Parent/child: ~3,330–3,720 (and full-identical segments pattern distinguishes from siblings)
  - Full sibling: ~1,600–3,500
  - Half sibling / grandparent / aunt-uncle: ~1,150–2,300 (these overlap heavily)
  - First cousin: ~400–1,400
  - Second cousin: ~40–600
  *Ranges quoted from memory of the project's published data; check the current DNA Painter tool.*
- Enter the cM in DNA Painter's Shared cM tool for probabilities. Use **age**, **number of
  segments** and **largest segment** to narrow candidates (e.g. half-sibling vs grandparent).
- Below ~20 cM, many matches share DNA from deep or false-positive segments; treat
  single segments under ~7–10 cM with great caution.

## 3. Organise matches: Leeds method / clustering
1. List matches in the 2nd–3rd cousin band (roughly 90–400 cM).
2. For each, check **shared matches** and give each group a colour.
3. Typically four clusters emerge = your four grandparents' lines.
Ancestry's colour-coded groups, MyHeritage AutoClusters and GEDmatch tools automate this.
Then identify the common ancestor in each cluster from matches' trees — and verify those
trees with records (see
`humanities.genealogy-and-family-history.records-research.applying-the-genealogical-proof-standard`).

## 4. Triangulation
- Where segment data is available (23andMe, MyHeritage, FTDNA, GEDmatch — **not** Ancestry),
  **triangulation** = three or more people share an overlapping segment on the same
  chromosome *and* match each other on it. That segment likely came from a common ancestor.
- Map confirmed segments to ancestors with DNA Painter to see which lines are where.
- Use "What Are The Odds?" (WATO) to score hypotheses for where an unknown person fits in a tree.

## 5. Endogamy and pedigree collapse
In endogamous populations (e.g. Ashkenazi Jewish, some island, Acadian, colonial or
religious communities) people share DNA through many lines: totals are inflated, many small
segments appear, and predicted relationships come out too close. Lean on largest segment,
use higher thresholds, and expect lots of matches.

## Gotchas
- Shared cM ranges overlap; one number never proves a specific relationship alone.
- Misattributed parentage, adoption and donor conception are common surprises; prepare before testing.
- Transferring raw data between sites has terms and privacy implications (law-enforcement
  matching opt-ins differ). Read them; get consent for kits you manage.
- A match's tree can be wrong; their DNA isn't.

## Verify
- [ ] Each relationship hypothesis uses cM, segments, ages and records together.
- [ ] Matches are clustered into lines before trees are trusted.
- [ ] Triangulated segments are mutually matching, not just overlapping.
- [ ] Endogamy considered where relevant.
- [ ] Consent and privacy terms checked for every kit managed or transferred.
