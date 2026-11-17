---
id: manufacturing-production.pharmaceutical-manufacturing.serialisation-packaging-pharma.blister-line-label-control-and-serialisation
name: blister-line-label-control-and-serialisation
category: manufacturing-production
field: pharmaceutical-manufacturing
product: serialisation-packaging-pharma
tags: [serialisation-packaging-pharma, pharmaceutical-packaging, secondary-packaging, blister-line, thermoforming, cold-form, alu-alu, pvc-pvdc, sealing-temperature, leak-test, blue-dye-test, bottle-line, induction-seal, label-control, label-reconciliation, printed-components, line-clearance, serialisation, serialization, track-and-trace, datamatrix, gs1, gtin, sscc, aggregation, eu-fmd, falsified-medicines-directive, emvs, dscsa, tamper-evidence, anti-tampering, vision-system, ocr, ocv, pharmaceutical-manufacturing]
level: practitioner
status: gated
description: "Pack medicines under GMP: blister forming and seal checks, printed-component control and reconciliation, line clearance, serialisation codes, aggregation, and tamper-evident closures."
sources:
  - "https://www.fda.gov/drugs/drug-supply-chain-integrity/drug-supply-chain-security-act-dscsa"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blister line, label control and serialisation

**Goal:** every pack contains the right product, sealed, with the right printed
information and a unique serial number that the verification system will accept. In
packaging, the classic disasters are **mix-ups** (wrong leaflet, wrong strength label)
— which is why printed-component control is as strict as dispensing.

## 1. Line clearance (every batch, every change)
- Remove **all** materials, packs, labels, leaflets, rejects and documents from the
  previous run, including from reject bins, under the conveyor and in vision-system
  reject trays.
- Clear the serialisation system of previous batch data (the order must be closed).
- Second person verifies against the checklist and signs. One stray carton from the
  last batch is a recall risk.

## 2. Blister forming and sealing
- **Thermoform** (PVC, PVC/PVDC, PVC/Aclar) or **cold form** (alu/alu, for moisture-sensitive product).
- Set forming temperature, sealing temperature, sealing pressure and dwell per the batch
  record; check the sealing tool's knurl pattern is even.
- **Checks:** empty/broken pocket detection (camera), seal integrity — vacuum leak test
  (blue dye or methylene blue test is common) at the specified frequency; batch/expiry
  embossing legible.
- Defects: poor seal (temperature too low, worn tool, foil wrinkle), pinholes in cold
  form (forming depth too aggressive), product fragments in the seal area.

## 3. Printed-component control
- Labels, cartons, leaflets and foil are issued in **counted quantities** from a
  controlled store; check item code, version and quantity on receipt at the line.
- Variable data (batch, expiry, serial) printed online is verified by **vision system**
  (OCR/OCV, barcode grading). Challenge it at start-up and per frequency with
  deliberately wrong samples; it must reject them.
- **Reconciliation** at the end: issued = used + destroyed + returned (± a defined
  tolerance for roll labels; usually zero tolerance for coded items). A discrepancy
  outside limits is a deviation and the batch is held.
- Destroy surplus printed batch-specific material under witness; return generic material to stores.

## 4. Serialisation
- Each saleable pack carries a **2D DataMatrix** (GS1) with GTIN/product code, serial
  number, batch, expiry (and national code where required) plus human-readable text.
- Serial numbers are allocated from the site/enterprise system down to the line.
- **EU FMD**: packs are uploaded to the EU hub/EMVS and verified/decommissioned at the
  pharmacy; also requires an **anti-tampering device** (glue spot, tamper-evident label/carton) (gated: unconfirmed, source is paywalled or blocked). EUR-Lex is blocked to the review tool.
- **US DSCSA**: package-level electronic tracing of drugs (FDA); the implementation and enforcement dates have been phased and
  extended, so check the current FDA DSCSA implementation page for dates.
- **Aggregation** (pack → case → pallet, SSCC labels) is required in some markets and
  used by many companies regardless.
- **Rejects and samples:** every serial must end with a status — commissioned, sampled,
  destroyed or decommissioned. QC samples taken from the line must be recorded in the
  system or the numbers won't reconcile with what's uploaded.

## Gotchas
- Re-feeding a rejected carton by hand back into the line after the camera: it now carries a serial that may have been marked rejected.
- Leaflet folders picking two leaflets at once (check weight of finished pack if checkweigher fitted).
- Changing a code template version on the printer without change control.
- Batch closure before all rejects are scanned → serial reconciliation fails at upload.
- Tamper-evident seal applied crooked so it doesn't break when opened.

## Verify
- [ ] Line clearance signed by two people, including serialisation system cleared.
- [ ] Seal/leak tests passed at every required interval.
- [ ] Vision system challenged at start and per frequency; challenges recorded.
- [ ] Printed-component and serial reconciliation balance within limits.
- [ ] Batch data uploaded/closed successfully; aggregation hierarchy complete if used.

## Checked

Date: 2026-10-25. Jurisdictions: United States (DSCSA) and European Union (Falsified Medicines Directive).

Confirmed: FDA DSCSA page describes package-level electronic tracing of drugs; the page gave no dates, so the skill no longer states any. Not confirmed (marked gated above): EU FMD upload, verification and anti-tampering details. Removed: serialisation vendor names. Line clearance, blister forming and printed-component control are site procedure and were not tied to a primary source.

Method: documentation only; no commands were run.
