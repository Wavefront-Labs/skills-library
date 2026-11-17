---
id: engineering-technology.electrical-engineering.etap.arc-flash-study
name: arc-flash-study
category: engineering-technology
field: electrical-engineering
product: etap
tags: [etap, arc-flash, arc-flash-study, incident-energy, ieee-1584, ieee-1584-2018, nfpa-70e, csa-z462, arc-flash-boundary, arc-flash-label, ppe, electrode-configuration, vcb, vcbb, hcb, reduced-arcing-current, short-circuit, protective-device-coordination, star, clearing-time, working-distance, power-system-study, electrical-safety, ieee-1584-2018-inputs, arc-flash-label-content]
level: advanced
status: gated
description: "Run an IEEE 1584-2018 arc-flash study in ETAP: model data, electrode config, trip times, reduced arcing current, NFPA 70E labels."
sources:
  - "IEEE Std 1584-2018, IEEE Guide for Performing Arc-Flash Hazard Calculations"
  - "NFPA 70E, Standard for Electrical Safety in the Workplace (2024 edition)"
  - "CSA Z462, Workplace Electrical Safety"
  - "ETAP user guide, Arc Flash and Short Circuit modules (vendor documentation)"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Arc-flash study in ETAP — IEEE 1584-2018 incident energy to defensible labels

**Goal:** produce incident energy (cal/cm²) and arc-flash boundary for every bus a
worker could open while energised, using IEEE 1584-2018 in ETAP, with trip times
taken from the real protection settings, and turn that into NFPA 70E-compliant labels.

> **Safety:** a study is not permission to work live. NFPA 70E requires an
> energised work justification and permit first; the label only sizes the PPE when
> de-energising is infeasible. Establishing an electrically safe work condition is
> always the first choice.

## 1. Data you must collect (the study is only as good as this)
- Utility source: max **and** min available fault (MVAsc and X/R) — get both in writing.
- Transformers: kVA, %Z, X/R, tap, winding connection, grounding.
- Cables: size, length, conductors per phase, raceway type.
- Every protective device: make/model, CT ratio, actual settings as found (not as
  designed), fuse type and rating, breaker trip unit settings and opening time.
- Motors that contribute meaningful fault current (group small ones).
- Per bus: equipment type, voltage, **electrode configuration**, enclosure size, gap.

## 2. Model setup in ETAP
1. Build the one-line; run **Short Circuit** first (ANSI or IEC) and sanity-check
   bus fault levels against hand calcs (infinite-bus transformer: `Isc ≈ FLA / Z_pu`).
2. In each bus editor's arc-flash page set equipment type; ETAP fills IEEE 1584-2018
   typical gap, working distance and enclosure size. Override when you have the
   real dimensions. Exact tab/field names vary between ETAP versions — check yours.
3. Electrode configuration (new in 2018 and a large driver of results):
   **VCB** (vertical conductors in box — typical switchgear/panels), **VCBB**
   (vertical, terminated on an insulating barrier), **HCB** (horizontal in box —
   often the worst case, e.g. some MCC buckets and bus duct taps), **VOA/HOA** (open air).
   If you are unsure between VCB and HCB, run both and label the worse one.
4. Typical IEEE 1584-2018 working distances: 455 mm (18 in) for LV MCCs and
   panelboards, 610 mm (24 in) for LV switchgear, 910 mm (36 in) for 5/15 kV switchgear (typical values (gated: unconfirmed, source is paywalled or blocked); use the standard's table and the actual task distance).
5. In the Arc Flash study case: method IEEE 1584-2018, arc-flash boundary at
   **1.2 cal/cm²** (second-degree burn threshold, as described in secondary NFPA 70E summaries; the standard is paywalled (gated: unconfirmed, source is paywalled or blocked)), source fault from the short-circuit
   case, and clearing time **from protective device curves** (ETAP pulls them from
   Star/TCC data) — never a blanket fixed time.

## 3. Trip times, the main-breaker trap and reduced arcing current
- Clearing time = relay operate time + breaker interrupting time (e.g. 5-cycle MV
  breaker ≈ 0.083 s at 60 Hz, computed 5/60). Fuses: total clearing curve.
- **The device that clears a fault on the line side of a main is the upstream one**
  (often the transformer primary). Model the main's line-side terminals as a
  separate location; that is frequently the highest number on the label.
- IEEE 1584-2018 requires a second calculation with the **reduced arcing current**
  (variation correction factor). Lower current can push a device into its slow
  inverse region and *raise* energy. ETAP runs both; report the worse.
- Many practitioners cap duration at 2 s on the basis that a worker can move away;
  IEEE 1584 treats this as engineering judgment, not a rule. Document it if used.
- Run every operating scenario: max and min utility, tie closed/open, generator-only.
  The minimum-fault case often governs because devices trip slower.

## 4. Applicability limits (state them in the report)
IEEE 1584-2018 model ranges are three-phase AC, 208 V–15 kV (confirmed in IEEE introductory slides), bolted fault 500 A–106 kA at 208–600 V and 200 A–65 kA at 601 V–15 kV (from EasyPower and ETAP documentation, not the standard itself), gaps and enclosure sizes within the
standard's tables. Outside these (DC systems, single-phase, > 15 kV) the empirical
model does not apply — use another documented method (e.g. Lee, or published DC
methods) and flag it. Confirm every boundary value, including electrode gap limits, against the standard before quoting (gated: unconfirmed, source is paywalled or blocked).

## 5. Labels (NFPA 70E 130.5(H))
Label must show nominal voltage, arc-flash boundary, and at least one of: incident energy
with working distance **or** the PPE category (not both), minimum arc rating of clothing, or a
site-specific PPE level. Do not mix the incident
energy method and the PPE-category tables on the same equipment. Review the study
when the system changes and at least every 5 years (the five-year interval and section numbers could not be confirmed from free sources (gated: unconfirmed, source is paywalled or blocked); check the adopted NFPA 70E edition). Arc-flash work is life-safety critical: studies must be performed and signed off by a qualified electrical engineer.

## 6. Reducing high results
Cut clearing time, never massage inputs: maintenance switch on LV trip units,
zone-selective interlocking, bus differential, arc-flash (light + current) relays.

## Verify
- [ ] Bus fault currents agree with an independent hand or spreadsheet check within ~10%.
- [ ] Every device setting in the model was field-verified, not copied from design drawings.
- [ ] Line side of each main is a separate location cleared by the upstream device.
- [ ] Both full and reduced arcing current results reviewed for each scenario; worst case labelled.
- [ ] Electrode configuration and working distance chosen per bus and justified.
- [ ] Labels show incident energy or PPE category, not both; study date recorded.
