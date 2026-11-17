---
id: energy-mining-utilities.amateur-radio.vhf-uhf-operating.repeater-procedure-and-fm-satellite-passes
name: repeater-procedure-and-fm-satellite-passes
category: energy-mining-utilities
field: amateur-radio
product: vhf-uhf-operating
tags: [vhf-uhf-operating, amateur-radio, ham-radio, vhf, uhf, 2m, 70cm, repeater, repeater-offset, ctcss, pl-tone, dcs, courtesy-tone, timeout-timer, simplex, handheld, ht, mobile-radio, station-identification, amateur-satellite, fm-satellite, iss-repeater, amsat, doppler-shift, gpredict, heavens-above, arrow-antenna, yagi, grid-square, maidenhead, cross-band, full-duplex]
level: intro
status: gated
description: "Use VHF/UHF repeaters properly (offset, CTCSS tone, pauses, ID) and work an FM amateur satellite pass with a handheld: predicting passes, Doppler tuning, short exchanges."
sources:
  - "https://www.arrl.org/band-plan"
  - "https://www.ecfr.gov/current/title-47/part-97/section-97.119"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repeater procedure and FM satellite passes

**Goal:** get through a local repeater cleanly and sound like you belong, then step up
to contacts hundreds or thousands of kilometres away through an FM satellite using
only a handheld and a small beam. Offsets, tones and ID rules below are common
defaults; your licence conditions and local repeater directory are authoritative.

## 1. Programming for a repeater
A repeater listens on one frequency (its input) and retransmits on another (its
output). You need:
- **Output frequency** (what you receive).
- **Offset and direction** to its input. Common defaults: 2 m ±600 kHz (US; Europe
  usually −600 kHz (gated: unconfirmed, source is paywalled or blocked)); 70 cm +5 MHz in the US, −7.6 MHz in much of IARU Region 1 (gated: unconfirmed, source is paywalled or blocked).
  **Check the directory**: many repeaters are non-standard.
- **Access tone** (CTCSS/"PL" sub-audible tone, or DCS) — without it, the repeater
  ignores you. Some use 1750 Hz tone-burst (older European practice) (gated: unconfirmed, source is paywalled or blocked).
- Use the **reverse** button to listen on the input: if you can hear the other
  station directly, move to a simplex frequency and free the repeater.

## 2. On-air procedure
- **Listen first** for a while; someone may be mid-conversation.
- To join: say your call sign once ("G4XYZ" / "W1XYZ listening"). Avoid "CQ" on FM
  repeaters; it's not the norm in most places.
- **Key up, wait a second, then speak.** Repeaters and tone decoders need a moment;
  otherwise your first word is lost.
- **Pause between overs** (wait for the courtesy tone, if used) so others can break
  in, especially for emergency traffic. "Break" or a call sign in the gap means let
  that station in.
- Keep overs short: a **timeout timer** (often a few minutes) will cut you off.
- **Identify** at the intervals your licence requires (US, 47 CFR 97.119(a): at least every 10 minutes
  and at the end) and at the end of a contact.

## 3. Working an FM satellite pass
FM satellites act like a repeater in orbit: uplink usually on 2 m, downlink on 70 cm
(or the reverse). Which satellites are operational changes often — **check AMSAT's
current status page before planning; any named bird may be off-line.** The ISS
cross-band FM repeater is a well-known option when active.
1. **Predict passes** with an app or program (e.g. Gpredict, Heavens-Above, AMSAT
   pass predictor). Passes last about 10–15 minutes (gated: unconfirmed, source is paywalled or blocked); higher maximum elevation = better.
2. **Antenna:** a small handheld dual-band Yagi (an "Arrow"-type) makes a huge
   difference over a rubber-duck antenna. Point it along the predicted track; rotate
   it to fight polarisation fading.
3. **Doppler:** the 70 cm downlink appears up to about ±10 kHz off nominal (gated: unconfirmed, source is paywalled or blocked). Pre-
   program memories in ~5 kHz steps: start high as it rises, step down through the
   pass. The 2 m uplink shift is smaller; many operators leave it fixed.
4. **Full duplex helps:** if your radio can, listen to the downlink while
   transmitting to hear yourself coming through. Otherwise use headphones and listen
   between transmissions.
5. **Exchange:** call signs and **Maidenhead grid square**, nothing more:
   "W1XYZ, FN42". Many stations share a few minutes; one or two contacts per pass is
   polite, and don't call over others.
6. Log time (UTC), satellite, call, grid.

## Gotchas
- Wrong or missing CTCSS is the number-one "repeater's dead" cause.
- Power: use the minimum that works; high power on a busy satellite captures it
  unfairly and doesn't help much.
- A satellite pass passes; practise antenna handling with an outdoor dry run first.

## Verify
- [ ] Repeater memory has correct output, offset direction and tone; reverse checked.
- [ ] Key-pause-speak habit; pauses between overs; ID at required intervals.
- [ ] Satellite confirmed active; pass predicted with elevation and timings.
- [ ] Doppler memories programmed; antenna pointed and rotated during the pass.
- [ ] Exchange short with grid square; contact logged.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (47 CFR 97.119; ARRL band plan); other regions noted as unconfirmed.

Sources: https://www.arrl.org/band-plan; https://www.ecfr.gov/current/title-47/part-97/section-97.119 (versions: current eCFR and web pages as read on the date above).

Confirmed: 47 CFR 97.119(a): identify at least every 10 minutes during a communication and at its end. The ARRL band plan lists 2 m repeater inputs and outputs 600 kHz apart (146.01-146.37 in, 146.61-146.97 out) and 70 cm repeater segments 442-445 and 447-450 MHz, which are 5 MHz apart; the page does not state the offsets in words.

Gated: claims marked as gated were not confirmed. The IARU Region 1 offsets, 1750 Hz tone burst, Europe 2 m direction, pass length and Doppler range come from sources that were not fetched.

Method: documentation only; no commands were run.
