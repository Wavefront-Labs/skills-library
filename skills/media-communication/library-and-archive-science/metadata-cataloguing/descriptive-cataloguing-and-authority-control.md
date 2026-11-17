---
id: media-communication.library-and-archive-science.metadata-cataloguing.descriptive-cataloguing-and-authority-control
name: descriptive-cataloguing-and-authority-control
category: media-communication
field: library-and-archive-science
product: metadata-cataloguing
tags: [metadata-cataloguing, cataloguing, cataloging, descriptive-cataloguing, marc21, marc, rda, aacr2, dublin-core, metadata, authority-control, name-authority, lcnaf, viaf, isni, orcid, copy-cataloguing, original-cataloguing, oclc, worldcat, bibframe, metadata-quality, controlled-access-points, librarianship]
level: practitioner
status: docs-checked
description: "Describe items so they can be found: copy vs original cataloguing, core MARC 21 bibliographic fields, Dublin Core elements, and LC authority files."
sources: ["https://www.loc.gov/marc/bibliographic/", "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/", "https://id.loc.gov/", "https://www.loc.gov/marc/bibliographic/bd245.html", "https://www.loc.gov/marc/bibliographic/bd264.html", "https://www.loc.gov/marc/bibliographic/bd040.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptive cataloguing and authority control

**Goal:** create records that let users find and identify items, consistently enough
that searches and facets work across the whole collection.

## 1. Copy before original
- **Copy cataloguing:** search a shared database for an existing record, then match it to
  the item in hand (edition, publisher, date, extent, format); an identifier alone may be
  reused or wrong.
- Edit imported records to local standards (call number, holdings, local subjects).
- **Original cataloguing** only when no acceptable record exists.

## 2. Core MARC 21 bibliographic fields
The MARC 21 Format for Bibliographic Data (Library of Congress) defines each field.
| Tag | Content (as named in the format) |
|---|---|
| 020 | International Standard Book Number |
| 040 | Cataloging source; `$e` is Description conventions (example value `rda`) |
| 100 / 110 | Main entry: personal name / corporate name |
| 245 | Title statement: `$a` title, `$b` remainder of title, `$c` statement of responsibility |
| 250 | Edition statement |
| 264 | Production, publication, distribution, manufacture and copyright notice; `$a` place, `$b` name, `$c` date |
| 300 | Physical description |
| 336 / 337 / 338 | Content type / media type / carrier type |
| 490 | Series statement |
| 505 / 520 | Formatted contents note / summary |
| 650 | Subject added entry: topical term |
| 700 / 710 | Added entry: personal name / corporate name |
- In 245 the second indicator is the number of nonfiling characters (0 for none, 1-9
  for the count), so that filing ignores an initial article.
- In 264 the second indicator gives the function of the entity: 0 production,
  1 publication, 2 distribution, 3 manufacture, 4 copyright notice date.

## 3. Dublin Core for digital collections
The fifteen-element Dublin Core (the `/elements/1.1/` namespace, corresponding to
ISO 15836-1:2017) comprises contributor, coverage, creator, date, description, format,
identifier, language, publisher, relation, rights, source, subject, title and type. The
wider DCMI Terms vocabulary adds qualified terms. Write down which elements your
collection requires, which are repeatable and which vocabularies apply.

## 4. Authority control
The same person or body must appear in one form so all their works collocate.
- id.loc.gov (the Library of Congress Linked Data Service) provides the LC Name
  Authority File, LC Subject Headings, LC Classification, genre/form terms, language
  and country codes, the BIBFRAME ontology and PREMIS preservation vocabularies.
- Use the authorised form exactly as found and, where your system supports it, store the
  authority's URI.

## 5. Metadata quality
- Required elements present; controlled fields use their vocabulary; dates in one format.
- Use facets or reports to spot variant forms of the same name or place.

## Gotchas
- Accepting a copy record for a different edition or format.
- A wrong nonfiling indicator in 245 makes titles file under "The".
- Free-text names with no authority link split author facets.

## Verify
- [ ] Copy records matched on edition, date, extent and format.
- [ ] 245, 264, 300 and 336-338 present and consistent with the item.
- [ ] Names use an authorised form (with URI where supported).
- [ ] Digital collection has written element rules.
- [ ] Facet review shows no obvious variant duplicates.

## Checked
2026-11-09. Confirmed against the Library of Congress MARC 21 bibliographic field pages (020, 040, 100, 110, 245, 250, 264, 300, 336, 337, 338, 490, 505, 520, 650, 700, 710: titles, subfields, the 245 and 264 second indicators and the 040 `$e` description conventions example `rda`), the DCMI Terms page (fifteen elements, ISO 15836-1:2017) and the id.loc.gov service listing. Removed unconfirmed claims: RDA transcription rules, the LRM user tasks, WorldCat, VIAF/ISNI/ORCID and NACO workflow, subfield 670 and 4XX practice, DCMI Type/ISO 639/W3CDTF recommendations, OpenRefine, and the BIBFRAME adoption comment.
Method: documentation only; no commands were run.
