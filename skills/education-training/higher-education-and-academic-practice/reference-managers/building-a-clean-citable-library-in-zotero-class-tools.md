---
id: education-training.higher-education-and-academic-practice.reference-managers.building-a-clean-citable-library-in-zotero-class-tools
name: building-a-clean-citable-library-in-zotero-class-tools
category: education-training
field: higher-education-and-academic-practice
product: reference-managers
tags: [reference-managers, reference-management, citation-manager, zotero, bibliography, duplicates, doi, zotero-connector, unlink-citations]
level: practitioner
status: docs-checked
description: "Keep a Zotero library you can trust at submission time: capture with good metadata, add by identifier, merge duplicates, and unlink citations only in a copy."
sources:
  - https://www.zotero.org/support/adding_items_to_zotero
  - https://www.zotero.org/support/duplicate_detection
  - https://www.zotero.org/support/kb/unlinking_citations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a clean, citable library in Zotero

**Goal:** every reference you cite is complete and correct, and the bibliography can be regenerated rather than hand-edited. Examples use Zotero; other managers have equivalents, so check their own documentation.

## 1. Capture with good metadata

- Install the Zotero Connector for your browser alongside the desktop app. Zotero's documentation calls the Connector's save button the most convenient and reliable way to add items with high-quality bibliographic metadata.
- Save from the article's abstract page rather than the PDF when there is one; it usually gives better metadata.
- Add by identifier: Add Item by Identifier accepts ISBN, DOI, PubMed ID, arXiv ID or ADS Bibcode. Several can be entered at once, separated by spaces, commas or line breaks.
- When you save a PDF directly, Zotero tries to retrieve its information automatically. If that fails the PDF stays a standalone attachment; right-click it, choose Create Parent Item and enter a DOI or ISBN, or use Manual Entry. Check retrieved metadata before trusting it.

## 2. Clean as you go

For each new item check: item type, authors split correctly, title, journal, volume, issue, pages and DOI. Fixing the library item is better than hand-editing citations in a document.

- Duplicates: open the Duplicate Items collection (or right-click the library and choose Show Duplicates). Zotero advises always resolving duplicates by merging, never by deleting one. Select an item, click the Merge button in the right pane, and where fields differ choose a master item and the preferred version of each field.

## 3. Final submission

If a publisher wants plain text, use Unlink Citations in the word processor plugin, which leaves only flat text. Always unlink in a copy of the document and keep the original with live citations for reviewer changes or style switches. Treat unlinking as one-way.

## Verify

- [ ] Spot-check a sample of items for correct type, authors, journal and DOI.
- [ ] Duplicates merged, not deleted.
- [ ] An unlinked copy exists only as a copy; the live original is kept.

## Checked

2026-11-01. Confirmed against the Zotero support pages on adding items, duplicate detection and unlinking citations (sources above). Removed as not confirmed: EndNote and Mendeley equivalents, "Find Available PDF" and OpenURL setup, Better BibTeX and `.bib` export, CSL and style statements, group library storage figures, cloud-sync warnings, backup file names and the retraction flag (its support page returned 404).
Method: documentation only; no commands were run.
