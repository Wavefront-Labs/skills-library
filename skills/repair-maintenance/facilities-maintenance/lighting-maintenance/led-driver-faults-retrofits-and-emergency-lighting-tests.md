---
id: repair-maintenance.facilities-maintenance.lighting-maintenance.led-driver-faults-retrofits-and-emergency-lighting-tests
name: led-driver-faults-retrofits-and-emergency-lighting-tests
category: repair-maintenance
field: facilities-maintenance
product: lighting-maintenance
tags: [lighting-maintenance, led-retrofit, led-driver, ballast, ballast-bypass, fluorescent-tube, t8, t5, led-panel, downlight, flicker, emergency-lighting, emergency-light-test, monthly-flick-test, annual-duration-test, maintained-emergency, exit-sign, dali, occupancy-sensor, photocell, lockout-tagout, safe-isolation, voltage-tester, bs-5266, nfpa-101]
level: practitioner
status: draft
description: "Diagnose dead or flickering LED and fluorescent fittings, replace drivers and do LED retrofits safely, and run monthly and annual emergency lighting tests with proper records."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LED driver faults, retrofits and emergency lighting tests

**Goal:** get failed lights back on quickly, choose replace-lamp vs replace-driver vs
replace-fitting correctly, and keep the emergency lighting tested and recorded so it
works in a power cut.

## 1. Safety first — isolate and prove dead
Anything beyond swapping a plug-in lamp is work on fixed wiring.
1. Identify the circuit (circuit chart / CMMS), switch off **and lock off** the
   breaker with a personal padlock and tag. A wall switch is not isolation — it may
   switch only the line, or be on a two-way circuit.
2. **Test before touch:** check your voltage tester on a known live source or proving
   unit, test all conductors at the fitting (L-N, L-E, N-E), then re-prove the tester.
3. Watch for: shared neutrals, emergency fittings with a separate permanent live
   (unswitched), and capacitors in old ballasts.
Fitting replacement and retrofits are often restricted to qualified electricians.
(Draft note: who may do this varies by jurisdiction and employer policy — e.g. UK
Part P / BS 7671 competence, US state electrical licensing, Australian licensed-only
rules. Follow your site's authorisation.)

## 2. Diagnosing a dead or flickering fitting
| Symptom | Likely cause | Action |
|---|---|---|
| One fluorescent tube dark ends / flicker | Tube or starter end of life | Replace tube (and starter on switch-start) |
| Whole fitting dead, others on circuit OK | Driver/ballast, loose connector | Check supply at driver input, then output |
| LED flickers at low dim | Driver/dimmer incompatibility | Check dimmer compatibility list; set minimum level |
| LED strobes or cycles on/off | Driver thermal cutout or failing capacitors | Replace driver; check ventilation |
| Many fittings on one circuit dead | Breaker/RCD, controls | Trace upstream; check sensors/DALI |
Measure the LED driver output with a multimeter: constant-current drivers show a
voltage within their rated window (e.g. 25–42 V DC) under load; no output with input
present means a failed driver. Replacement drivers must match **output current (mA)**,
voltage window, dimming type (DALI, 1–10 V, phase, non-dim) and physical size.

## 3. LED retrofits
- **Plug-and-play (Type A) tubes** run on the existing ballast — quick, but limited to
  compatible ballasts.
- **Ballast-bypass (Type B)** tubes wire mains directly to the lampholders: remove the
  ballast, rewire per the label, use non-shunted holders where required, and **label
  the fitting** "ballast bypassed — do not fit fluorescent tubes". This alters the
  fitting's certification; many sites only allow it by electricians.
- Whole-fitting replacement (LED panel or batten) is usually cleaner and longer-lived.
- Match colour temperature across a room (e.g. 4000 K) and check CRI ≥ 80.
- Dispose of fluorescent tubes as hazardous (mercury) waste.

## 4. Emergency lighting tests
Typical regime (Draft note: check your local code — e.g. UK BS 5266-1, EU EN 50172,
US NFPA 101 — for exact intervals and durations):
- **Monthly functional ("flick") test:** simulate mains failure via the key switch
  (not the breaker), walk every fitting and exit sign, confirm each lights. Keep it
  short (seconds to a minute is typical).
- **Annual full-duration test:** run for the rated duration (commonly 3 h, sometimes
  1 h or 90 min). Do it when the building can tolerate it, and allow 24 h recharge
  afterwards before occupancy relies on it.
- Self-test fittings: read the status LED and the central panel log; still walk them.
- Record date, fittings tested, failures and remedial work in the logbook/CMMS.
- Failed fittings are usually battery (typically 3–5 year life) or LED module; date-
  label new batteries.

## Gotchas
- Never test emergency lights by switching off the lighting circuit breaker if it
  also feeds other loads; use the dedicated test key switch.
- Driver mA mismatch gives a dim or quickly burnt-out LED board.
- Mixing LED tube brands in one ceiling looks patchy.
- Working at height: use a podium step, not a chair; tower above ~2.5 m.

## Verify
- [ ] Circuit locked off and proven dead before opening fittings.
- [ ] Replacement driver matches current, voltage window and dimming type.
- [ ] Bypassed fittings labelled; tubes disposed as hazardous waste.
- [ ] Monthly and annual emergency tests recorded with failures actioned.
- [ ] All fittings on and stable after reinstatement, no flicker at minimum dim.
