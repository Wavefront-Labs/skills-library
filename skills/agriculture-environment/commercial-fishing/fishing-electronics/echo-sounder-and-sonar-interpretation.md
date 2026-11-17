---
id: agriculture-environment.commercial-fishing.fishing-electronics.echo-sounder-and-sonar-interpretation
name: echo-sounder-and-sonar-interpretation
category: agriculture-environment
field: commercial-fishing
product: fishing-electronics
tags: [commercial-fishing, fishing-electronics, echo-sounder, fish-finder, sonar, omnidirectional-sonar, chirp, frequency, 50-khz, 200-khz, gain, tvg, colour-line, white-line, bottom-lock, a-scope, fish-marks, arches, bait-balls, thermocline, bottom-typing, second-echo, plotter, waypoints, marks, track-plotting, simrad, furuno, garmin, lowrance, humminbird, raymarine]
level: practitioner
status: draft
description: "Find fish with sounders and sonar: choose frequency, set gain, range and TVG, tell fish from bait, thermocline and noise, judge bottom hardness, and log marks for placing gear."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Echo sounder and sonar interpretation

**Goal:** turn the colours on the sounder into decisions — is that fish, what size,
how deep, and is the bottom right for the gear? This applies to any brand (Furuno,
Simrad, Garmin, Lowrance, Humminbird, Raymarine…); menu names differ, so check your
manual for the exact settings.

## 1. Choose the frequency
- **Low (~38–50 kHz)**: wide beam, goes deep, less detail; good for searching and deep
  water.
- **High (~120–200 kHz)**: narrow beam, sharp detail in shallow water, separates fish
  close to the bottom; attenuates faster with depth.
- **CHIRP** (frequency-swept) gives better target separation; use the low/medium/high
  CHIRP band as you would a single frequency.
- Dual-frequency side by side: a mark strong on low but weak on high is often bigger fish
  or a school deeper in the wide beam.

## 2. Set it up (manual mode beats auto when you know the ground)
1. **Range**: set so the bottom sits in the lower third of the screen, or use **bottom
   lock/zoom** to expand the last few metres above the seabed (essential for demersal fish).
2. **Gain**: increase until light speckles (noise) appear in the water column, then back
   off a little. Too low hides fish; too high paints everything.
3. **TVG** (time-varied gain): compensates for signal loss with depth so similar fish look
   similar at different depths. Leave at default unless you know why.
4. **Clutter/interference rejection**: medium; high settings can hide small fish.
5. **Colour line / white line**: separates the bottom from fish lying on it.
6. **Ping speed / scroll**: faster in shallow water; slow scroll at slow boat speed distorts shapes.

## 3. Reading marks
- **Arches** (on a moving boat): single fish passing through the cone — arch length depends
  on time in the beam, not fish size; **colour intensity** (signal strength) is the better
  size guide.
- **Dense blob / cloud**: schooling fish. Tight, strong-coloured school = bigger fish;
  diffuse, weak = **bait**/plankton or very small fish.
- **Thin horizontal band** in mid-water that persists: a **thermocline** or plankton layer
  (deep scattering layer at dusk rises toward the surface).
- **Vertical streaks** from the surface: aeration/turbulence or interference.
- **Fish on the bottom**: bumps on top of the bottom line, separated by the white line — use
  high frequency and bottom zoom.

## 4. Bottom typing
- **Hard bottom** (rock, gravel): thick, strong bottom echo and a strong **second echo**
  (a "ghost" bottom at about twice the depth).
- **Soft bottom** (mud): thinner, weaker return; weak or no second echo.
- Rough, jagged returns = rock/reef. Know it before setting trawls, nets or pots.

## 5. Sonar (horizontal/omni)
- Searches **around** the boat (hundreds of metres to km); shows schools ahead and their
  movement. Used heavily in purse seining and pelagic trawling.
- Set **tilt** (beam angle down from horizontal): shallower tilts search far; steeper tilts
  close to the boat and deeper. Use target tracking to read school speed and direction.
- Surface reverberation and wake noise near the boat are not fish.

## 6. Marks and placing gear
- Save **waypoints** on productive marks with names/notes (species, depth, date, tide).
- Correct for **layback**: gear is behind the boat (trawls and longline hooks can be far
  back) — place gear by its position, not the boat's.
- Track lines and plotter data are valuable fishery records — back them up.

## Gotchas
- Auto-gain changes as depth changes; marks that "disappear" may be gain, not fish moving.
- A transducer with weed, fouling or air bubbles beneath it = poor readings; clean it.
- Running two sounders on the same frequency causes interference.
- Fish size estimates from sounders are approximate unless the unit is calibrated (scientific
  echosounders).

## Verify
- [ ] Gain set by the noise method, range/zoom showing the bottom clearly.
- [ ] You can name what a mark is (fish, bait, thermocline, noise) and why.
- [ ] Bottom hardness checked by bottom thickness and second echo before setting gear.
- [ ] Waypoints saved with notes for every productive mark.
