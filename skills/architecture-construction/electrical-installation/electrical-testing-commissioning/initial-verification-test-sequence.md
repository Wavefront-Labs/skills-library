---
id: architecture-construction.electrical-installation.electrical-testing-commissioning.initial-verification-test-sequence
name: initial-verification-test-sequence
category: architecture-construction
field: electrical-installation
product: electrical-testing-commissioning
tags: [electrical-installation, electrical-testing-commissioning, initial-verification, commissioning, dead-testing, live-testing, continuity, r1-r2, ring-final-test, insulation-resistance, megger, polarity, earth-fault-loop-impedance, zs, ze, pfc, rcd-test, gfci-test, trip-time, multifunction-tester, eic, certificate-of-compliance, safe-isolation, bs-7671, as-nzs-3000]
level: practitioner
status: draft
description: "Run the initial-verification test sequence on a new circuit: dead tests (continuity, IR, polarity) then live tests (loop impedance, PFC, RCD trip times), and certify."
sources: ["BS 7671 Requirements for Electrical Installations, Part 6", "IET Guidance Note 3: Inspection & Testing", "AS/NZS 3000 Wiring Rules, Section 8", "AS/NZS 3017 Electrical installations - Verification guidelines", "NFPA 70 National Electrical Code (NEC)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Initial verification test sequence

**Goal:** prove a new or altered circuit is safe to energise and leave in service — the
protective conductor is continuous, the insulation is sound, polarity is right, a fault
will disconnect fast enough, and RCDs trip in time — and record it on the certificate.

> **Licensed, jurisdiction-specific work.** Who may test and certify, and which tests
> are mandatory, depends on jurisdiction: UK BS 7671 Part 6 with an Electrical
> Installation Certificate; AU/NZ AS/NZS 3000 Section 8 with a certificate of
> compliance; US installs are typically inspected by the AHJ, with formal testing per
> project specs (e.g. NETA ATS) on commercial work. Limits below are typical; confirm
> against your edition of the wiring rules and the tables for your device.

## 0. Before you test
- **Inspect first:** correct cable sizes, devices, terminations torqued, labels, no
  damage — testing doesn't find a missing grommet.
- **Instrument:** calibrated multifunction tester (IR, low-ohm continuity, loop, RCD);
  probes to GS38-style (fused, shrouded, minimal exposed tip).
- **Order matters:** dead tests first, then live. Never live-test a circuit that failed a
  dead test.

## 1. Safe isolation for dead tests
1. Isolate the circuit (or board) and **lock off and tag**.
2. **Prove the tester** on a proving unit, **test dead** at the point of work across all
   conductor combinations, **re-prove the tester**.
3. Warn others; dead tests inject test voltages up to 500–1000 V DC.

## 2. Dead tests
1. **Continuity of protective conductors** — main and supplementary bonding, then each
   circuit's CPC. Typical method: link line to CPC at the board, measure L–CPC at every
   point; the highest reading at the far end is **R1+R2**. Null the leads first.
2. **Ring final continuity (UK):** measure end-to-end r1, rn, r2 (r1 ≈ rn; r2 ≈ 1.67× r1 for
   2.5/1.5 mm² twin-and-earth); cross-connect L–N and then L–CPC and read at each socket —
   readings should be nearly equal everywhere (a spike means a spur or a break).
3. **Insulation resistance:** disconnect or isolate electronics, SPDs, dimmers, drivers
   and RCD electronics; test L+N to E (and L–N where safe) at 500 V DC for circuits up to
   500 V. Typical minimum: ≥1 MΩ (UK BS 7671 and AU), and new work usually reads
   >200 MΩ. Investigate anything under ~2 MΩ even if it passes. SELV/PELV: 250 V test,
   ≥0.5 MΩ (unverified — confirm against your edition of the wiring rules).
4. **Polarity:** every switch and single-pole device in the line conductor; centre contact
   of ES/Edison lampholders on line; confirmed by the R1+R2 test.
5. **Earth electrode resistance** on TT systems; low values are better and must make the
   RCD operate — UK guidance treats readings over ~200 Ω as possibly unstable
   (unverified — confirm against your edition of the wiring rules).

## 3. Live tests (supply on, under the site's live-testing controls)
1. **Ze** — external earth-fault loop impedance at the origin with the earthing conductor
   disconnected (reconnect it immediately).
2. **Zs** — at the furthest point of each circuit. Compare with the maximum Zs for the
   device; apply the temperature correction (UK practice: compare with 80% of the table
   value when testing cold). Example order of magnitude: a B32 MCB on 230 V allows roughly
   1.37 Ω tabulated (unverified — confirm against your edition of the wiring rules).
   Check: Zs ≈ Ze + (R1+R2).
3. **Prospective fault current (PFC/PSCC)** at the origin, highest of L–N and L–E (×2 for
   three-phase estimate, or measure); must be ≤ device breaking capacity.
4. **RCD/GFCI:** 30 mA RCD at 1× IΔn must trip within 300 ms (general type); at 5× IΔn
   within 40 ms; test at 0° and 180°. AU/NZ uses similar ≤300 ms limits for 30 mA
   (unverified — confirm against your edition of the wiring rules). Then press the
   integral test button. US GFCI: test with the button and a plug-in tester.
5. **Phase sequence** on three-phase supplies; **functional tests** of switches,
   isolators, interlocks, emergency stops.

## 4. Record and certify
Enter every reading on the schedule of test results with instrument serial numbers, then
issue the certificate.

## Gotchas
- Testing IR with lamps or LED drivers connected: false low readings or destroyed drivers.
- Forgetting to remove the L–CPC link used for R1+R2 — remove it before energising.
- Ze with the earthing conductor disconnected leaves the installation unearthed: isolate
  the installation first and reconnect before restoring supply.

## Verify
- [ ] Inspection done before testing; tester calibrated, leads nulled.
- [ ] Isolated, locked off and proved dead (tester proved before and after) for dead tests.
- [ ] Continuity, IR, polarity all recorded and within limits; temporary links removed.
- [ ] Zs ≤ corrected maximum for each device; PFC ≤ breaking capacity.
- [ ] RCD trip times within limits at 1× and 5×; test button works.
- [ ] Certificate and test schedule completed and handed over.
