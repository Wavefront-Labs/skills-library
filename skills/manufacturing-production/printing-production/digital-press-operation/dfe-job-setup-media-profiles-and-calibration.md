---
id: manufacturing-production.printing-production.digital-press-operation.dfe-job-setup-media-profiles-and-calibration
name: dfe-job-setup-media-profiles-and-calibration
category: manufacturing-production
field: printing-production
product: digital-press-operation
tags: [digital-press-operation, digital-printing, production-digital-press, toner-press, inkjet-press, hp-indigo, xerox, canon-imagepress, konica-minolta-accuriopress, ricoh-pro, dfe, digital-front-end, fiery, efi-fiery, rip, command-workstation, hot-folder, virtual-printer, imposition, media-catalog, paper-catalog, media-profile, calibration, linearisation, icc-profile, colour-drift, front-to-back-registration, variable-data-printing, vdp, pdf-vt, duplex]
level: practitioner
status: draft
description: "Set up production digital press jobs at the DFE: media catalogue entries, calibration and profiling routines, imposition and duplex registration, and variable-data jobs that print right first time."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital press: DFE job setup, media profiles and calibration

**Goal:** get consistent, correctly imposed output from a production toner or inkjet
press by controlling the three things that matter — the media definition, the
calibration state, and the job settings at the digital front end (DFE).

*Draft note:* terminology follows common DFEs (EFI Fiery Command WorkStation, and
vendor DFEs for HP Indigo, Xerox, Canon, Konica Minolta, Ricoh). Exact menus differ;
the logic is shared.

## 1. Media catalogue: define every stock properly
Each stock gets an entry with: name (as the floor knows it), size, **weight (gsm)**,
**coating** (uncoated, gloss, silk/matte coated), and type (plain, tabs, envelope,
synthetic). The press uses weight and coating to set **fuser temperature, transfer
voltage, paper path speed and airflow** (toner) or drying/ink limits (inkjet).
- Wrong weight → poor toner fusing (rubs off, cracks on fold) or blistering/curl.
- Wrong coating → mottle, poor transfer, or toner offset.
- Link each media entry to the **right output (ICC) profile and calibration set**.
Make a new entry for a new stock rather than "borrowing" a close one.

## 2. Calibration vs profiling
- **Calibration (linearisation)** brings the press back to a known reference state:
  print a target, measure with the inline or handheld spectrophotometer, the DFE
  updates curves. Do it **at the start of each shift**, after consumable changes
  (drum, developer, blanket, imaging oil), after big temperature/humidity changes,
  and whenever QC patches drift.
- **Profiling** characterises a calibrated press + media combination into an ICC
  output profile. Do it once per stock family (and again if results drift after
  calibration). Never profile an uncalibrated press.
- Use the DFE's verification step (print a control strip, compare to reference e.g.
  ISO 12647-8 / G7 targets); keep the report as evidence.

## 3. Job setup at the DFE
1. **Hot folder or virtual printer** with presets for repeat work — fewer manual
   mistakes than setting every job by hand.
2. **Check incoming PDF**: preflighted? fonts embedded? bleed present (typically 3 mm)?
   Spot colours named correctly (spot matching tables used for brand colours)?
3. **Imposition:** N-up, booklet (saddle-stitch with creep compensation),
   cut-and-stack for numbered jobs. Add crop marks and colour bar off the trim area.
4. **Colour settings:** source profiles (RGB/CMYK), rendering intent, black
   overprint and spot handling — usually from a preset; change only deliberately.
5. **Duplex:** set front-to-back registration adjustments for the stock; check with a
   registration target or by holding a sheet to the light. Paper grain and curl
   affect it.
6. **Proof one** (or one set), check against the job ticket and any signed proof,
   then release the quantity.

## 4. Variable data printing (VDP)
- Prefer optimised formats (**PDF/VT**, or vendor VDP formats) so repeated elements
  are cached; plain PDFs with thousands of unique pages can choke the RIP.
- Verify the **data file** before printing: record count, blank fields, special
  characters (accents, ampersands), field overflow on long names.
- Print and check **first, last and a few edge-case records** (longest name, missing
  line 2 of an address).
- For mailings and numbered work, define **cut-and-stack** order so sequence
  survives finishing; keep a reconciliation count (printed vs good vs spoiled).

## 5. Gotchas
- Humidity: paper stored outside the pressroom causes jams, curl and duplex misregister;
  condition stock in the room for a day where possible.
- Rich black from Office files: 4-colour text at small size misregisters; force 100% K
  for text if your workflow allows.
- Clearing a jam mid-VDP job: confirm restart record number so you don't skip or
  duplicate personalised pieces.

## Verify
- [ ] Stock has its own media entry with correct weight/coating linked to a profile.
- [ ] Press calibrated this shift; verification strip within tolerance and saved.
- [ ] Imposition, bleed and marks checked on the first proof.
- [ ] Duplex registration confirmed on the actual stock.
- [ ] VDP data checked; first/last/edge records proofed; counts reconciled.
