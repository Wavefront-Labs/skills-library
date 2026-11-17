---
id: repair-maintenance.consumer-electronics-repair.audio-video-equipment-repair.amplifier-recap-and-output-stage-bias
name: amplifier-recap-and-output-stage-bias
category: repair-maintenance
field: consumer-electronics-repair
product: audio-video-equipment-repair
tags: [audio-video-equipment-repair, hifi-repair, vintage-hifi, amplifier-repair, receiver-repair, stereo-receiver, recapping, electrolytic-capacitor, filter-capacitor, output-transistors, output-stage, bias-adjustment, quiescent-current, dc-offset, dim-bulb-tester, variac, protection-relay, contact-cleaner, deoxit, service-manual, dummy-load, signal-generator, turntable-service, speaker-repair, mains-safety]
level: advanced
status: draft
description: "Restore vintage and modern hi-fi amplifiers and receivers: safe power-up on a dim-bulb or variac, selective recapping, output transistor checks, bias and DC offset setting, relay cleaning."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Amplifier recapping, output stage repair and bias setting

**Goal:** bring an amplifier or receiver back to safe, quiet, in-spec operation —
power it up without smoke, replace what has actually aged, repair a blown output
stage and set bias and DC offset to the service manual.

## 1. Before power: safety and intake
- Get the **service manual** (bias points, DC offset spec, voltages); vintage manuals
  are widely shared by enthusiast communities.
- Main filter capacitors can hold 50–100 V DC at high current; tube gear holds 300–
  500 V. Discharge with a resistor (~1 kΩ 5 W for solid-state, higher for tube) and
  measure before touching.
- Check the mains cord and plug, fuse rating (correct value, not a bigger one) and
  that any voltage selector is on the local mains.
- Never power an unknown unit straight from the wall. Use a **dim-bulb tester**
  (60–100 W incandescent in series with live) or a variac brought up slowly over
  minutes, watching current. A bulb that stays bright = a short; stop.

## 2. Diagnose before recapping
1. With a dummy load (8 Ω, rated power resistors) on each channel and no speakers,
   measure **DC offset** at each speaker output: under ~50 mV is typical good; over
   ~100 mV or one channel far higher points at a fault in that channel.
2. Protection relay not clicking in: the protection circuit is sensing offset or
   overcurrent — find the cause, don't bypass the relay.
3. Output transistors: in diode mode, base-emitter and base-collector junctions read
   ~0.4–0.7 V one way and open the other; collector-emitter near 0 is a short (lift
   a leg to confirm in-circuit readings). One shorted output device
   usually takes out its driver, emitter resistors (0.22–0.47 Ω) and sometimes the bias
   transistor — check them all.
4. Scratchy pots and switches: contact cleaner (DeoxIT-type), operate the control
   20–30 times.

## 3. Recapping (selective, not blanket)
- Electrolytics dry out after ~20–40 years; replace main filter caps, power-supply
  caps and coupling caps in the signal path where ESR is high or they leak/bulge.
  Measure ESR with an ESR meter rather than assuming.
- Replace like for like: same capacitance, **equal or higher voltage**, 105 °C rated,
  same lead spacing. Observe polarity (marking on the board can be faded; photograph
  first).
- Film and ceramic caps rarely fail; leave them unless specific problem types are
  known for the model (Draft note: model-specific weak-part lists not given here).
- Work one board section at a time; it limits wiring and polarity mistakes.

## 4. Replacing output devices and setting bias
1. Fit matched pairs (hFE-matched NPN/PNP where specified), new insulating pads or
   thermal compound, and correct mounting torque. A missing mica insulator shorts the
   collector to the heatsink.
2. Turn the **bias trimmer to minimum** before first power-up after any output repair.
3. Power through a dim bulb, then a variac to full mains. Warm up for ~15 minutes.
4. Measure bias as the manual says — usually voltage across an emitter resistor (e.g.
   a few mV to ~20 mV), converted to quiescent current. Adjust slowly, recheck after
   another 15–30 minutes as it drifts warm.
5. Set DC offset trimmer (if present) to as near 0 mV as possible.
6. Check with a signal generator and scope into the dummy load: clean sine waves up
   to rated power, symmetrical clipping, no oscillation.

## 5. Turntables and speakers (quick notes)
- Turntables: replace the stretched drive belt, clean old grease from the platter
  bearing and re-oil, adjust tracking force and anti-skate to the cartridge spec.
- Speakers: foam surrounds rot after 15–25 years; refoam with the cone centred
  (shim the voice coil gap) or replace the driver with a matching Thiele-Small spec.

## Gotchas
- Some vintage units have a "death cap" (line-to-chassis capacitor); replace with a
  safety-rated Y-class part.
- Bias set cold reads low; always set warm.
- Polarised-cap reversal in a high-voltage supply can vent violently on power-up.
- Counterfeit output transistors are common from unofficial sellers; buy from
  authorised distributors.

## Verify
- [ ] DC offset within spec on all channels after 30 minutes warm.
- [ ] Bias at the manual figure warm, both channels; heatsinks warm, not hot, at idle.
- [ ] Clean sine output to rated power into a dummy load; no oscillation.
- [ ] Protection relay engages after its normal delay; no hum or crackle at volume.
- [ ] Mains fuse is correct rating; chassis earth continuity confirmed.
