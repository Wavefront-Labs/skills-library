---
id: health-medicine.speech-language-pathology-and-audiology.hearing-instruments.hearing-instrument-troubleshooting-and-programming-workflow
name: hearing-instrument-troubleshooting-and-programming-workflow
category: health-medicine
field: speech-language-pathology-and-audiology
product: hearing-instruments
tags: [audiology, hearing-aids, hearing-instruments, noahlink-wireless, noah, fitting-software, phonak-target, oticon-genie, signia-connexx, resound-smart-fit, hearing-aid-troubleshooting, dead-aid, weak-sound, feedback, wax-guard, receiver-replacement, test-box, ansi-s3-22, coupler-measurement, remote-fitting, firmware-update, listening-check]
level: practitioner
status: draft
description: "Hearing-instrument workflow: connecting via Noah/Noahlink, safe programming and firmware updates, a dead/weak/feedback troubleshooting ladder, test-box checks against spec, and remote fitting."
sources: [HIMSA Noah 4 documentation, ANSI/ASA S3.22-2014 hearing aid specification, IEC 60118-7, manufacturer fitting-software user guides (Phonak, Oticon, Signia, ReSound, Widex, Starkey)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hearing instrument troubleshooting and programming workflow

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** program devices without losing settings, and fix a "not working" aid in
minutes with a fixed ladder before sending it for repair.

Status: draft — menu names differ across manufacturers and software versions; the
workflow is generic.

## 1. Programming environment
- **Noah** (HIMSA) holds patient records/audiograms and launches each manufacturer's
  module (Phonak Target, Oticon Genie 2, Signia Connexx, ReSound Smart Fit, Widex
  Compass, Starkey Pro Fit).
- Interface: **Noahlink Wireless** for most current wireless aids; older aids need
  HI-PRO/cable or manufacturer-specific links.
- Keep audiogram entered in Noah **before** opening the fitting module so the
  prescription uses it.

## 2. Safe programming habits
- **Read/connect first, save a session before changing anything** — always start from
  what the aid currently holds.
- **Firmware updates:** fully charged/fresh battery, no interruptions, one aid at a
  time if the software says so; re-run feedback calibration after an update.
- Save to aids and to Noah before closing; confirm "saved to device" for both sides.
- Label left/right correctly — swapped programs are a common fault.

## 3. Troubleshooting ladder (dead or weak)
1. **Power:** battery fresh (check with tester; pull tab removed ≥ 1–2 min before
   inserting for zinc-air), or charge contacts clean and charger lit correctly.
2. **Wax guard / filter** at the receiver — replace (most "dead" aids are blocked
   guards). Microphone covers/filters.
3. **Dome / tube / mould:** blocked with wax or moisture; slim tube kinked;
   condensation in moulded tubing — dry or replace.
4. **Receiver** (RIC): swap with a known-good receiver of the same power.
5. **Settings:** volume, program, muting, streaming state; connect and check program
   values against last saved session.
6. **Moisture:** dry with a drying kit/station.
7. **Listening check** with a stethoset: distortion, intermittency, static.
8. Then **test box** measurement vs specification (below) → repair if out of spec.

## 4. Feedback (whistling)
Check fit (dome size, mould shrinkage, ear wax in canal — **look in the ear**),
receiver seated, tube cracks; then re-run feedback calibration; then reduce
high-frequency gain or change coupling (smaller vent, closed dome, custom mould).
Feedback when hugging/near a phone is normal-ish.

## 5. Test-box (coupler) verification
- ANSI S3.22 / IEC 60118-7 test in a 2-cc coupler: OSPL90, full-on gain, frequency
  response, equivalent input noise, harmonic distortion, battery current.
- Compare to the device's spec sheet tolerances. Out of tolerance → repair or replace.
- Use for new devices (verify before fitting) and for repair returns.

## 6. Remote fitting
Patient app–based remote adjustments: confirm identity, a quiet environment, and that
the patient knows how to revert. Large gain changes should still be verified in clinic
with REM.

## Gotchas
- Programming before reading the device → overwriting settings with stale defaults.
- Wrong receiver power after swap (e.g. S vs M) → under-amplification.
- Interrupted firmware update → bricked aid.
- Blaming the aid when the ear canal is full of wax.

## Verify
- [ ] Session saved before and after changes; L/R confirmed.
- [ ] Ladder steps documented for any fault visit.
- [ ] Test-box result vs spec recorded before sending for repair.
- [ ] Feedback calibration re-run after hardware/firmware change.
- [ ] Patient demonstrated cleaning and wax-guard change.
