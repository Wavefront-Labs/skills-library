---
id: sports-recreation.water-sports-and-aquatics.dive-computers.algorithm-conservatism-gas-setup-and-log-review
name: algorithm-conservatism-gas-setup-and-log-review
category: sports-recreation
field: water-sports-and-aquatics
product: dive-computers
tags: [dive-computer, dive-computers, decompression-algorithm, buhlmann, zhl-16c, gradient-factors, gf-low, gf-high, rgbm, vpm, conservatism, personal-adjustment, ndl, tts, time-to-surface, ceiling, deco-stop, safety-stop, ascent-rate-alarm, nitrox, fo2, ppo2, mod, gas-switching, multi-gas, air-integration, transmitter, cns-percent, otu, gauge-mode, freedive-mode, subsurface, shearwater-cloud, suunto-app, garmin-dive, dive-log, desat, no-fly-time, multilevel-planning]
level: practitioner
status: draft
description: "Using a dive computer properly: decompression models and gradient factors, conservatism settings, nitrox and multi-gas setup, air integration, reading NDL/TTS/ceiling, alarms, and reviewing logs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dive computers — algorithm, conservatism, gas setup and log review

**Goal:** have your computer set to the gas you're breathing and a
conservatism you chose deliberately, read it correctly underwater, and use the
log afterwards to dive better. Applies to wrist and console computers from
Shearwater, Suunto, Garmin, Mares, Scubapro, etc.; menu names differ by brand.

## 1. What the computer is computing
- It models nitrogen (and helium) uptake in theoretical tissue compartments
  from your depth/time profile and tells you how long you can stay (**NDL**) or
  what stops you need.
- **Algorithms:** **Bühlmann ZHL-16C** with **gradient factors** (common on
  Shearwater, Garmin, many technical computers); **RGBM** variants (Suunto,
  Mares historically — now Suunto offers Bühlmann too); proprietary models
  from other brands. Two brands can show different NDLs on the same dive.
  None is "correct" — they are models; DCS can occur within limits.

## 2. Conservatism settings
- **Gradient factors (GF low/GF high):** percentage of the original
  Bühlmann limit allowed. Lower numbers = more conservative. GF low affects
  first (deepest) stops; GF high affects surfacing and NDL. Common settings
  seen: **30/70** (conservative tech), **40/85**, **45/85**; recreational presets
  such as "Low/Med/High" map to GF pairs (check your manual).
- Other brands: "Personal adjustment" P0/P1/P2, "Conservative/Aggressive", altitude modes.
- **Be more conservative** for cold water, hard work, fatigue, age,
  dehydration, repetitive multi-day diving, or a past DCS hit.
- Set it on land and don't change it mid-trip without reason.

## 3. Gas setup
- **Set FO2 to the analysed mix** each dive (21 % for air). Wrong FO2 → wrong
  NDL and wrong oxygen warnings. Some computers reset to air after a period.
- **ppO2 limit:** usually 1.4 bar working, 1.6 bar for deco gas. The computer
  derives **MOD** and alarms beyond it.
- **Oxygen exposure:** **CNS %** and **OTU** track oxygen toxicity limits —
  watch it on multi-day nitrox trips.
- **Multi-gas (technical):** define each gas, switch depth and confirm the
  switch underwater; a missed or wrong switch corrupts the deco plan.
- **Air integration:** pair the transmitter to the computer before the dive;
  shows tank pressure and **gas time remaining** — verify readings against the
  SPG on the first dive.

## 4. Reading the screen underwater
- **NDL** counting down: plan your ascent before it reaches zero.
- If you enter deco: **ceiling** (don't go shallower), **stop depth/time** and
  **TTS** (time to surface including stops). Plan gas for TTS.
- **Ascent rate** bar/alarm — slow down when it flashes.
- **Safety stop** timer (3 min at ~5 m, usually optional but recommended).
- Ignore a "violation" lockout at your peril — some computers lock to gauge mode
  for 24–48 h after an omitted stop. That's a sign to stop diving and seek advice
  if any symptoms.

## 5. Practical habits
- Battery charged / replaced before a trip. Know the backlight and how to
  wake the screen.
- **One computer per diver**, worn all day on multi-dive days — swapping
  computers loses tissue loading history.
- Freediving: use a dedicated freedive mode; don't scuba and freedive on the same
  computer mode without understanding how it tracks.
- Altitude/fresh-water settings for lakes.
- **No-fly time** / desaturation shown after surfacing; follow DAN guidance.

## 6. Log review
Download to **Subsurface** (open source), **Shearwater Cloud**, Suunto app, Garmin
Connect etc. Check: ascent rate spikes, sawtooth profiles, time at depth, SAC
(with air integration), CNS %. Use your logged SAC to plan gas (see
sports-recreation.water-sports-and-aquatics.scuba-diving.buoyancy-gas-planning-and-buddy-checks).

## Verify
- [ ] Algorithm and conservatism setting known and written in your log.
- [ ] FO2 set to the analysed gas before every dive; ppO2 limit 1.4 working.
- [ ] Transmitter paired and checked against SPG.
- [ ] You can find NDL, ceiling, TTS and ascent rate on your screen.
- [ ] Logs downloaded and reviewed after each trip.

*Draft: algorithm availability per brand changes with firmware; check the
current manual. GF examples are common usage, not recommendations.*
