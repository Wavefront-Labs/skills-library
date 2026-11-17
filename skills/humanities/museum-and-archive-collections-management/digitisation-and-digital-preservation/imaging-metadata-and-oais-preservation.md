---
id: humanities.museum-and-archive-collections-management.digitisation-and-digital-preservation.imaging-metadata-and-oais-preservation
name: imaging-metadata-and-oais-preservation
category: humanities
field: museum-and-archive-collections-management
product: digitisation-and-digital-preservation
tags: [digitisation-and-digital-preservation, digitisation, digitization, digital-preservation, imaging, fadgi, metamorfoze, iso-19264, colour-target, colour-checker, tiff, master-file, access-copy, jpeg2000, ppi, fixity, checksum, md5, sha-256, bagit, premis, mets, dublin-core, oais, sip-aip-dip, ingest, born-digital, file-format-identification, droid, siegfried, 3-2-1-backup, iiif, archivematica, ndsa-levels]
level: practitioner
status: draft
description: "Digitise and keep collections: FADGI/Metamorfoze imaging targets, TIFF masters, fixity checksums, PREMIS metadata, OAIS-style ingest, 3-2-1 storage and IIIF access."
sources: ["FADGI Technical Guidelines for Digitizing Cultural Heritage Materials (2023)", "ISO 14721 (OAIS) reference model", "PREMIS Data Dictionary v3", "NDSA Levels of Digital Preservation v2.0", "IIIF Image and Presentation API specifications"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Imaging, metadata and OAIS-style preservation

**Goal:** digital surrogates good enough that you never need to rescan, and digital
files (scanned or born-digital) that remain findable, readable and provably unchanged.

## 1. Imaging to a measurable standard
- Pick a standard and star level: **FADGI** (US; 1–4 stars) or **Metamorfoze /
  ISO 19264-1** (EU). Aim for FADGI 3-star for most heritage work.
- Typical targets (confirm per material in the guideline): bound volumes and documents
  ~400 ppi at original size; photographs and small originals higher (600+ ppi);
  maps and art scaled to the long edge.
- Shoot a **colour/device target** (e.g. FADGI/ISO target or a colour checker) in each
  session and analyse it (tools such as OpenDICE or vendor software report delta-E,
  tone response, resolution). If the session fails the target, reshoot.
- Master files: uncompressed or losslessly compressed **TIFF** (or lossless JPEG 2000 if
  your policy allows), embedded colour profile (Adobe RGB 1998 or eciRGB v2; sRGB for
  access). Access copies: JPEG or derived via IIIF.
- Filenames from the object number, no spaces: `2026_014_001_r.tif` (r/v for recto/verso).

## 2. Metadata
- **Descriptive** comes from the catalogue record — link by object number, don't
  retype.
- **Technical** (embedded EXIF/XMP: device, settings, colour space) — extract with
  ExifTool or the ingest system.
- **Preservation** (**PREMIS**: events such as capture, validation, migration; agents;
  rights) and **structural** (METS or IIIF manifests: page order).

## 3. Fixity and ingest (OAIS in practice)
OAIS describes packages: **SIP** (what arrives), **AIP** (what you store), **DIP** (what
users get). A small-shop workflow:
1. Package files with checksums (BagIt via `bagit.py` or Bagger). SHA-256 preferred;
   MD5 is still common for fixity (not security).
2. Identify formats (**DROID** or **Siegfried**, against PRONOM IDs) and validate
   (JHOVE for TIFF/PDF).
3. Normalise risky formats to preservation formats where your policy says so (tools
   like **Archivematica** automate steps 1–3).
4. Store: at least **3 copies, 2 media/systems, 1 off-site/off-cloud-region** (3-2-1).
5. Schedule fixity checks (e.g. quarterly or yearly) and log results as PREMIS events.
Measure yourself with the **NDSA Levels of Digital Preservation** grid.

## 4. Born-digital material
Image carriers (floppies, CDs, hard drives) with a write blocker (FTK Imager, Guymager,
or BitCurator tools) before they fail; keep the disk image and a file-level copy;
scan for personal data before access.

## 5. Access
Serve images via **IIIF** (Image API for deep zoom; Presentation API manifests for
multi-page objects) so they work in Mirador/Universal Viewer and aggregators. Put
rights statements (RightsStatements.org or Creative Commons) on every item.

## Gotchas
- "Backed up to the shared drive" is not preservation: no fixity, one copy, no audit.
- JPEG masters can't be undone; compression artefacts accumulate on re-save.
- Don't let the vendor's scanner software auto-sharpen or auto-crop masters.
- Status: ppi values and fixity intervals are representative; check the guideline edition
  your funder requires.

## Verify
- [ ] Each session has a target analysis that passes the chosen star level.
- [ ] Masters are lossless with embedded profile and object-number filenames.
- [ ] Checksums were generated at capture and verified after every copy.
- [ ] Three copies exist across two systems, one off-site; fixity checks are logged.
- [ ] Access copies carry a rights statement and link back to the catalogue record.
