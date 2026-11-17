---
id: repair-maintenance.building-services-equipment-maintenance.building-electrical-maintenance.switchgear-thermography-and-periodic-inspection
name: switchgear-thermography-and-periodic-inspection
category: repair-maintenance
field: building-services-equipment-maintenance
product: building-electrical-maintenance
tags: [building-services-equipment-maintenance, building-electrical-maintenance, electrical-maintenance, switchgear, distribution-board, panelboard, mcb, mccb, rcd, rcbo, gfci, thermography, infrared, ir-camera, hot-spot, loose-connection, torque, insulation-resistance, megger, eicr, bs-7671, nfpa-70b, nfpa-70e, arc-flash, loto, safe-isolation, voltage-indicator, proving-unit, circuit-fault-finding, nuisance-tripping]
level: practitioner
status: gated
description: "Plan and interpret infrared surveys of loaded switchgear, carry out safe isolation and periodic inspection/testing (EICR, NFPA 70B), torque checks, RCD tests and fault-finding nuisance trips."
sources: ["https://www.hse.gov.uk/electricity/standards.htm", "https://www.electricalsafetyfirst.org.uk/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switchgear thermography and periodic inspection

**Goal:** find failing connections and overloaded circuits before they cause outages or
fires, and keep an inspection-and-test record that satisfies the standard. Electrical
work requires competence and, often, licensing; follow **NFPA 70E / 70B** (US) or
**BS 7671 and the Electricity at Work Regulations** with GS38 (UK).

## 1. Safe isolation (do it the same way every time)
1. Identify the circuit, isolate, **lock off with your own lock** and tag (LOTO).
2. Prove the tester (two-pole voltage indicator, GS38-compliant leads) on a known source
   or proving unit.
3. Test dead: all conductor combinations (L–N, L–E, N–E; L1–L2–L3 on three-phase).
4. Re-prove the tester on the known source.
5. Only then work. Never rely on a non-contact "volt stick" alone.

## 2. Thermographic (IR) survey of switchgear
- **Load matters:** survey at ≥40% of rated load (gated: unconfirmed, source is paywalled or blocked; many guides say higher is better);
  record the load current at each point — a cool connection on an unloaded circuit
  proves nothing.
- Open covers only with arc-flash risk assessed and PPE to the incident energy level,
  or use **IR windows** fitted to panels.
- Camera settings: set **emissivity** (bare copper/aluminium reflects — measure on
  insulation, tape or painted surfaces near the joint, or use a known-emissivity marker),
  reflected temperature, distance; focus sharply.
- Compare like with like: **ΔT between phases** carrying similar load is the key finding.
  Typical severity guidance (e.g. NETA-style): ΔT 1–3 °C between similar components =
  possible deficiency; 4–15 °C = probable, repair when possible; >15 °C = major, repair
  immediately (gated: unconfirmed, source is paywalled or blocked). Use your standard's table.
- Report each finding: image + visible photo, location, load current, ΔT, priority.

## 3. Periodic inspection and testing
- **Frequency:** per standard and risk — UK EICR commonly 5 years for commercial,
  more often for higher-risk premises; NFPA 70B (2023) now sets intervals by equipment
  condition (gated: unconfirmed, source is paywalled or blocked).
- **Visual:** damage, overheating marks, missing blanks, labelling and circuit charts,
  enclosures IP rating, cable support.
- **Tests (dead):** continuity of protective conductors, insulation resistance (typically
  500 V DC test on 230/400 V circuits, ≥1 MΩ minimum in BS 7671 (gated: unconfirmed, source is paywalled or blocked) — disconnect sensitive
  electronics/surge protection first), polarity.
- **Tests (live, with care):** earth fault loop impedance vs the maximum for the protective
  device, prospective fault current, **RCD/GFCI operation** (trip time at rated current,
  e.g. ≤300 ms for a general RCD at IΔn in BS 7671 (gated: unconfirmed, source is paywalled or blocked)) and the test button.
- **Torque checks:** after isolation, check terminations to the maker's torque — but
  don't repeatedly re-torque (it can deform conductors); use torque marks.

## 4. Fault-finding nuisance trips
| Trips | Likely cause |
|---|---|
| RCD on wet weather | Moisture in outdoor fittings/junction boxes |
| RCD at random, many circuits | Cumulative earth leakage — split circuits across RCDs, measure leakage with a clamp meter |
| MCB on startup | Inrush (motors, LED drivers) — device curve type (B vs C) |
| MCB warm/trips after hours | Overload — clamp-meter the current; check connection heat |
Isolate loads one at a time to find the culprit; use insulation resistance testing to
find faulty cables.

## Gotchas
- An IR image without load data and emissivity notes isn't a report.
- Neutral heating in buildings with lots of electronic loads (harmonics) — check neutral currents.
- Never open live panels for "a quick look" without the PPE category for that board.

## Verify
- [ ] Safe isolation proved with a tested tester before work.
- [ ] IR survey done at adequate load with load recorded; findings prioritised by ΔT.
- [ ] Test results recorded on a schedule of test results; failures coded.
- [ ] RCD trip times within limits; labelling and circuit charts current.
- [ ] Repairs re-scanned under load to confirm the hot spot is gone.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (NFPA 70E/70B) and United Kingdom (BS 7671, Electricity at Work Regulations); the standard in force on site governs.
HSE electrical standards page lists BS 7671 and the Electricity at Work Regulations as the UK references. The figures taken from NFPA 70B, NETA and BS 7671 could not be confirmed because those standards are paywalled; each is marked gated. The safe isolation sequence (prove, test dead, re-prove, lock off) is a procedure, not a figure, and is unchanged.

Method: documentation only; no commands were run.
