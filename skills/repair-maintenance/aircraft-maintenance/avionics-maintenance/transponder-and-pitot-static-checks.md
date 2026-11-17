---
id: repair-maintenance.aircraft-maintenance.avionics-maintenance.transponder-and-pitot-static-checks
name: transponder-and-pitot-static-checks
category: repair-maintenance
field: aircraft-maintenance
product: avionics-maintenance
tags: [aircraft-maintenance, avionics-maintenance, avionics, transponder, mode-c, mode-s, ads-b, 91-411, 91-413, part-43-appendix-e, part-43-appendix-f, pitot-static, altimeter, encoder, altitude-encoder, air-data-test-set, leak-test, ifr-certification, ramp-tester, ifr-6000, adsb-out, vsi, airspeed-indicator]
level: practitioner
status: gated
description: "Perform the 24-month pitot-static leak test, altimeter/encoder correlation and transponder test (14 CFR 91.411/91.413, Part 43 App. E/F) with an air-data test set and transponder ramp tester."
sources: ["14 CFR 91.411, 91.413 and 91.217 (eCFR)", "14 CFR Part 43 Appendix E and Appendix F (eCFR)", "FAA AC 43-6D Altitude Reporting Equipment and Transponder System Maintenance and Inspection", "FAA AC 43.13-1B ch. 12"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transponder and pitot-static checks

**Goal:** carry out the recurrent checks that keep an aircraft legal for IFR and
controlled airspace: static system leak test, altimeter and encoder accuracy, and
transponder performance. In the US these are 14 CFR 91.411 (IFR, every 24 calendar months)
and 91.413 (transponder, every 24 months) with test content in Part 43 Appendix E (altimeter system) and F (ATC transponder), both confirmed in the eCFR.
Only appropriately rated repair stations (or the manufacturer) may test/certify the
altimeter itself; check your certificate/ratings before signing. EASA states have
equivalent national rules.

## 1. Equipment and setup
- Air-data test set (pitot and static outputs, rate control, known calibration date,
  e.g. a Barfield DPS or Laversab unit).
- Transponder/ADS-B ramp tester (e.g. Viavi/Aeroflex IFR-6000) with antenna at the
  documented test distance, or direct-connect with attenuation.
- Adapters that seal each static port and the pitot without damaging heated probes;
  pitot heat OFF and breaker pulled.
- Aircraft powered from ground power; avionics on and warm (~15 min).

## 2. Static system leak test
1. Connect the static line of the test set to *all* static ports (tape over any port
   not connected; alternate static source closed).
2. Apply suction slowly — never exceed the VSI or airspeed indicator limits; keep pitot
   ≥ static at all times (connect pitot too and move them together) or you can damage
   the ASI.
3. Bring to 1,000 ft above field elevation (typical (gated: unconfirmed, source is paywalled or blocked)). Isolate and time.
4. **Limit (unpressurised aircraft): ≤ 100 ft loss in 1 minute** (common practice from the AC 43-6D / aircraft maintenance manual method (gated: unconfirmed, source is paywalled or blocked)). Part 43 App. E itself only requires a proof test of the static system "in a manner acceptable to the Administrator" (and, for Part 25 aircraft, leakage within the 25.1325 tolerance); the 100 ft figure in App. E is the altimeter case-leak tolerance, a different test. Pressurised aircraft use the manufacturer's limit.
5. Leak hunting: work outward from the instruments — fittings on the back of the
   altimeter, encoder and autopilot air-data computers, quick-drains, and old rubber hose
   joints are the usual suspects. Snoop-type leak detector only where the manual allows
   near instruments.

## 3. Altimeter and encoder correlation
1. Set the altimeter Kollsman window to 29.92 inHg.
2. Step through test points (App. E table: e.g. 0, 500, 1,000 ft... up to the aircraft's
   maximum operating altitude) and compare indicated altitude to test-set altitude
   against the tolerance table (tolerance widens with altitude).
3. **Encoder correlation (App. E(c) and 91.217):** the difference between the transponder-reported
   altitude and the altimeter display may not exceed **125 ft** (App. E); 91.217 requires the encoder to be within 125 ft (95 % probability basis) of the indicated datum. Adjust encoder offsets per the encoder manual, or the
   transponder's configuration page on modern units.
4. Check scale error, hysteresis, after-effect and friction per App. E if certifying the
   altimeter itself (repair-station task).

## 4. Transponder test (Part 43 App. F)
With the ramp tester, verify (values from App. F, read in the eCFR on 2026-10-19; confirm your edition):
- Reply frequency 1090 ± 3 MHz (App. F; ±1 MHz applies to Mode S units with the optional 1090 ±1 MHz reply frequency).
- Suppression and side-lobe suppression behaviour.
- Receiver sensitivity (App. F: ATCRBS minimum triggering level −73 ±4 dBm; Mode S limits are given separately there).
- Peak RF output power within limits for the transponder class.
- Mode S address (ICAO 24-bit hex) matches the aircraft registration; flight ID correct.
- ADS-B Out (if installed): GPS position, NIC/NACp/SIL values, emitter category; run the
  FAA's Public ADS-B Performance Report after a flight for the US rule.

## 5. Paperwork
Logbook/permanent record entry listing tests performed, maximum altitude tested
(this limits the aircraft's IFR altitude), equipment used with calibration due date, and
the approval under which you signed.

## Gotchas
- Reverse-pressurising (static higher than pitot) can blow an ASI or VSI.
- Disconnecting any static line *after* the test reopens 91.411 for that part of the
  system — retest.
- Encoder Gillham (gray-code) wiring faults show up only at some altitudes; test every step.
- Altimeter tolerance tables (App. E Tables I-III) are not reproduced here; read them in the current Part 43 text.

## Verify
- [ ] Static leak within the manual/AC 43-6D limit (commonly ≤ 100 ft/min at 1,000 ft, unpressurised) with all ports connected.
- [ ] Altimeter within App. E tolerances at every test point; encoder within 125 ft.
- [ ] Transponder frequency, power, sensitivity and Mode S address within App. F.
- [ ] Test equipment in calibration; max tested altitude recorded in the entry.
