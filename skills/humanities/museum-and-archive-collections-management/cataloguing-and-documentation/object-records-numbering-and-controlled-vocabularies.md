---
id: humanities.museum-and-archive-collections-management.cataloguing-and-documentation.object-records-numbering-and-controlled-vocabularies
name: object-records-numbering-and-controlled-vocabularies
category: humanities
field: museum-and-archive-collections-management
product: cataloguing-and-documentation
tags: [cataloguing-and-documentation, cataloguing, object-record, catalogue-record, spectrum, spectrum-5, cco, cataloging-cultural-objects, cdwa, lido, getty-aat, aat, ulan, tgn, controlled-vocabulary, thesaurus, authority-file, object-number, accession-number, object-marking, labelling, measurements, condition-report, object-name, museum-documentation, collections-trust, registrar, inventory]
level: practitioner
status: docs-checked
description: "Write a museum object record to standard: Spectrum inventory, numbering and marking, controlled terms (AAT, ULAN, TGN), and measurements others can trust."
sources:
  - https://collectionstrust.org.uk/spectrum/procedures/inventory-spectrum-5-0/
  - https://collectionstrust.org.uk/spectrum/procedures/
  - https://vocab.getty.edu/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object records, numbering and controlled vocabularies

**Goal:** a record that lets a stranger find the object, recognise it on the shelf,
search for it alongside similar things and know what is fact versus opinion.

## 1. Minimum record first, enrichment later
Spectrum's Inventory procedure helps you hold "basic information to be accountable for
the objects in your care", and points to a separate "Inventory - the Spectrum standard"
resource for the minimum requirements: use that list, not a remembered one. Get every
object to that level before writing scholarly essays on a few — an un-inventoried store
is a security risk.

Then catalogue: title (if it has one), maker/role, date, place, materials and technique,
dimensions, inscriptions/marks, subject, provenance summary, references, images.

## 2. Numbering and marking
- Use the institution's existing scheme exactly (e.g. `1998.27.3a-b` for a two-part
  object). Parts share a base number with suffixes; record "number of parts" so a
  missing lid is noticed.
- Mark reversibly and discreetly, never on a decorated face or a break edge, and use
  tie-on tags for objects that can't be marked. Method choice is material-specific:
  agree it with a conservator first. This list is a summary, not a procedure.
- Photograph the object **with its number visible** at cataloguing time.

## 3. Controlled vocabulary: the search depends on it
- **Object name** from a thesaurus (Getty **AAT**, the Art & Architecture Thesaurus of
  generic concepts) — "teapot", not "tea pot", "Tea-pot", "pot (tea)".
- **People and organisations** from an authority (Getty **ULAN**, Union List of Artist
  Names) with the role: *maker*, *designer*, *publisher*, *previous owner*.
- **Places** from **TGN** (Getty Thesaurus of Geographic Names); say what the place
  means (*made*, *found*, *used*).
- Keep a local authority file for terms the thesauri lack; never let free text
  multiply variants.

## 4. Write facts so they stay facts
- **Dimensions**: say what was measured and how — "H 23.4 cm × W 18 cm (max, with
  handle)"; metric, a consistent order, units on every value.
- **Dates**: a display date ("about 1760–70") plus machine earliest/latest years
  (1755/1775) so the date is searchable.
- **Attribution qualifiers**: "attributed to", "workshop of", "after" — controlled, not
  invented each time.
- **Inscriptions**: transcribe exactly, position and method ("painted, underside: 'W'").
- **Source of every claim**: who said so, where. "Donor said it belonged to her
  grandfather" is provenance information, not fact.

## Gotchas
- Free-text "description" fields full of key facts cannot be searched or migrated;
  put facts in the right field.
- Legacy records: never overwrite an old attribution silently. Add the new one with a
  date and reason; keep the history.
- Uncertainty is data. "Unknown" is better than a plausible guess left unflagged.
- Field names differ between cataloguing standards (e.g. Spectrum vs CCO/CDWA): map them,
  don't mix them within one system.

## Checked
2026-11-01. Confirmed: the Spectrum Inventory procedure wording and that the minimum list sits in a separate resource (Collections Trust Inventory page); AAT, ULAN and TGN full names and scope (Getty Vocabularies home page). Removed: the remembered inventory field list, Paraloid B-72 marking method, MDS/SHIC lists, LCNAF, Wikidata, GeoNames, CCO measurement order. CCO and CDWA are named only as other standards; their texts were not read.
Method: documentation only; no commands were run.

## Verify
- [ ] Every object meets the inventory minimum, including current location.
- [ ] Number on object = number in record = number in photo.
- [ ] Object name, people and places come from named vocabularies.
- [ ] Dimensions have units and say what was measured; dates have earliest/latest.
- [ ] Opinion and attribution carry a source and a qualifier.
