---
id: creative-arts.film-live-action.production-sound.wireless-and-rf-coordination
name: wireless-and-rf-coordination
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, production-sound-mixer, wireless, radio-mics, rf-coordination, frequency-coordination, wireless-coordination, frequency-scan, rf-scan, intermodulation, intermod, uhf, tv-band, dtv-channels, ofcom, fcc, pmse-licence, licence-exempt, 2-4ghz, lectrosonics, wisycom, sennheiser-ew, zaxcom, shure-axient, audio-ltd-a10, wireless-workbench, wisycom-manager, freqfinder, lectro-wireless-designer, antenna-distribution, antenna-placement, sharkfin, dipole, lpda, diversity, rf-dropouts, squelch, transmitter-gain, tx-gain, tx-power, companding, digital-hybrid, encryption, ifb, comtek, camera-hop, video-village-rf, 5ghz-video, scanning-tools, rf-explorer, wireless-workbench-use, wireless-designer-use, antenna-systems, rf-licensing, rf-troubleshooting, dropout-diagnosis]
level: practitioner
status: draft
description: "Keep wireless mics clean all day: scan and coordinate intermod-free frequencies, licences and TV-band rules, antenna distribution and placement, TX gain and power, sharing spectrum with video."
sources:
  - "https://www.lectrosonics.com/support (Lectrosonics - Wireless Designer, frequency coordination guides)"
  - "https://www.wisycom.com/ (Wisycom Manager and RF best practice)"
  - "https://www.ofcom.org.uk/spectrum/pmse (Ofcom PMSE licensing - UK)"
  - "https://www.fcc.gov/wireless-microphones (FCC wireless microphone rules - US)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wireless and RF coordination

**Goal:** six to twelve radio mics, a camera hop, IFBs and the video village's
transmitters all working in the same building without a hit on a take - because the
spectrum was planned, not hoped for.

## 1. Know the rules where you are
- **UHF TV band** (470-694 MHz Europe / 470-608 MHz US after the 600 MHz repack):
  the home of pro wireless. Many ranges need a **licence**: UK **Ofcom PMSE** (shared
  Ch 38 606-614 MHz licence, or coordinated per-location licences for other channels);
  US **FCC Part 74** (licence eligible for productions; unlicensed use allowed at ≤50 mW
  in specified spaces away from active TV channels; the 600 MHz band is off-limits).
  Licence-free pockets exist (UK 863-865 MHz, US 902-928 MHz ISM for some systems) but
  are crowded.
- Each country's DTV channel map differs: a Lectrosonics block that is clean in LA is on
  top of a broadcaster in London. Check the local TV channel allocation before travel
  and bring the right blocks/receivers.
- **2.4 GHz** systems (consumer and some pro) share with Wi-Fi/Bluetooth - fine for a
  one-person interview, not for drama.

## 2. Scan, then coordinate
1. **Scan** at the location, at the time of shooting, with the receivers (Lectrosonics
   SmartTune / Wisycom scan / Sennheiser EW-DX scan) or a dedicated scanner (RF Explorer);
   import into **Wireless Workbench** (Shure), **Wireless Designer** (Lectro), **Wisycom
   Manager**, **FreqFinder** or **Sound Devices' Freq Assist**. The scan shows active DTV
   channels and other users.
2. **Coordinate**: let the software compute an **intermodulation-free** set (3rd/5th-order
   products of your own transmitters must not land on your own frequencies) with spacing
   ≥ 300-400 kHz; include **every** transmitter on set in the calculation - IFB, camera
   hops, timecode (Tentacle 2.4 GHz is fine), the DIT's/video village's wireless video
   (5 GHz, separate band), stunt comms, and other units' systems.
3. Program frequencies to TX/RX (IR sync or app); label channel plan; record it on the
   sound report.
4. Re-scan after company moves and in the afternoon (broadcasters and other users
   come and go).

## 3. Antennas and distribution
- Receivers' whips are a compromise; use an **antenna distribution system** (Lectro
  UMC/ Wisycom/ Shure UA844) with two **directional antennas** (sharkfin/LPDA) or
  dipoles on a mast, **2-3 m high**, line of sight to the actors, spaced ≥ 1 m apart
  for diversity. Angle sharkfins toward the set; keep antennas away from metal,
  bodies and LED walls.
- Coax: low-loss (RG8X/LMR-240) short runs; use RF amplifiers only with long cable
  runs and never to "boost" a weak signal - amplify noise too.
- On a bag: whips vertical, receivers at the top of the bag, body away from the
  actors' side.
- Separate antenna systems (or at least separation and filtering) for IFB transmitters
  near receive antennas: your own IFB TX is the loudest thing in the room.

## 4. Transmitter setup
- **TX gain**: set with the actor at performance level so the TX's modulation meter
  peaks near full without "clipping/limiter" indication (Lectro: -20 dB headroom;
  Wisycom/Sennheiser show an AF peak). Too low = hiss, too high = TX limiter distortion
  that no fader fixes.
- **TX power**: lowest that gives clean reception (50 mW indoors; 100-250 mW for
  distance/exteriors); more power raises intermod with your other TXs.
- **Encryption** on for sensitive sets (digital systems); **companding/digital hybrid**
  modes matched TX-RX.
- Battery discipline: fresh/charged at call, change at lunch; mark used cells.
- Keep TX antennas away from each other on the body (two lavs on one actor: separate
  pockets) and away from mobile phones (actors' phones in flight mode).

## 5. Diagnosing hits
Dropouts with full RF bars = intermod or a strong adjacent user - move frequency.
Dropouts with low RF = distance/shadowing - move antennas or raise power. Hiss =
TX gain low or **squelch** too open. Buzzing synced to lights = dimmers/LED drivers
radiating - distance, or use a different block. Record the hits per take for post and
offer a wild line if a key line was hit.

## Gotchas
- Coordinating only the radio mics and forgetting the camera hop and IFBs.
- Receivers on the bag's bottom under batteries and metal.
- Sharkfins pointed at the sky; or two antennas six inches apart.
- Using a block that overlaps the local TV channel; perfect in the morning, hits at 3 p.m. when the broadcaster ramps power.
- No licence; Ofcom/FCC enforcement and a shut-down on a big day.

## Verify
- [ ] Local band plan checked and licence held; blocks match the country.
- [ ] Scan at location, intermod-free coordination including hops/IFB; channel plan recorded.
- [ ] Antenna distribution with directional antennas raised, spaced and aimed.
- [ ] TX gain and power set per actor; batteries fresh at call and lunch; re-scan after moves.
