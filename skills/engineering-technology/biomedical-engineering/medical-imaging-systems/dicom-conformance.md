---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.dicom-conformance
name: dicom-conformance
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [dicom-conformance, imaging-qa, dicom, conformance-statement, sop-class, scu-scp, transfer-syntax, ihe, pacs]
level: practitioner
status: gated
description: "Write and read a DICOM conformance statement: SOP classes, SCU and SCP roles, transfer syntaxes, networking, security profiles and interoperability checks before integration."
sources: ["DICOM Standard PS3.2 Conformance and PS3.4 Service Class Specifications (current edition at https://www.dicomstandard.org)", "IHE Radiology technical framework (https://www.ihe.net)", "NEMA/MITA, DICOM Standard overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DICOM conformance statements

**Goal:** declare exactly which DICOM features a device supports so integrators can predict interoperability, and read other vendors' statements critically.

## What it must say (PS3.2 structure; the list below is unconfirmed (gated: unconfirmed, source is paywalled or blocked): the online PS3.2 Annex A template page is marked retired and points to a PS3.2 PDF edition)
1. **Implementation model:** application entities (AE), their titles and roles.
2. **Services:** each supported SOP class (for example CT Image Storage, MR Image Storage, Modality Worklist, Storage Commitment, MPPS) with role: **SCU** (client) or **SCP** (server).
3. **Transfer syntaxes:** Implicit VR Little Endian (the default every implementation must support, UID 1.2.840.10008.1.2, confirmed in DICOM PS3.5), Explicit VR Little Endian, JPEG, JPEG 2000 or other compressed forms; lossy compression must be explicit.
4. **Networking:** supported protocols, ports, TLS options, number of associations, timeouts, PDU sizes.
5. **Media:** DICOMDIR and file set profiles if used.
6. **Character sets** and extended negotiation.
7. **Security:** supported profiles (TLS, user identity), audit trail.
8. **Private attributes and creators** with their meaning; list unlisted extras.
9. **Configuration:** how AE titles, hosts and ports are set.

## How to use it
- Match each requirement of the site (worklist, storage, print, structured report) to an SOP class and role on both sides.
- Check transfer syntax overlap (a sender that only offers JPEG-LS to a receiver that only accepts uncompressed will fail).
- Verify attribute handling: patient ID, study UID uniqueness, pixel spacing and rescale slope/intercept.

## Test
- Use DICOM tools such as dcmtk's storescu, findscu and echoscu, or validators (dciodvfy) (gated: unconfirmed, source is paywalled or blocked) to test conformity before connecting to a production PACS.
- Verify de-identification behaviour per the PS3.15 profiles if sharing data.

## Gotchas
- A conformance statement is a claim; test it. Behaviour with unusual tags often differs.
- Multi-frame, enhanced and legacy objects differ; check which your viewers handle.

## Verify
- [ ] Association negotiation succeeds with the target PACS using the chosen syntaxes.
- [ ] Images round-trip with correct geometry and window levels.
- [ ] Private tags documented and not clashing.
