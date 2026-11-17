---
id: transportation-logistics.trade-compliance-customs-brokerage.bonded-transit-procedures.bonded-warehouse-transit-and-drawback-control
name: bonded-warehouse-transit-and-drawback-control
category: transportation-logistics
field: trade-compliance-customs-brokerage
product: bonded-transit-procedures
tags: [bonded-warehouse, customs-warehousing, special-procedures, ncts, common-transit, t1, t2, tir, in-bond, cbp-7512, ftz, foreign-trade-zone, duty-drawback, inward-processing, ipr, outward-processing, temporary-admission, ata-carnet, guarantee, stock-records, discharge, duty-suspension]
level: advanced
status: gated
description: "Keeping duty-suspended goods under control: bonded-warehouse stock records, transit movements (NCTS, US in-bond), guarantees and discharge, and drawback/inward-processing claims."
sources: ["https://www.ecfr.gov/current/title-19/part-18", "https://www.ecfr.gov/current/title-19/part-191", "https://www.ecfr.gov/current/title-19/part-146", "https://taxation-customs.ec.europa.eu/customs/customs-procedures_en"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bonded warehouse, transit and drawback control

**Goal:** move and hold goods without paying duty yet — and prove, at any moment, where
every unit is. Duty suspension is a privilege backed by a guarantee; losing track of
goods turns into a full duty debt plus penalties.

## 1. Bonded/customs warehousing
- Authorisation (EU/UK customs warehouse; US bonded warehouse class or a Foreign-Trade
  Zone) with a **guarantee** covering potential duty.
- **Stock records** are the core obligation. Each line needs: entry reference, date
  in, description, tariff code, quantity and unit, origin, customs value, location,
  status (suspended/released/re-exported), and the discharge reference when it leaves.
- Permitted handling ("usual forms of handling": repacking, labelling, sorting) only;
  anything more needs inward processing authorisation.
- Reconcile records to physical stock on a fixed cycle (cycle counts monthly, full
  count at least annually or as authorised). Investigate and report losses promptly;
  unexplained shortages incur duty.
- Discharge by: release for free circulation (declaration + duty), re-export, transfer
  to another special procedure, or destruction under supervision.

## 2. Transit movements
- **EU/UK common/Union transit (NCTS) (gated: unconfirmed, source is paywalled or blocked) EU and HMRC pages were not read:** T1 (non-Union goods) declaration lodged at
  office of departure, guarantee attached, seals applied, **time limit** for arrival
  set. At destination, arrival notification closes the movement. Unclosed movements
  generate enquiries and duty claims against the principal.
- **TIR (gated: unconfirmed, source is paywalled or blocked) Convention text not read:** carnet-based transit across multiple countries with sealed load
  compartments.
- **US in-bond (CBP 7512 data, filed electronically):** IT (immediate transportation),
  T&E (transportation and exportation), IE (immediate exportation). Goods must arrive
  at destination port within 30 days (19 CFR 18.1(i)(1); 60 days if any part of the movement is by barge) and the arrival
  must be reported promptly; bond liability attaches otherwise.
Habits: check seal numbers at departure and arrival; record vehicle/container IDs;
chase any movement not closed within its time limit before customs does.

## 3. Duty relief on processing and exports
- **Inward processing (EU/UK IP):** import non-EU/UK goods duty-suspended, process,
  re-export. Keep a **bill of discharge** linking imports to processed products
  (rate of yield). Discharge within the authorised period.
- **US duty drawback** (refund of generally 99 % of eligible duties when goods are exported or
  destroyed): manufacturing drawback (direct identification or substitution),
  unused merchandise drawback, rejected merchandise. The goods must be exported or destroyed within 3 years of
  importation (19 CFR 191.31(b) for direct identification) and a completed claim must be filed within
  3 years after exportation or destruction (19 CFR 191.51(e)); requires linking import entries to
  export proof.
- **Temporary admission / ATA carnet:** exhibitions, professional equipment, samples
  — goods must leave within the time allowed, in the same state.

## Gotchas
- Guarantee level must cover the peak, not average, duty exposure.
- Mixing duty-paid and duty-suspended stock in the same location without system
  status flags — the commonest audit failure.
- A transit not closed because the destination never sent the arrival message: you
  are still the principal; get alternative proof (destination office stamp,
  subsequent declaration) quickly.
- *Time limits and periods vary by authorisation and jurisdiction; confirm yours.*

## Verify
- [ ] Every stock-record line traces from entry document to discharge document.
- [ ] Book stock = physical stock at last count, with variances explained.
- [ ] No open transit or in-bond movement past its time limit.
- [ ] Guarantee/bond covers current peak exposure.
- [ ] Drawback/IP claims link import entries to export or processing evidence.

## Checked

Jurisdiction: United States (CBP, 19 CFR) with EU/UK notes. Checked 2026-10-25 against current eCFR: 19 CFR 18.1(i)(1) (in-bond 30 days, barge 60), 191.51(b)(1) (drawback generally 99 percent) and (e)(1) (claim within 3 years after exportation or destruction), 191.31(b) (3 years from importation to export or destroy). Corrected: the draft said claims within 5 years of import. EU UCC, HMRC and TIR statements were not confirmed and are marked gated.

Method: documentation only; no commands were run.
