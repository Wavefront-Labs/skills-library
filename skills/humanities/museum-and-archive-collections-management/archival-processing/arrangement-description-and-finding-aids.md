---
id: humanities.museum-and-archive-collections-management.archival-processing.arrangement-description-and-finding-aids
name: arrangement-description-and-finding-aids
category: humanities
field: museum-and-archive-collections-management
product: archival-processing
tags: [archival-processing, archives, archivist, appraisal, arrangement, description, finding-aid, respect-des-fonds, provenance, original-order, fonds, series, file, item, isad-g, dacs, ead, ead3, rad, mplp, more-product-less-process, processing-plan, collection-survey, box-list, scope-and-content, biographical-history, access-restrictions, archivesspace, atom, records]
level: practitioner
status: draft
description: "Process an archival collection: survey and appraisal, respect des fonds and original order, series arrangement, MPLP-level processing and a DACS/ISAD(G) finding aid encoded in EAD."
sources: ["ICA, ISAD(G) General International Standard Archival Description, 2nd ed.", "SAA, Describing Archives: A Content Standard (DACS)", "Greene & Meissner, 'More Product, Less Process', American Archivist 68 (2005)", "Library of Congress / SAA, EAD3 tag library"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Arrangement, description and finding aids

**Goal:** turn boxes of records into a collection researchers can find, understand and
request, at a processing depth you can actually afford.

## 1. Survey before you touch anything
- Walk through every box: extent (linear metres/feet, number of boxes, digital media),
  date range, formats, condition hazards (mould, rust, nitrate film, magnetic media),
  and **evident order**. Photograph box contents as found.
- Read the accession file: who created these records, who gave them, any restrictions
  or embargoes, copyright status.
- Write a one-page **processing plan**: target level (collection, series, folder), hours
  estimate, what will be weeded, preservation actions, access restrictions.

## 2. Principles of arrangement
- **Respect des fonds / provenance**: keep one creator's records together; never merge
  them with another collection by subject.
- **Original order**: if the creator's filing system survives, keep it — it is evidence
  of how they worked. Only impose order where none exists or it's unusable.
- Build the hierarchy: **fonds/collection → series → (subseries) → file/folder → item.**
  Series reflect functions or activities (Correspondence, Financial records, Project
  files), not formats where avoidable.

## 3. Appraise and weed (within the deed's terms)
Remove true duplicates, blank forms, publications held elsewhere, and records the
agreement allows you to destroy or return. Document what was removed and how much.
Personal data (medical, student, HR records) is flagged for restriction, not discarded
on a whim — check data-protection law for your jurisdiction.

## 4. Process to the right level (MPLP)
Greene and Meissner's "More Product, Less Process" argues for minimal processing:
describe at series/folder level, don't remove every staple, don't refolder everything,
get it open. Go deeper only where use or risk justifies it (high-demand series,
fragile media, sensitive data). Rehouse into acid-free folders/boxes where needed;
label every folder with collection number, box and folder number, title and dates.

## 5. Describe to a standard
Use **DACS** (US) or **ISAD(G)** (international; RAD in Canada). The core elements:
reference code, title, dates (inclusive and bulk), level of description, extent, creator,
**biographical/administrative history**, **scope and content**, arrangement, conditions
of access and reproduction, language, finding aids, related materials.
- Scope and content says what is *in* the boxes, including gaps ("no records before
  1962", "photographs largely undated").
- Titles: devised titles follow the standard's formula (DACS: name + form/topic).
- Then a container list: box/folder, title, dates.

## 6. Encode and publish
Enter in your archival management system (ArchivesSpace, AtoM, Axiell — see
collection-management-systems skill) which exports **EAD** (EAD3 or EAD 2002 — confirm
which your aggregator ingests). Validate the XML against the schema before submitting
to a union catalogue.

## Gotchas
- "Miscellaneous" series grow into dumping grounds. Cap it or describe it.
- Bulk dates matter: 1890–1995 (bulk 1960–1975) changes a researcher's decision.
- Born-digital media in boxes need imaging before the carrier dies; flag for digital
  preservation, don't just list "3 floppy disks".
- Status: element names follow DACS/ISAD(G) as summarised; check the current DACS
  revision your repository uses.

## Verify
- [ ] Processing plan with level and hours exists and was roughly met.
- [ ] Provenance kept; original order kept or departures documented.
- [ ] Weeded material is recorded with quantity and authority.
- [ ] Finding aid has all required elements plus a container list.
- [ ] Box/folder labels match the container list; EAD validates.
- [ ] Restrictions are stated in the finding aid and flagged on the boxes.
