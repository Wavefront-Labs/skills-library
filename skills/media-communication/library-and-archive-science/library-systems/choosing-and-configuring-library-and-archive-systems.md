---
id: media-communication.library-and-archive-science.library-systems.choosing-and-configuring-library-and-archive-systems
name: choosing-and-configuring-library-and-archive-systems
category: media-communication
field: library-and-archive-science
product: library-systems
tags: [library-systems, ils, integrated-library-system, library-services-platform, koha, evergreen, alma, folio, archivesspace, dspace, omeka, islandora, atom, access-to-memory, opac, discovery-layer, circulation, circulation-rules, patron-records, cataloguing-module, marc-import, z39-50, oai-pmh, digital-collections, institutional-repository, finding-aids, ead, migration]
level: practitioner
status: draft
description: "Pick and configure library and archive systems: ILS (Koha, Alma, FOLIO), ArchivesSpace, DSpace and Omeka; circulation rules, record imports and system migration."
sources: ["https://koha-community.org/documentation/", "https://archivesspace.org/", "https://wiki.lyrasis.org/display/DSDOC", "https://omeka.org/classic/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing and configuring library and archive systems

**Goal:** match the system to the job, configure it so staff work efficiently and users
can find things, and migrate between systems without losing data.

## 1. Which class of system does the job?
| Job | System class | Examples |
|---|---|---|
| Catalogue, circulation, acquisitions, serials for a library | ILS / library services platform | Koha, Evergreen (open source); Alma, FOLIO, Sierra-class (commercial/hosted) |
| User-facing search across catalogue + e-resources | Discovery layer | Primo, EBSCO Discovery, VuFind, Blacklight |
| Archival description, accessions, finding aids | Archival management | ArchivesSpace, AtoM (Access to Memory) |
| Institutional repository (theses, papers, datasets) | Repository | DSpace, EPrints, Samvera/Hyrax |
| Curated online exhibits of digitised items | Digital collections | Omeka Classic/S, Islandora, CONTENTdm-class |
| Long-term preservation | Preservation system | Archivematica, Preservica-class |
Small institutions often combine: Koha + Omeka; ArchivesSpace + an access front end.
Hosting: open-source systems are free to license but need hosting/support — many
libraries buy hosting from a support vendor. *Pricing and hosting options vary widely;
get quotes and references from similar-sized institutions.*

## 2. Configuring an ILS (Koha as the worked example)
Order matters — set the foundations before loading records:
1. **Libraries/branches**, **item types** (Book, DVD, Reference, Laptop),
   **collection codes**, **shelving locations** (authorised values).
2. **Patron categories** (Adult, Child, Staff, Student) with enrolment periods and age rules.
3. **Circulation and fines rules** — the matrix of patron category × item type × branch:
   loan period, renewals, holds allowed, fines/fees (many libraries are now fine-free —
   a policy decision first). Test edge cases: reference items not loanable, staff
   exceptions, closed days in the calendar (due dates skip holidays).
4. **MARC frameworks**: which fields show in the cataloguing editor; keep to what
   cataloguers use.
5. **Z39.50/SRU targets** for copy cataloguing (e.g. Library of Congress, national library).
6. **Notices** (overdue, hold available) — wording, channel (email/SMS), timing.
7. **OPAC**: facets, search weighting, display; accessibility check.
8. **Permissions**: staff roles with least privilege (circulation staff don't need
   system preferences).
Write each decision down; ILS configs become archaeology otherwise.

## 3. Archives and repositories in brief
- **ArchivesSpace:** accessions (what arrived) → resource records (the described
  collection, DACS-compliant) → archival objects (series/files) → digital objects;
  agents and subjects as linked records. Export EAD for finding aids or publish via its
  public interface.
- **DSpace:** communities › collections › items; configure submission forms and
  Dublin Core metadata, workflow review steps, licence agreement, and OAI-PMH for
  harvesting by aggregators.
- **Omeka:** items with Dublin Core, collections, exhibits; plugins/modules for IIIF,
  maps, CSV import. Good for showcase, not a preservation store.

## 4. Imports and migration
1. **Export everything** from the old system: bibs, items/holdings, patrons, open loans,
   holds, fines, acquisitions, authorities; digital files with checksums.
2. **Map** fields old → new in a spreadsheet; agree what's dropped.
3. **Clean** before migrating (OpenRefine, MarcEdit for MARC batch edits) — garbage moves too.
4. **Test loads** into a sandbox; compare counts (records, items, patrons, loans)
   and spot-check 50 random records end to end.
5. Plan cutover: freeze cataloguing, offline circulation mode, final delta load, go-live.
6. Patron data is personal data: minimise, secure transfer, delete old copies after go-live.

## Gotchas
- Loading records before item types/locations exist → thousands of items with blank codes.
- Circulation matrix with an unintended "default" rule letting everything circulate.
- Using a digital-collections tool as the only copy of master files.

## Verify
- [ ] Each job (circulation, archives, repository, exhibits, preservation) has a named system.
- [ ] Circulation rules tested on at least five patron × item edge cases.
- [ ] Post-migration counts match source within explained differences; 50-record spot check passed.
- [ ] Staff roles reviewed for least privilege.
- [ ] OAI-PMH/EAD exports (where used) validate and are harvested correctly.
