---
id: repair-maintenance.motorcycle-small-engine-repair.generator-repair.no-output-diagnosis-avr-and-brushes
name: no-output-diagnosis-avr-and-brushes
category: repair-maintenance
field: motorcycle-small-engine-repair
product: generator-repair
tags: [generator-repair, portable-generator, no-output, avr, automatic-voltage-regulator, brushes, slip-rings, rotor, stator-windings, field-flashing, residual-magnetism, excitation, capacitor-generator, brushless, inverter-generator, frequency, hz, governor-speed, multimeter, megger, insulation-resistance, transfer-switch, backfeed, generac, champion, honda-eu]
level: practitioner
status: draft
description: "Fix a portable generator that runs but gives no power: breakers and GFCI, engine speed/frequency, brushes and slip rings, AVR and capacitor tests, winding resistance, and field flashing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# No-output diagnosis: AVR, brushes and windings

**Goal:** a generator whose engine runs but whose outlets are dead (or low voltage)
traced to the actual fault — often a cheap brush, AVR or lost residual magnetism — and
safely back in service.

**Danger:** generator windings produce lethal voltage even with no load. Live tests are
done only with insulated probes, one hand, and no contact with the frame or windings;
disconnected tests are done with the engine off, plug cap off, and capacitors
discharged. Never backfeed a house without a **transfer switch or interlock** — it can
kill line workers.

## Identify the type
- **Brushed with AVR** (most open-frame portables): rotor field fed through brushes/
  slip rings, regulated by an AVR.
- **Brushless capacitor-excited** (many cheaper units): a capacitor on an auxiliary
  winding excites the rotor; no AVR or brushes.
- **Inverter** (Honda EU, Yamaha EF-i etc.): AC from a multi-pole alternator → inverter
  module. Diagnosis is mostly "test stator windings, then replace the inverter module";
  internal boards aren't field-repairable.

## 1. Simple checks first
1. **Breakers** on the panel reset; **GFCI** outlets reset (press test/reset). Many "no
   output" calls end here.
2. Idle/eco switch off (eco mode on some units outputs only when loaded).
3. **Engine speed**: conventional 2-pole generators must run at **3,600 rpm for 60 Hz
   (3,000 for 50 Hz)**. Check frequency with a meter set to Hz or a plug-in meter at no
   load — typically ~61–63 Hz (or ~51–52 Hz) no-load, dropping slightly under load.
   Low speed (governor, carb, choke) = low voltage and AVRs may shut down below a
   threshold frequency.

## 2. Brushes and slip rings (brushed units)
1. Engine off. Remove the brush holder (usually two screws on the end bell).
2. Brushes: length vs spec (replace when short, cracked, or chipped); springs pushing;
   leads intact.
3. Slip rings: clean with fine non-metallic abrasive if blackened; look for pitting.
4. **Rotor resistance** across the slip rings: often a few ohms to tens of ohms (check
   spec). Open = rotor fault; also check rotor to shaft = OL (insulation).

## 3. Stator windings
With the AVR and outlets disconnected:
- **Main windings** (to the outlets): very low resistance, often <1–2 Ω, equal between
  matching windings.
- **Exciter/auxiliary winding** (feeds the AVR or capacitor): spec in the manual.
- **Insulation to frame**: OL on a meter; a **500 V insulation tester (megger)** is better —
  readings of at least ~1 MΩ are commonly considered acceptable for small machines.
- Burnt smell, discoloured varnish = winding damage → rewind or replace stator.

## 4. AVR / capacitor
- **AVR**: if brushes, rotor and stator test good and there's still no output,
  suspect the AVR (they fail from overload and surges). Check its fuse if fitted.
  Confirm by field flashing (below): if output appears with external excitation, the
  AVR or exciter winding is the likely fault.
- **Capacitor units**: check the capacitor (bulging, leaking); measure capacitance with
  a meter (μF value is printed on the case, typically tens of μF). Discharge it first.

## 5. Field flashing (restore residual magnetism)
Generators that sat unused, ran with a load connected at shutdown or had the AVR
disconnected may lose **residual magnetism** — the rotor has nothing to start excitation.
Common methods (check the manual):
- **Drill method** (for units with a household outlet): plug in a corded drill, run the
  generator, press the drill trigger and spin the drill chuck **backwards** by hand for
  a few seconds — this momentarily makes the drill's motor generate into the field.
- **Battery method**: with the engine running and AVR disconnected per the manual,
  briefly (1–3 s) touch a 9–12 V battery to the brush leads observing polarity.
Then retest output with no load.

## 6. After repair
- No-load voltage within spec (e.g. ~120/240 V ±~5% or 230 V ±~5%) and frequency correct.
- Load test with a known resistive load (heater or a load bank) to ~75–100% of the
  running rating: voltage stays up, engine doesn't hunt.
- Ground/bond per the manual (floating neutral vs bonded neutral matters for transfer-
  switch use and GFCI behaviour).

## Gotchas
- Running a generator indoors or in a garage — carbon monoxide kills. Outdoors, away from windows.
- Ethanol-fuel varnish causes most low-speed/hunting issues (see carburettor-fuel-systems).
- Overloaded with motor-start surges (pumps, compressors), AVRs and windings fail.

## Verify
- [ ] Breakers, GFCI and eco mode ruled out.
- [ ] Frequency correct at no load (hence engine speed correct).
- [ ] Brushes, rotor, stator and insulation values recorded vs spec.
- [ ] Output restored and stable under a resistive load test.
- [ ] Owner reminded: transfer switch/interlock only, never backfeed; outdoor use only.

*Draft: resistance values are model-specific; drill-flashing works on many brushed units but follow the maker's method.*
