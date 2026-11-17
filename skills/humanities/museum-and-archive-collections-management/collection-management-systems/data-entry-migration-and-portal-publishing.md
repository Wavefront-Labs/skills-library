---
id: humanities.museum-and-archive-collections-management.collection-management-systems.data-entry-migration-and-portal-publishing
name: data-entry-migration-and-portal-publishing
category: humanities
field: museum-and-archive-collections-management
product: collection-management-systems
tags: [collection-management-systems, cms, collections-database, tms, gallery-systems, emuseum, axiell, axiell-collections, adlib, calm, pastperfect, archivesspace, atom, access-to-memory, collectiveaccess, mimsy, specify, data-entry, data-standards, data-cleaning, openrefine, migration, data-mapping, csv-import, ead-export, lido, public-portal, online-collections, api, data-protection, spectrum]
level: practitioner
status: draft
description: "Run a collections database well (TMS, Axiell, PastPerfect, ArchivesSpace, AtoM): data-entry rules, clean-up queries, migration mapping and test loads, and safe public-portal publishing."
sources: ["Collections Trust, Spectrum 5.1 and 'Choosing a collections management system' guidance", "ArchivesSpace documentation (importers, EAD export)", "OpenRefine documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data entry, migration and portal publishing in a collections system

**Goal:** a collections database whose records are consistent enough to search,
report on, migrate and publish without embarrassment. Products differ in screens; the
discipline is the same. Menu names below are indicative — check your version.

## 1. Data-entry rules (write them down)
A one-page **data standards manual** per system beats any training:
- Which field holds what (e.g. "Object name = AAT preferred term only; Brief description
  = one sentence, no measurements").
- Formats: dates (display date + earliest/latest year), dimensions (cm, H × W × D),
  names (authority records, inverted "Surname, Forename").
- Mandatory fields at each stage (entry, accession, catalogue).
- What never goes in a public field: donor addresses, valuations, security notes,
  exact locations of vulnerable objects.
Use the system's authority/term lists and **lock** them so staff pick rather than type.
In ArchivesSpace and AtoM, link agents/subjects as records, not free text.

## 2. Clean-up
- Export to CSV and profile in **OpenRefine**: facet on object name, maker, place;
  cluster ("key collision", "nearest neighbour") to find variants (`Wedgewood` /
  `Wedgwood`); fix in the source system, or re-import with the system's batch update.
- Recurring reports: objects with no location, no image, no object name, duplicate
  numbers, loans past end date. Run them monthly.
- Always keep the pre-change export; batch edits are hard to undo.

## 3. Migration
1. **Inventory** the old system: tables, fields, codes, attachments, users, audit history.
2. **Field map** in a spreadsheet: source field → target field, transformation, owner,
   decision on fields with no home (usually into a notes field with a prefix).
3. **Clean before**, not after — the new system's validation rejects bad data or,
   worse, accepts it silently.
4. **Test loads** with a representative sample (all object types, multipart objects,
   loans, archives with deep hierarchy), then the full set into a test instance.
5. **Reconcile**: record counts per type, spot-check 50+ records field by field,
   images attached, hierarchies intact. Get sign-off.
6. Freeze the old system to read-only at cutover; keep an export permanently.
Common breaks: character encoding (é → Ã©; use UTF-8 end to end), date fields that
held text ("c.1800"), multi-value fields split wrongly, image file paths.

## 4. Publishing to a portal
- Publish from a **flag** (e.g. "Web: yes") reviewed by a curator, never "everything".
- Map only public fields; strip sensitive data; consider culturally sensitive material
  (sacred objects, human remains, images of the deceased) — consult communities.
- Attach rights statements to images; use IIIF if the portal supports it.
- Aggregators (Europeana, DPLA, Art UK, national archive catalogues) want specific
  exports (LIDO, EDM, EAD) — test one record end to end first.

## Gotchas
- Access controls: who can delete records? Usually nobody but the registrar.
- Back up the database *and* the media folder; restore-test once a year.
- Vendor upgrades can change export formats; retest your portal feed after each.
- Status: product capabilities change frequently; verify against vendor docs.

## Verify
- [ ] A written data standards manual exists and term lists are locked.
- [ ] Monthly gap reports run and the counts are going down.
- [ ] Migration reconciled with counts and sampled records, signed off.
- [ ] Portal feed exposes no private fields; rights on every image.
- [ ] A restore from backup has been tested in the last year.
