---
id: creative-arts.design-for-form-and-experience.ux-design.designing-labelling-systems-and-taxonomies
name: designing-labelling-systems-and-taxonomies
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [labeling-system, taxonomy-design, labelling-system, controlled-vocabulary, information-architecture, navigation-labels]
level: practitioner
status: draft
description: "Design labelling systems and taxonomies: gather user vocabulary, set naming rules, build a controlled vocabulary and facets, and test labels with users."
sources:
  - "Louis Rosenfeld, Peter Morville and Jorge Arango, Information Architecture, 4th ed. (O'Reilly, 2015)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Labelling systems and taxonomy design

Rosenfeld, Morville and Arango list labelling alongside organisation, navigation and search as the main systems in information architecture. Labels are the words that represent content in navigation, headings, links and metadata.

## Labels
1. **Gather the language users use:** search logs, support tickets, card sort group names (see `...ux-design.running-an-open-or-closed-card-sort`), interview quotes.
2. **Set rules:** use plain words; be consistent in grammar (nouns or verb phrases, not mixed), case and number; avoid jargon, brand-only names and ambiguous terms such as "Resources"; keep to the same label for the same thing everywhere; make it scannable (front-load the key word).
3. **Create a style guide** with approved terms and banned ones (see `...ux-design.defining-voice-and-tone-guidelines`).
4. **Test** labels in tree tests and first-click tests (see `...ux-design.running-a-tree-test`).

## Taxonomy and metadata
- **Controlled vocabulary:** a list of preferred terms with synonyms (variants map to preferred); optionally broader and narrower relationships (hierarchy), related terms and scope notes.
- **Facets:** independent attributes (type, topic, audience, location) to filter large sets, designed so that values are mutually exclusive within a facet.
- **Governance:** owner, change process, review cycle, how to propose new terms.

## Gotchas
- Mixing categories (type and topic) in one list.
- A taxonomy only an expert understands; check against user vocabulary.

## Verify
- [ ] Each term has a definition and synonyms.
- [ ] Facets are independent and cover the content.
- [ ] Label tests show the target success rate.
