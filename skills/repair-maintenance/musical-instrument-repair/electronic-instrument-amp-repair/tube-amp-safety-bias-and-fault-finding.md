---
id: repair-maintenance.musical-instrument-repair.electronic-instrument-amp-repair.tube-amp-safety-bias-and-fault-finding
name: tube-amp-safety-bias-and-fault-finding
category: repair-maintenance
field: musical-instrument-repair
product: electronic-instrument-amp-repair
tags: [electronic-instrument-amp-repair, tube-amp, valve-amp, guitar-amp, amp-repair, filter-capacitors, cap-discharge, bleeder-resistor, dim-bulb-tester, variac, bias, bias-probe, plate-dissipation, 6l6, el34, el84, 6v6, 12ax7, preamp-tubes, power-tubes, crackle, hum, scratchy-pots, contact-cleaner, cold-solder-joint, chopstick-test, fender, marshall, vox]
level: advanced
status: draft
description: "Work safely inside a tube amp (discharge caps, dim-bulb test), then fix common faults: noisy tubes, crackle via chopstick test, scratchy pots, hum, and power-tube bias by dissipation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tube amp: safety, bias and fault finding

**Goal:** diagnose and fix the common faults in valve guitar/bass amps without getting
hurt. **Tube amps hold several hundred volts DC (often 350–500 V+) on filter
capacitors, even unplugged, potentially for days.** If you aren't confident with
high-voltage work, stop here and take it to a tech.

## 1. Safety routine (every time)
1. Unplug. Standby switch on/off doesn't make it safe.
2. One hand in your pocket when probing live; insulated probes and clip leads; no rings or watches.
3. **Discharge the filter caps**: a ~10 kΩ 5 W resistor on insulated clip leads from each
   cap's positive (or the power tube plate/B+ nodes) to chassis for several seconds.
   Then **measure** with a meter on DC volts — confirm <~5 V before touching anything.
4. First power-up after a repair or on an unknown amp: through a **dim-bulb tester**
   (incandescent bulb, ~60–100 W, in series with the mains) or a **variac**, so a short
   lights the bulb instead of blowing transformers.
5. Always run with a **speaker load** (or dummy load) connected — running output tubes
   without a load can arc and destroy the output transformer.

## 2. Triage by symptom
| Symptom | Likely cause | Check |
|---|---|---|
| No power, fuse blown | shorted power tube, rectifier, filter cap | Replace fuse with **same rating**; if it blows again, pull power tubes and retry on the dim-bulb |
| Hum at 100/120 Hz that rises with volume | **dried filter caps** (often 20+ years old) | Measure ripple on B+ (AC volts); replace caps |
| Hum at 50/60 Hz | ground loop, heater wiring, ground fault | Try a different outlet/cable; check heater center-tap |
| Crackle/pops, intermittent | noisy tube, cold solder joint, dirty sockets, failing plate resistor | Chopstick test (below) |
| Microphonic squeal | preamp tube (often V1) | Swap the first 12AX7 |
| Scratchy volume/tone | dirty pots | Contact cleaner + rotate |
| Cuts out with cable wiggle | jack contacts | Clean/re-tension input and speaker jacks |
| Red-plating power tube (plate glows red) | bias too hot, failed coupling cap, screen resistor fault | Turn off immediately; measure bias |

## 3. The chopstick test
Amp running, volume up modestly, with a load. Tap (don't poke) components with a
**wooden chopstick**: each tube, solder joints, sockets, resistors and wiring. Noise that
follows a tap localises the fault. Swap tubes one at a time with known-good spares.
Reflow suspect joints (shiny, concave fillet; cold joints are dull/grainy and ring-cracked).

## 4. Pots and jacks
Spray **contact cleaner** (e.g. DeoxIT D5) into the pot's opening, rotate end to end
20–30 times. Input and speaker jacks: clean contacts, bend the spring contact for firm
tension, tighten nuts so they don't spin and break leads.

## 5. Setting bias (fixed-bias amps)
Cathode-biased amps (many Vox AC30, Fender Champ-type, EL84 combos) don't need
adjustment. Fixed-bias amps with a bias trim pot do, when power tubes are replaced.
1. Fit matched power tubes, set the bias pot to the **coldest** (most negative grid
   voltage) setting before power-up.
2. Warm up on standby, then on with no signal, ~5 minutes.
3. Measure **cathode current** per tube with a **bias probe** (or across a 1 Ω cathode
   resistor if fitted: 1 mV = 1 mA). Measure **plate voltage** (B+ at the plate).
4. **Plate dissipation** = plate voltage × plate current (cathode current minus ~5% for
   screen current, approximately). Typical targets: **~60–70% of the tube's max rating**
   (e.g. 6L6GC max 30 W → ~18–21 W; EL34 25 W → ~15–17.5 W; 6V6 12–14 W → ~8–9.5 W).
5. Adjust the pot slowly; re-measure after 15–20 min of playing at temperature.
*Some techs bias by ear/scope at crossover; the dissipation method is the safe common
standard. Use the tube's datasheet, not the brand's marketing.*

## 6. Solid-state and keyboards (brief)
Solid-state amps: blown output transistors usually take emitter resistors and drivers
with them — check the whole output stage and DC offset at the speaker output
(<~50 mV). Keyboards/synths: dead keys are often dirty **keybed contacts** — clean rubber
contacts and PCB pads with isopropyl alcohol; check ribbon cables.

## Gotchas
- Never "test" by touching a lead to see if it's live.
- Replacing a fuse with a larger rating is how transformers burn.
- Filter caps are polarised; reversed electrolytics can explode.

## Verify
- [ ] Caps discharged and measured safe before every hands-in step.
- [ ] Repaired amp powered first through a dim-bulb/variac with a load connected.
- [ ] Fault localised (chopstick/tube swap) and fixed; no crackle on tap test.
- [ ] Bias at 60–70% dissipation per tube, matched within a few mA.
- [ ] Amp quiet at idle, clean at volume, fuse correct rating.
