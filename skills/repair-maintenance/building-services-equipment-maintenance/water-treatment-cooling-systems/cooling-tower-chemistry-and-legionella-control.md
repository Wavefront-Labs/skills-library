---
id: repair-maintenance.building-services-equipment-maintenance.water-treatment-cooling-systems.cooling-tower-chemistry-and-legionella-control
name: cooling-tower-chemistry-and-legionella-control
category: repair-maintenance
field: building-services-equipment-maintenance
product: water-treatment-cooling-systems
tags: [building-services-equipment-maintenance, water-treatment-cooling-systems, water-treatment, cooling-tower, evaporative-condenser, legionella, legionella-sampling, dip-slide, tvc, biocide, oxidising-biocide, chlorine, bromine, non-oxidising-biocide, scale-inhibitor, corrosion-inhibitor, cycles-of-concentration, conductivity, bleed-off, blowdown, closed-loop, nitrite, molybdate, l8, hsg274-part-1, ashrae-188, tower-cleaning, disinfection, drift-eliminators]
level: practitioner
status: gated
description: "Cooling tower and closed-loop water treatment: conductivity and cycles, biocide dosing, dip-slide and legionella sampling with action levels, inhibitor tests, clean and disinfect."
sources: ["https://www.hse.gov.uk/pubns/books/hsg274.htm", "https://www.hse.gov.uk/legionnaires/cooling-towers.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cooling tower chemistry and legionella control

**Goal:** keep towers and closed loops free of scale, corrosion and bacteria — above all
**Legionella**, which grows in warm tower water and spreads in drift to kill people.
Cooling towers are legally controlled: in the UK, notifiable to the local authority (gated: unconfirmed, source is paywalled or blocked)
and managed under ACoP L8 / HSG274 Part 1 with a responsible person and written scheme;
in the US, ASHRAE 188 water management plans and local codes (e.g. New York City's
tower rules). The treatment company's specification and the site risk assessment
override typical numbers here.

## 1. Cooling tower: routine (weekly)
- **Visual:** water clarity, slime/algae on fill and pond, drift eliminators intact and
  seated, no aerosol plume carry-over, sludge in the pond.
- **Conductivity** of tower water and make-up water → **cycles of concentration** =
  tower conductivity ÷ make-up conductivity. Target per treatment spec.
  Too high → scale; too low → wasted water and chemical. Bleed-off (blowdown) controller
  set to hold the conductivity setpoint — check it actually opens.
- **Biocide residual:** oxidising (chlorine/bromine) held at the free halogen
  residual the treatment specification gives, with a DPD test kit; non-oxidising biocides
  dosed as slugs on a schedule, often alternating two types.
- **pH** (halogen biocide efficacy depends on pH; HSG274 Part 1 (2024) covers pH correction of free-halogen results).
- **Inhibitor level** (scale/corrosion) tested against the spec.
- **Dosing equipment:** tanks have product, pumps actually dose (drawdown test), injection
  points not blocked. Record everything in the log book.

## 2. Microbiology
- **Dip slides / TVC (total viable count):** at least weekly in many regimes. Confirm
  the TVC action levels in the current HSG274 Part 1.
- **Legionella sampling:** quarterly in the UK guidance (gated: unconfirmed, source is paywalled or blocked;
  more often on new or problem systems), UKAS-accredited lab. Confirm the action levels
  in cfu/l in the current HSG274 Part 1. US plans set their own triggers; check the units.
- Sample from the return to the tower or the pond per procedure, before biocide dosing,
  in sterile bottles with neutraliser; chilled to the lab within 24 hours.

## 3. Cleaning and disinfection (at least six-monthly in UK guidance; gated: unconfirmed, source is paywalled or blocked)
1. Pre-clean disinfection: raise free chlorine with dispersant to the concentration and
   contact time in HSG274 Part 1 or your scheme, maintaining the residual.
2. Drain, clean pond, fill, eliminators and casing with low-pressure water (high-pressure
   jets make aerosols — wear **RPE** of the grade your risk assessment specifies and protective clothing).
3. Refill, disinfect again, flush, return to normal treatment. Record.

## 4. Closed loops (chilled and heating water)
- Test quarterly: inhibitor (e.g. nitrite, molybdate) at the specified range, pH,
  conductivity, iron/copper, TVC and **sulphate-reducing bacteria** for corrosion risk.
- Add inhibitor by pot feeder after any top-up; frequent make-up = a leak, find it.
- Side-stream filters changed when dP rises.

## Gotchas
- Systems standing idle become high risk — stagnant warm water. Recommission with
  disinfection before restart.
- A biocide reading taken right after dosing looks great and means nothing; test at a
  consistent point in the cycle.
- Don't mix oxidising biocide concentrates with acids or other chemicals; segregate storage.

## Verify
- [ ] Tower registered/notified where required; written scheme and responsible person named.
- [ ] Weekly log: conductivity, cycles, biocide residual, pH, inhibitor, dosing checks.
- [ ] Dip slides and Legionella results logged with actions against action levels.
- [ ] Clean and disinfection done in schedule with records.
- [ ] Closed-loop inhibitor in range; make-up volume trended.

## Checked

Date checked: 2026-10-25. Jurisdiction: United Kingdom (ACoP L8, HSG274 Part 1 second edition March 2024); US codes mentioned only by name.
HSE pages: cooling towers and evaporative condensers are covered by L8 and HSG274 Part 1; the March 2024 second edition of Part 1 added DPD No 1 testing and pH correction of free-halogen results. The HSG274 Part 1 PDF returned unreadable binary here, so the quarterly sampling interval, six-monthly cleaning interval and local-authority notification are marked gated and the action levels, chlorine dosing and cycles figures were replaced by a deferral to HSG274 Part 1. Removed the US trigger figure because units differ (cfu/l versus cfu/ml).

Method: documentation only; no commands were run.
