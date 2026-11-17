---
id: law-government.civil-litigation.e-discovery-platforms.review-workflow-search-tar-and-productions
name: review-workflow-search-tar-and-productions
category: law-government
field: civil-litigation
product: e-discovery-platforms
tags: [e-discovery-platforms, civil-litigation, e-discovery, ediscovery, ediscovery-platform, relativity, relativityone, everlaw, disco, reveal, nuix, logikcull, processing, deduplication, email-threading, near-duplicate, search-terms, search-term-report, hit-report, tar, technology-assisted-review, active-learning, continuous-active-learning, elusion-test, recall, precision, coding-layout, review-batches, privilege-review, qc, redaction, production, load-file, dat-file, opt-file, bates-numbering, native-production, edrm]
level: practitioner
status: docs-checked
description: "Running document review on e-discovery platforms such as Relativity: processing, search term validation, TAR/active learning workflows, coding layouts, QC and production formats."
sources: ["https://www.law.cornell.edu/rules/frcp/rule_26", "https://www.law.cornell.edu/rules/fre/rule_502", "https://edrm.net/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# E-discovery platforms: review workflow, TAR and productions

**Goal:** get from collected data to a defensible, on-time production while controlling
review cost. Steps follow the EDRM model and use **Relativity** terminology (platform names differ:
Relativity, Everlaw, DISCO and Reveal).
Menu locations change between versions — check your platform's current documentation.

## 1. Processing
- Ingest collections with **chain of custody** recorded (custodian, source, collection
  method, hash values).
- Set processing options deliberately: **time zone** for date normalisation (agree it
  with opposing counsel), de-NISTing (remove known system files),
  container extraction, OCR for image-only documents.
- **Deduplication:** global (across custodians) vs custodial. Global saves the most
  review; track all custodians in a field (e.g. "All Custodians") so you can still
  produce custodian metadata.
- **Email threading** and **near-duplicate** identification reduce review — review only
  inclusive emails where agreed.

## 2. Search terms
- Draft with the case team, then **test**: run a search term report
  showing hits per term, unique hits, and hits with family.
- Sample hits for each term to estimate precision; refine terms that over-hit
  (e.g. a term that is also a common email signature word).
- Negotiate with opposing counsel using hit counts — data beats argument.
- Syntax differs across platforms; proximity and wildcard
  operators don't translate automatically. Test exact syntax before agreeing a list.

## 3. TAR / active learning
- **Continuous active learning (CAL)** — the model prioritises likely-relevant documents
  for reviewers and keeps learning.
- Defensibility: agree or disclose the protocol, then **validate** — an **elusion test**
  (random sample of the unreviewed, predicted-not-relevant set) to estimate recall.
  There is no universal recall standard; confirm any target with opposing counsel or the court.
- Keep a record: settings, training rounds, validation sample sizes and results.

## 4. Review setup
- **Coding layout:** responsiveness, issue tags, privilege (with basis), confidentiality
  designation (per protective order), redaction needed, hot document.
- Batch by family to keep attachments with parents; set propagation rules for family
  coding.
- Reviewer protocol document: definitions with examples, escalation route for
  questions. Hold a kickoff and update the protocol as decisions are made.
- **QC:** second-level review of samples per reviewer, all privilege calls, and all
  hot documents; targeted searches for inconsistencies (responsive parent with
  non-responsive child).

## 5. Privilege and redaction
Search for attorney names and domains to flag potential privilege. Redact using the
platform's redaction tools (never by drawing boxes on native files). Generate the
privilege log from coded fields and QC it.

## 6. Production
Follow the ESI protocol: typically TIFF/PDF images with extracted text and a load file
(**.DAT** metadata, **.OPT** image cross-reference), natives for spreadsheets and media,
**Bates numbering** with prefix, confidentiality endorsements burned on images. Run a
production QC: count reconciliation, privilege screen (no privileged-coded doc in the
set), redactions burned in, metadata fields correct. Keep a production log.

## Gotchas
- Wrong processing time zone corrupts date searches and chronology.
- Producing native files with hidden content (track changes, comments, hidden sheets).
- Redactions applied but not burned into images.

## Verify
- [ ] Processing settings and time zone documented and agreed.
- [ ] Search terms tested with hit reports and sampling.
- [ ] TAR validated with an elusion test and recorded.
- [ ] Production QC checklist completed and production log updated.

## Checked

- Date checked: 2026-10-25. Jurisdiction: Platform-neutral practice for United States federal civil litigation (FRCP 26, FRE 502).
- Confirmed against official sources (see `sources`): Nothing in this skill is a statutory or numeric rule; the remaining workflow steps (processing, search-term testing, TAR validation, coding layout, load-file production) are generic craft that the skill already tells the reader to check against their own platform documentation.
- Corrected or removed: Removed vendor-specific feature claims (Relativity STR and Active Learning project type, dtSearch versus Lucene syntax), the "UTC is common" practice claim and the 70-80% recall figure, none of which could be confirmed on a free official source.

Method: documentation only; no commands were run.
