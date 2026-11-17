---
id: health-medicine.public-health.immunization-programmes.programme-planning-cold-chain-and-coverage-monitoring
name: programme-planning-cold-chain-and-coverage-monitoring
category: health-medicine
field: public-health
product: immunization-programmes
tags: [public-health, immunization-programmes, immunisation, vaccination-programme, epi, expanded-programme-on-immunization, ia2030, microplanning, vaccine-forecasting, wastage-rate, cold-chain, 2-8c, vaccine-vial-monitor, vvm, freeze-sensitive-vaccines, shake-test, temperature-logger, cold-chain-breach, coverage-monitoring, dtp1-dtp3-dropout, zero-dose-children, administrative-coverage, coverage-survey, herd-immunity-threshold, catch-up-campaign, outbreak-response-immunisation, aefi, vaccine-hesitancy, measles]
level: practitioner
status: gated
description: "Running population immunisation: microplanning and vaccine forecasting, cold-chain management and breach response, coverage and dropout monitoring, catch-up and outbreak-response campaigns, AEFI."
sources: ["https://www.cdc.gov/vaccines/hcp/storage-handling/index.html", "https://www.who.int/news-room/fact-sheets/detail/measles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programme planning, cold chain and coverage monitoring

> General professional reference. Schedules, eligibility, dosing and storage
> specifics are vaccine- and country-specific: use the current national immunisation
> handbook (e.g. Green Book, CDC Pink Book/ACIP, national EPI manual) and product
> information.

**Goal:** get potent vaccine into every eligible person on time, find the ones being
missed, and respond fast when immunity gaps show up as outbreaks.

## 1. Planning (microplanning)
- **Target population** per area by birth cohort/age band (registers, census
  projections — check denominators, often the biggest error source).
- Map sessions: fixed, outreach, mobile; travel times; hard-to-reach groups (migrants,
  travellers, urban slums, conflict zones).
- **Forecast vaccine** = target population × doses in schedule × expected coverage ×
  **wastage factor** (1/(1 − wastage rate)) + buffer stock − stock on hand. Multi-dose
  vials have higher wastage; apply the open-vial policy where allowed.
- Supplies: syringes (auto-disable), safety boxes, diluents (matched to vaccine and
  stored per guidance), recording tools.

## 2. Cold chain
- Most vaccines are stored refrigerated at **+2 to +8 °C** (gated: unconfirmed, source is paywalled or blocked); some are frozen — product-specific, so follow the package insert. CDC: do not use vaccines stored outside recommended temperatures unless the manufacturer or public health authorities confirm safety and effectiveness.
- **Freezing destroys** many vaccines (aluminium-adjuvanted: DTP-containing, HepB,
  HPV, PCV). Use the **shake test** (per WHO procedure) when freezing is suspected (gated: unconfirmed, source is paywalled or blocked).
- **Vaccine vial monitors (VVM)**: heat exposure indicator; don't use past discard
  point (gated: unconfirmed, source is paywalled or blocked).
- Equipment: purpose-built vaccine refrigerators, continuous **digital data loggers**
  with min/max and at least one backup logger (CDC), read at the frequency your local standard sets; no food; not in
  door shelves; stock rotation (FEFO — first expiry, first out).
- **Breach response**: quarantine stock (label "do not use"), don't discard, record
  min/max and duration, contact manufacturer/immunisation team for advice; identify
  and recall anyone vaccinated with compromised vaccine if advised.

## 3. Coverage monitoring
- **Administrative coverage** = doses given / target population (can exceed 100% with
  bad denominators). Validate with **coverage surveys** (WHO cluster survey methods)
  or register-based data.
- **Dropout rate** (DTP1→DTP3) = (DTP1 − DTP3)/DTP1; a high rate suggests access or
  quality problems after first contact. **DTP1 coverage** low = access problem;
  **zero-dose children** are the IA2030 priority.
- Analyse by area and subgroup; RED/REC categorises districts by access and
  utilisation.
- Timeliness matters, not just completion (measles susceptibility in late-vaccinated
  infants).

## 4. Immunity thresholds and catch-up
- Herd immunity threshold ≈ 1 − 1/R0 (measles R0 ~12–18 → ~95% two-dose coverage
  needed (gated: unconfirmed, source is paywalled or blocked)). Accumulating susceptibles predicts outbreaks.
- **Catch-up / supplementary campaigns**: target age groups with immunity gaps;
  follow-up campaigns every few years where routine coverage is suboptimal.

## 5. Outbreak-response immunisation
- Rapid assessment of age distribution and vaccination status of cases, define target
  area and ages, launch quickly, use
  post-exposure prophylaxis where indicated (**per national guidance**).
- Coordinate with outbreak control
  (`health-medicine.public-health.outbreak-investigation.stepwise-field-investigation-and-control`).

## 6. Safety and confidence
- **AEFI surveillance**: report, investigate serious events, causality assessment
  (WHO algorithm), communicate transparently.
- Vaccine hesitancy: listen, presumptive recommendation by trusted clinicians,
  address specific concerns, reduce practical barriers (often bigger than beliefs).

## Gotchas
- Denominator drift makes coverage look fine where it's falling.
- Domestic fridges and freezer-plate contact causing silent freezing.
- Campaigns that pull staff from routine services, creating new gaps.

## Verify
- [ ] Denominators sourced and cross-checked.
- [ ] Forecast includes wastage and buffer.
- [ ] Data logger records reviewed; breach procedure posted on the fridge.
- [ ] Coverage, dropout and zero-dose counts tracked by area.
- [ ] AEFI reporting route in place and known to vaccinators.

## Checked

- Date checked: 2026-10-25. Jurisdiction: International (WHO EPI) with US and UK handbooks named; schedules and storage are product- and country-specific.
- Sources read: CDC Vaccine Storage and Handling page; WHO measles fact sheet.
- Confirmed: CDC: use digital data loggers and keep a backup; do not use out-of-range vaccine unless safety is confirmed; WHO: two doses are recommended to ensure immunity and prevent outbreaks.
- Corrected or removed: Removed the unsupported ">~10% dropout" threshold, the "twice daily" logging claim and the measles "within weeks" response timing.
- Gated: The 2-8 C range, shake test, VVM, and the measles R0 12-18 and 95% coverage figures: the UKHSA Green Book chapter and CDC toolkit PDFs came back as binary or landing pages, and the WHO and CDC measles pages state neither R0 nor a coverage threshold.

Method: documentation only; no commands were run.
