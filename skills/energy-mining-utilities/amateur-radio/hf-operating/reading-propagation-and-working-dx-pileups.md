---
id: energy-mining-utilities.amateur-radio.hf-operating.reading-propagation-and-working-dx-pileups
name: reading-propagation-and-working-dx-pileups
category: energy-mining-utilities
field: amateur-radio
product: hf-operating
tags: [hf-operating, amateur-radio, ham-radio, hf, shortwave, dx, dxing, dxpedition, pileup, split-operation, propagation, solar-flux, sfi, k-index, a-index, muf, gray-line, greyline, solar-cycle, band-conditions, 20m, 40m, 80m, 15m, 10m, dx-cluster, reverse-beacon-network, pskreporter, voacap, phonetics, ssb, logging, qsl, lotw, club-log, band-plan]
level: practitioner
status: gated
description: "Pick the right HF band for the time and solar conditions, use cluster and beacon tools to confirm openings, and break DX pileups politely with split operation, timing and clean phonetics."
sources:
  - "https://www.spaceweather.gov/noaa-scales-explanation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading propagation and working DX pileups on HF

**Goal:** be on the band that's open to where you want to reach, and get into a rare
station's log quickly without making the pileup worse. Stay within your licence's
frequency privileges and your region's band plan at all times.

## 1. Band choice by time and conditions
Rules of thumb (ionospheric conditions vary hugely by season and the solar cycle) (gated: unconfirmed, source is paywalled or blocked):
- **Higher bands (20 m, 17 m, 15 m, 12 m, 10 m)** open by day along sunlit paths and
  need ionisation; 10–15 m are best near solar maximum.
- **Lower bands (40 m, 80 m, 160 m)** come alive after dark and on paths in darkness;
  daytime absorption kills them for DX.
- **20 m** is the most reliable all-rounder for daytime and early-evening DX.
- **Gray line:** the sunrise/sunset terminator often gives enhanced low-band paths
  between stations both near it.
- Check the current solar-cycle state and forecasts at NOAA SWPC (spaceweather.gov) before planning; this skill does not state them.

## 2. Reading the space-weather numbers
- **Solar flux index (SFI):** higher = more ionisation, better high-band openings.
- **K-index** (Kp, 0–9, 3-hour geomagnetic disturbance): NOAA rates Kp 5 as a minor (G1) geomagnetic storm, Kp 6 G2, Kp 7 G3, Kp 8 (including 9-) G4 and Kp 9 G5; lower values are quieter.
These are hints. **Real evidence beats forecasts:** look at what's actually being
heard.

## 3. Confirm the opening
- **Reverse Beacon Network** (CW/RTTY skimmers) and **PSKReporter** (digital modes)
  show who hears whom right now. Call CQ briefly and see where you're spotted.
- **DX cluster** spots tell you who's on, where and in what mode.
- Propagation predictors (VOACAP and its web front ends) show likely paths and times
  for planning.
- Listen across the band: lots of distant signals = it's open.

## 4. Working a pileup
1. **Listen first.** Find out the DX's call, pattern and where they are listening.
   Rare stations often work **split**: transmit on one frequency, listen on another
   ("listening up 5 to 10"). Set your rig to split (VFO A receive / VFO B transmit)
   and *check it before transmitting*.
2. **Find the last station worked** in the split range (tune with your second VFO or
   SDR panadapter); the DX often tunes slowly in one direction. Call slightly ahead of
   that point.
3. **Call once, full call sign, standard phonetics** (ITU alphabet: Alfa, Bravo,
   Charlie...). Then listen. Don't call continuously over the DX.
4. If they reply with a partial call ("the Kilo Two?"), only stations matching
   respond.
5. Exchange is usually just the call and a signal report; keep it short. Confirm
   your call was copied correctly — log errors are common in pileups.
6. If the DX says "listening by number" or by region, wait for yours.

**Pileup manners (they make *you* get through faster too):** never transmit on the DX's
own frequency when they're working split ("tuning up" or asking "is he split?" there
causes chaos); don't act as a cop; don't call when it isn't your region; tune up into a
dummy load or off-frequency at low power.

## 5. Logging and confirmation
Log UTC time, frequency/band, mode, call, reports. Upload to **LoTW**, Club Log or
the DX's chosen QSL route; check their QSL info before sending a card.

## Verify
- [ ] Band chosen for time of day, path and current SFI/K-index.
- [ ] Opening confirmed by RBN/PSKReporter/cluster or by ear.
- [ ] Split set and checked; calling only in the DX's listening range.
- [ ] Called once with full call and phonetics, then listened.
- [ ] Contact logged in UTC; confirmation route checked.

## Checked

Date checked: 2026-10-25. Jurisdiction: International practice; frequency privileges follow the operator's own national licence.

Sources: https://www.spaceweather.gov/noaa-scales-explanation (versions: current eCFR and web pages as read on the date above).

Confirmed: NOAA Space Weather Scales: geomagnetic storm levels are based on Kp, with G1 = Kp 5, G2 = Kp 6, G3 = Kp 7, G4 = Kp 8 (including 9-) and G5 = Kp 9.

Gated: claims marked as gated were not confirmed. The band-choice rules of thumb, gray-line effect and SFI meaning come from operating manuals that were not read, and the solar-cycle timing and numeric SFI and A-index thresholds were removed because they could not be confirmed.

Method: documentation only; no commands were run.
