---
id: media-communication.library-and-archive-science.digital-preservation.fixity-format-migration-and-oais-workflow
name: fixity-format-migration-and-oais-workflow
category: media-communication
field: library-and-archive-science
product: digital-preservation
tags: [digital-preservation, oais, sip, aip, dip, fixity, checksums, sha-256, bagit, rfc-8493, ndsa-levels, premis, format-migration, digital-archives]
level: practitioner
status: docs-checked
description: "Keep digital materials trustworthy: OAIS packages, BagIt (RFC 8493) manifests for fixity, NDSA Levels for self-assessment, and PREMIS for event records."
sources: ["https://datatracker.ietf.org/doc/html/rfc8493", "https://ndsa.org/publications/levels-of-digital-preservation/", "https://www.loc.gov/standards/premis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixity, format migration and an OAIS-style workflow

**Goal:** files you hold today can be trusted as unaltered and opened decades from now,
with a workflow proportionate to your resources.

## 1. OAIS vocabulary (general practice, not on the pages read)
SIP is what the producer submits, AIP is what you keep, DIP is what users receive.
Document each step even if you have no large system.

## 2. Package with BagIt (RFC 8493)
A bag is a base directory containing:
- `bagit.txt`: the bag declaration, exactly two lines, UTF-8, no byte order mark;
- `data/`: the payload directory (required);
- at least one payload manifest, `manifest-<algorithm>.txt` (for example
  `manifest-sha256.txt`, `manifest-sha512.txt`), which must list every payload file;
- optionally tag files such as `bag-info.txt` (metadata) and tag manifests
  `tagmanifest-<algorithm>.txt`. Tag manifests should use the same algorithms as the
  payload manifests.
A *complete* bag has every required element; a *valid* bag is complete and every
checksum in every manifest verifies. Since BagIt 1.0, creation and validation tools MUST
support SHA-256 and SHA-512; the RFC says to support MD5 and SHA-1 for backward
compatibility, and its examples note SHA-512 as the recommended algorithm.
Validation means recomputing the checksums and comparing them to the manifests.

## 3. Assess maturity with the NDSA Levels
The Levels of Digital Preservation help practitioners build or assess a preservation
programme. Version 2.0 was released in 2019 and version 2.1 in March 2026 (focus:
environmental sustainability). Resources on the NDSA page include the matrix, FAQ,
implementation guidelines and working definitions, an assessment tool (spreadsheet) and
a digital curation decision guide, all hosted in an OSF repository. Read the matrix
itself there for the level criteria.

## 4. Record events with PREMIS
The PREMIS Data Dictionary for Preservation Metadata is the international standard
for metadata supporting the preservation of digital objects. It consists of the Data
Dictionary, an XML schema and supporting documentation; version 3.0 is the current
version. Library of Congress also publishes a Preservation Events Controlled Vocabulary.

## Verify
- [ ] Each accession packaged as a valid bag and checksum algorithm recorded.
- [ ] Validation repeated after every copy or move; results logged.
- [ ] Preservation events recorded in a consistent schema (for example PREMIS).
- [ ] Current NDSA Levels assessed and next improvement chosen.

## Checked
2026-11-09. Confirmed against RFC 8493 (bag structure, manifests, complete/valid,
algorithm support), the NDSA Levels page (versions and resources; the matrix itself is
on OSF and was not read) and the PREMIS home page (what it is, v3.0 current). Removed
because not on pages read: tool commands (bagit.py, Siegfried, DROID, JHOVE, veraPDF),
fixity schedules, MD5 adequacy claims, 3-2-1 backup rule, preferred preservation format
list, normalisation and migration rules, web archiving, Archivematica. PRONOM source
dropped (landing stub).
Method: documentation only; no commands were run.
