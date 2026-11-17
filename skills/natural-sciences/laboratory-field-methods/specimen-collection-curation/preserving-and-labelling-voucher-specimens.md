---
id: natural-sciences.laboratory-field-methods.specimen-collection-curation.preserving-and-labelling-voucher-specimens
name: preserving-and-labelling-voucher-specimens
category: natural-sciences
field: laboratory-field-methods
product: specimen-collection-curation
tags: [specimen-collection-curation, voucher-specimen, natural-history-collection, museum-collection, herbarium, plant-press, pinning-insects, ethanol-preservation, formalin, tissue-sample, dna-preservation, silica-gel, rnalater, minus-80, specimen-labels, archival-paper, pigma-pen, darwin-core, specify, gbif, georeferencing, collecting-permits, nagoya-protocol, cites, accession, catalogue-number]
level: practitioner
status: draft
description: "Collect a voucher specimen that stays useful for decades: choose preservation for morphology vs DNA, take tissue, write archival labels with Darwin Core data, and deposit in a collection."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preserving and labelling voucher specimens

**Goal:** a physical specimen, with data, that lets anyone later verify the identity of
what your study measured or sequenced — preserved for both morphology and DNA, and
deposited where it will be catalogued and kept.

## 1. Before you collect
- **Permits:** collecting, export/import, and access-and-benefit-sharing (Nagoya
  Protocol) permits as applicable; CITES for listed species; landowner permission.
  Carry copies and record permit numbers — they go on the label/record.
- **Arrange deposit** with a museum, herbarium or university collection in advance; they
  may specify preservation and data standards.
- Pre-print field numbers (unique collector number series) and bring archival materials.

## 2. Preservation by group (typical practice)
| Group | Morphology | DNA/tissue |
|---|---|---|
| Vascular plants | Press flat in newspaper with blotters/corrugates, dry with gentle heat; include flowers/fruit and leaf both sides | Fresh leaf into **silica gel** (≥ 10× leaf volume), dried quickly |
| Fungi | Dry with warm air (dehydrator ~40–50 °C); photograph fresh first (colours fade) | Small piece on silica or in a DNA buffer |
| Insects | Pin (hard-bodied) or 70–80 % ethanol (soft-bodied, larvae) | A leg into 95–100 % ethanol, or whole specimen in 95 % ethanol kept cold |
| Fish/herps | Fix in 10 % buffered formalin, transfer to 70 % ethanol for storage | Tissue clip into 95 % ethanol **before** formalin |
| Birds/mammals | Study skin/skeleton by trained preparator | Tissue (muscle/liver) frozen at −80 °C or in ethanol/RNAlater |

Key rule: **formalin fragments DNA**. Take the genetic sample first and keep it separate,
linked by the same field number. Use enough ethanol (~10× specimen volume) and replace it
after a day or two as body water dilutes it.

## 3. Labels
- **Archival** paper (acid-free, ~100 % cotton rag) and **pigment ink** (e.g. archival
  pigment pens) or a laser printer; test that the ink survives ethanol before using it in
  fluid. Pencil on archival paper also survives ethanol.
- In fluid, the label goes **inside** the jar; an outside label alone will be lost.
- Minimum data (map to **Darwin Core** terms): catalogue/field number (`recordNumber`),
  collector(s) (`recordedBy`), date (ISO 8601, `eventDate`), country/state/locality
  description, **decimal latitude/longitude with datum and uncertainty in metres**,
  elevation/depth, habitat, collecting method, identifier and date identified, preparations.
- Locality text should still be findable without the GPS ("3.2 km NE of [town] on [road],
  north bank of [river]").

## 4. Digitise and deposit
- Enter data into a collection-management system (Specify, Arctos, EMu, Symbiota portals) or
  a well-structured spreadsheet in Darwin Core columns.
- Collections publish to aggregators such as **GBIF** and iDigBio; cite the catalogue
  numbers of vouchers in your paper and in GenBank records (`specimen_voucher` field).
- Photographs of the fresh specimen and its habitat, linked by number, add value.

## Gotchas
- Vouchers that stay in a lab freezer or office drawer are effectively lost; deposit them.
- Collecting threatened or locally rare species may be prohibited or unethical; photograph
  instead where a photo voucher is acceptable.
- Silica gel with indicator crystals must be replaced when saturated; slow drying ruins DNA.
- Never re-use field numbers; duplicates break the link between tissue and specimen.
- Handling formalin and large ethanol volumes requires ventilation, PPE and flammable-storage rules.

Uncertain here: preservation details vary by taxon and institution; the deposit
collection's own protocol overrides the generic table above.

## Verify
- [ ] Permits obtained and their numbers recorded with the specimen data.
- [ ] Tissue for DNA taken before fixation and linked by field number.
- [ ] Archival label inside the container with full locality, coordinates + uncertainty, date and collector.
- [ ] Data entered in Darwin Core-compatible fields.
- [ ] Specimen deposited and catalogue number cited in publications/sequence records.
