---
id: repair-maintenance.building-services-equipment-maintenance.pump-motor-maintenance.seal-bearing-alignment-and-vfd-fault-service
name: seal-bearing-alignment-and-vfd-fault-service
category: repair-maintenance
field: building-services-equipment-maintenance
product: pump-motor-maintenance
tags: [building-services-equipment-maintenance, pump-motor-maintenance, centrifugal-pump, end-suction-pump, inline-pump, mechanical-seal, gland-packing, motor-bearings, regreasing, shaft-alignment, laser-alignment, dial-indicator, soft-foot, coupling, vibration, vibration-analysis, velocity-mm-s, iso-10816, iso-20816, vfd, vsd, variable-frequency-drive, overcurrent-fault, overvoltage-fault, ground-fault, megger, cavitation, npsh]
level: practitioner
status: draft
description: "Service building pumps and motors: diagnose leaks and vibration, replace a mechanical seal, regrease bearings correctly, laser-align couplings and triage VFD faults."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Seal, bearing, alignment and VFD fault service

**Goal:** pumps and motors that run cool, quiet and dry for years. Most early failures
trace back to misalignment, wrong greasing or running the pump away from its duty point.

## 1. Rounds checks (weekly/monthly)
- **Leaks:** mechanical seals should be dry (a few drops/hour at most); gland packing
  should **drip** (roughly 40–60 drops/min is a common guide) — a dry packing burns the
  shaft sleeve.
- **Noise:** gravel/marbles sound at the pump = **cavitation** (suction starved — closed
  valve, blocked strainer, low NPSH) or recirculation at low flow. Rumble/whine at the
  motor = bearings.
- **Temperature:** bearing housings by IR thermometer — trend it; a sudden rise of
  10 °C+ over the baseline warrants investigation.
- **Vibration:** handheld meter, velocity mm/s RMS on bearing housings in horizontal,
  vertical, axial. Compare with baseline and ISO 10816/20816 class zones (for small
  machines, roughly <2.8 mm/s good, >7.1 mm/s unacceptable — use the class for the machine).

## 2. Mechanical seal replacement (end-suction / inline pump)
1. Isolate electrically (LOTO), close suction and discharge valves, drain and
   de-pressurise the casing.
2. Back-pull or lift-out: remove the motor/rotating assembly per the design, mark
   impeller and coupling positions.
3. Remove impeller (left-hand thread on some; hold the shaft, not the coupling bolts).
4. Withdraw the old seal; inspect shaft/sleeve for scoring at the elastomer seat —
   replace the sleeve if grooved.
5. Fit the new seal **without touching the faces** (finger oils damage them); lubricate
   elastomers with water or soapy water/glycerine as the seal maker allows — never oil
   or grease on EPDM. Set the working length/setting dimension if not a cartridge seal.
6. Reassemble, refill and **vent the casing** fully. Never run a mechanical seal dry,
   even for seconds.

## 3. Motor bearings: greasing done right
- Use the grease type the nameplate/maker specifies (polyurea is common on motors);
  don't mix incompatible thickeners.
- Calculate quantity: rule of thumb **G (g) = 0.005 × D (mm) × B (mm)** (outer diameter ×
  width), or the maker's figure. Over-greasing causes heat and seal blowout.
- Remove the drain plug, grease with the motor running if safe to do so (or per maker),
  run 30 minutes before refitting the plug so excess purges.
- Sealed-for-life bearings: no greasing; replace at failure/schedule.

## 4. Shaft alignment
1. Check **soft foot** first: dial or laser on each foot, loosen one bolt at a time;
   movement >~0.05 mm → shim that foot.
2. Use a laser alignment system (or reverse dial indicators). Correct vertical (shims
   under feet) then horizontal (jacking bolts).
3. Typical tolerance for 1500/1800 rpm couplings: offset ≲0.05–0.08 mm and angularity
   ≲0.05–0.07 mm/100 mm — use the alignment tool's table for the speed.
4. Re-check after tightening down and after the first hours of running (pipe strain moves
   pumps — unbolt the flanges briefly to check pipe strain if alignment keeps drifting).

## 5. VFD fault triage
1. **Record the fault code and the drive's fault log** (time, current, DC bus volts).
2. Overcurrent at acceleration → ramp too fast, mechanical bind, motor short; check
   by uncoupling and spinning the pump by hand.
3. Overvoltage at deceleration → decel too fast on high-inertia fans; lengthen ramp or
   enable overvoltage control.
4. Ground/earth fault → **insulation test the motor and cable** with the drive
   disconnected (motor IR >~100 MΩ new; low single-digit MΩ is suspect). Never megger
   through a VFD.
5. Overtemperature → blocked heatsink fans/filters, hot plant room.
6. Check the BMS speed reference and run command — "fault" can be lost signal.

## Gotchas
- Running a pump with discharge valve shut overheats it in minutes.
- Bearing currents on VFD-driven motors leave fluting (washboard marks); fit shaft
  grounding rings/insulated bearings on larger motors.
- Replacing a seal without fixing misalignment or cavitation means another seal soon.

## Verify
- [ ] LOTO and valves isolated before opening; casing vented on restart.
- [ ] Seal dry after one hour of running; no packing smoke.
- [ ] Soft foot corrected; final alignment in tolerance and recorded.
- [ ] Vibration and bearing temperature recorded as new baseline.
- [ ] VFD fault cause identified, logged, and fault not repeated over a full cycle.
