---
id: energy-mining-utilities.amateur-radio.radio-direction-finding.foxhunting-with-a-yagi-attenuator-and-triangulation
name: foxhunting-with-a-yagi-attenuator-and-triangulation
category: energy-mining-utilities
field: amateur-radio
product: radio-direction-finding
tags: [radio-direction-finding, rdf, df, direction-finding, foxhunt, foxhunting, fox-hunting, transmitter-hunting, t-hunt, ardf, amateur-radio-direction-finding, bunny-hunt, tape-measure-yagi, yagi, front-to-back, body-fade, offset-attenuator, step-attenuator, s-meter, signal-strength, bearing, triangulation, magnetic-declination, compass, multipath, reflections, interference-hunting, rfi, 2m, 80m]
level: intro
status: draft
description: "Find a hidden transmitter on 2 m: take bearings with a handheld Yagi, triangulate on a map, beat multipath, and close in with an attenuator or offset attenuator when the signal overloads the radio."
sources:
  - "Amateur foxhunting and ARDF guides (national societies, ARDF rules); offset-attenuator technique as widely described in amateur DF articles; paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foxhunting with a Yagi, attenuator and triangulation

**Goal:** locate a hidden transmitter (the "fox") quickly. The same skills find a stuck
microphone on a repeater or an interfering device. The common failure is the end
game: the signal gets so strong the radio saturates and every direction reads full
scale.

## 1. Kit
- **Directional antenna:** a 2 m 3-element Yagi (the cheap "tape-measure Yagi" built
  from steel tape elements on PVC is a classic). It has a clear front lobe and a
  usable null off the back.
- **Receiver with an S-meter**, preferably one that reads signal steps finely
  (some handhelds barely move).
- **Attenuation:** a step attenuator in the coax and/or an **offset attenuator** — a
  small device that mixes the signal with a local oscillator so you listen a few MHz
  away on a product whose strength you can turn down smoothly. Essential at close range.
- Map (paper or app), compass, notebook, and for a car hunt a co-driver.

## 2. Taking a bearing
1. Get to **high, open ground** away from buildings and metal fences. Reflections are
   the biggest source of false bearings.
2. Hold the Yagi horizontal or vertical to match the fox's polarisation (FM foxes are
   usually vertical).
3. Turn slowly through 360°; note the direction of **maximum** signal. Use the
   attenuator to keep the S-meter **below full scale** — a pinned meter has no peak.
4. Cross-check with the back/null; with some antennas the null is sharper than the
   peak.
5. **Body fade** with no antenna: hold the handheld close to your chest and turn;
   the signal dips when your body is between the radio and fox. Rough but quick.
6. Read the bearing with a compass held away from metal; note whether it's magnetic or
   true, and **correct for magnetic declination** before plotting on a map.

## 3. Triangulate
- Take bearings from **at least three well-separated locations**, roughly 60–120°
  apart as seen from the fox if possible.
- Plot each as a line on the map; they form a triangle. The fox is usually in or near
  it. A wild outlier is probably a reflection — retake from elsewhere.
- Move toward the triangle, retaking bearings as you go.

## 4. Multipath traps
- In valleys and between buildings, signals arrive from reflections; bearings swing as
  you move a few metres. Move to open ground and retake.
- Signal strength jumping up and down as you walk = interference patterns, not
  necessarily distance.

## 5. Closing in
- Add attenuation steadily; switch to the offset attenuator. Some hunters remove the
  antenna entirely and use the radio alone, or tune to a harmonic or image of the
  frequency where the signal is weaker.
- On foot, sweep slowly; the fox is often hidden at ground level, in a bush, under
  a bench or in a container. Check bins and trees.
- Respect property and safety: don't trespass, and keep away from roads while
  watching the S-meter.

## 6. Interference hunting
Same method for a real interference source, but stop at identifying the location.
**Don't confront or tamper**; report to the repeater trustee or the national
regulator, who has enforcement powers.

## 7. ARDF sport
International ARDF uses 2 m and 80 m, several foxes transmitting in timed cycles,
orienteering maps and on-foot running. Train bearings on the move and quick map work.

## Verify
- [ ] Bearings taken from high, open ground with the meter below full scale.
- [ ] Declination corrected; three well-separated lines plotted.
- [ ] Outlier bearings retaken, not trusted.
- [ ] Attenuation increased steadily while closing; fox found without trespass.
