---
id: media-communication.library-and-archive-science.classification-and-taxonomy.building-a-controlled-vocabulary
name: building-a-controlled-vocabulary
category: media-communication
field: library-and-archive-science
product: classification-and-taxonomy
tags: [classification-and-taxonomy, classification, taxonomy, controlled-vocabulary, thesaurus, thesaurus-construction, iso-25964, ansi-niso-z39-19, dewey, ddc, lcc, library-of-congress-classification, lcsh, subject-analysis, aboutness, skos, broader-term, narrower-term, related-term, use-for, faceted-classification, synonym-ring, taxonomy-governance, knowledge-organisation]
level: practitioner
status: docs-checked
description: "Build a controlled vocabulary: pick the right scheme type (list, synonym ring, taxonomy, thesaurus), model it in SKOS, and use LC Classification resources."
sources: ["https://www.niso.org/publications/ansiniso-z3919-2005-r2010", "https://www.w3.org/TR/skos-reference/", "https://www.loc.gov/aba/cataloging/classification/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a controlled vocabulary (and applying classification)

**Goal:** make "what is it about?" consistent, either by applying an established scheme or
by building a fit-for-purpose vocabulary for an organisation's content, so search and
browse return the right things.

## 1. Know the standard and the scheme types
ANSI/NISO Z39.19-2005 (R2010), *Guidelines for the Construction, Format, and Management
of Monolingual Controlled Vocabularies*, gives guidelines and conventions for the
contents, display, construction, testing, maintenance and management of monolingual
controlled vocabularies. It covers vocabularies used to represent content objects in
knowledge organisation systems: **lists, synonym rings, taxonomies and thesauri**. Choose
the simplest of these that meets the need. The title says monolingual: multilingual
thesauri need other guidance (the tags name ISO 25964, which was not checked here).

## 2. Applying a library classification
The Library of Congress Classification (LCC) was developed in the late nineteenth and
early twentieth centuries to organise and arrange the Library of Congress's book
collections. The Library publishes the LCC Outline, the A-Z schedules and geographic
Cutter number tables (G1548-G9804) as downloads, and a regularly reviewed approved list
of additions and changes. Classification Web Plus is a product available for purchase,
and Library of Congress Subject Headings (LCSH) are a separate resource on the same site.
Check what your library subscribes to; current editions and licensing vary.

## 3. Modelling the vocabulary in SKOS
SKOS (W3C Recommendation, "SKOS Simple Knowledge Organization System Reference") is the
RDF data model for thesauri, taxonomies and similar schemes. Use:
- `skos:Concept` for each concept and `skos:ConceptScheme` for the scheme;
- `skos:prefLabel` and `skos:altLabel` for the preferred and alternative labels;
- `skos:broader` / `skos:narrower` for hierarchy (and `skos:broaderTransitive`) and
  `skos:related` for associative links; `skos:related` and `skos:broaderTransitive`
  are disjoint, so do not link the same pair both ways;
- documentation properties (scope notes, definitions, editorial notes) to say how a
  term should be used.
Keep the vocabulary in a form that can feed your CMS and search.

## 4. Test and govern
- Have two people tag the same sample independently; disagreement shows unclear terms or
  missing scope notes.
- Name an owner, a request process for new terms and a change log.
- Never delete a used term without recording its replacement (as an alternative label or
  mapping) so existing content and saved searches still work.

## Verify
- [ ] Scheme type (list, synonym ring, taxonomy, thesaurus) chosen deliberately.
- [ ] Every concept has one preferred label, with variants as alternative labels.
- [ ] Hierarchical and associative links use SKOS broader/narrower and related correctly.
- [ ] Scope notes written for contested terms; tagging consistency tested.
- [ ] Governance owner and change log exist.

## Checked
2026-11-09. Confirmed against the NISO Z39.19-2005 (R2010) abstract (scope and the four scheme types), the Library of Congress Classification and Shelflisting page (history, outline, A-Z schedules, Cutter tables G1548-G9804, approved lists, Classification Web Plus) and the W3C SKOS Reference (Concept, ConceptScheme, prefLabel, altLabel, broader, narrower, broaderTransitive, related, disjointness of related and broaderTransitive, documentation properties). Removed unconfirmed material: Dewey Decimal details, LCSH assignment counts, term-selection and facet advice, hierarchy depth, tool names, and ISO 25964 specifics.
Method: documentation only; no commands were run.
