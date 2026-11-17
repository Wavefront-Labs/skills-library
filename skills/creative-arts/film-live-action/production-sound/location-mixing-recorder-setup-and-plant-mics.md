---
id: creative-arts.film-live-action.production-sound.location-mixing-recorder-setup-and-plant-mics
name: location-mixing-recorder-setup-and-plant-mics
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, production-sound-mixer, sound-mixer, location-mixing, recorder-setup, mixer-setup, sound-devices, 833, 888, scorpio, mixpre, mixpre-10, zoom-f8n, zaxcom-nova, cantar, gain-staging, trim-gain, fader, limiter, high-pass-filter, iso-tracks, mix-track, l-r-mix, pre-fade, post-fade, bus-routing, sample-rate, 48k, 24-bit, 32-bit-float, poly-wav, timecode-in, timecode-out, cart, bag, plant-mics, plant-mic, hidden-mics, car-interior, vehicle-recording, lav-plants, boundary-mic, pzm, dpa-4060, dpa-4061, cos-11, comtek, ifb, headphones, monitoring-mix, recorder-routing, track-arming, gain-structure, limiter-settings, plant-mic-placement, bag-vs-cart, recorder-file-formats, poly-vs-mono, vehicle-interior-recording]
level: practitioner
status: draft
description: "Set up and mix a location sound bag or cart: recorder routing with ISOs and a mix track, gain staging and limiters, timecode and IFB feeds, and planting hidden mics in sets and vehicles."
sources:
  - "https://www.sounddevices.com/support/ (Sound Devices 833/888/Scorpio/MixPre user guides)"
  - "https://www.amps.net/ (Association of Motion Picture Sound - location sound guidance)"
  - "https://cinemaaudiosociety.org/ (Cinema Audio Society resources)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Location mixing: recorder setup and plant mics

**Goal:** every microphone recorded clean on its own track with a usable mix for the
editor, levels that never clip and never need rescuing, and a set-up that is rebuilt
identically every morning.

## 1. Recorder/mixer configuration (once per show)
On a Sound Devices 833/888/Scorpio (MixPre/Zoom/Zaxcom similar):
- **Sample rate 48 kHz, 24-bit** (32-bit float only if post agrees; it removes clipping
  risk but doubles file size and not all NLEs/DAWs handle it cleanly), **poly WAV**,
  BWF with **iXML**.
- **Tracks**: ISO per input (boom, each lav, plant) **pre-fade** (raw, safety) and a
  stereo or mono **mix track** (L/R or Mix) **post-fade** - the editor cuts with the
  mix; post uses ISOs. Name tracks (`BOOM`, `LAV MARTA`, `PLANT CAR`) - names go into
  iXML and the sound report.
- **Inputs**: mic/line, 48 V phantom for condensers (boom, DPA via adapter), none for
  wireless receivers (line level), **high-pass** 80-120 Hz on dialogue (higher in wind),
  **limiters** on per channel (threshold ~ -6 dBFS, linked for stereo pairs) as
  insurance, not as a tool.
- **Timecode**: free run/time of day, 25/24/23.976 per project, jam the camera(s) and
  slate from the recorder (or from a master Tentacle/Ambient lockit); check sync in
  the morning, after lunch, and after any power cycle.
- **Outputs**: L/R to camera (scratch, via wireless hop) and to **IFB/Comtek** for
  director/script/boom op; headphone output for the mixer. Save the whole thing as a
  **setup file** on the SD card and restore it each day.
- Media: dual-record to SD + SSD/CF; format daily after confirmed offload by the DIT.

## 2. Gain staging
- **Trim** (input gain) sets the ISO level: speak at performance level, aim for peaks
  around **-20 to -12 dBFS** with headroom; shouting scenes -6 dBFS peaks max. Set
  trims in rehearsal, then leave them - trim changes mid-take change the ISO.
- **Faders** shape the **mix** only; ride the boom up for the line, lav down when the
  boom is on-axis (or the reverse), avoid "phasey" doubling by keeping one mic dominant
  per line (3-6 dB difference).
- Headphones: monitor the mix normally; solo (PFL) each ISO regularly for noise
  (clothing rustle, RF hits, wind) - the ISO is what post uses.
- Noise floor: keep the preamp doing the work; low trim + high fader means hiss.

## 3. Bag vs cart
**Bag** (833/MixPre + 4-6 wireless, run-and-gun, docs, small drama): batteries (NP-F/
L-mount, a distribution box), antenna on a mast, a wireless hop to camera.
**Cart** (888/Scorpio/Cantar, drama/multi-cam): mains/big batteries, antenna
distribution, a monitor for video, a boom op and a 2nd AS running wireless and plants.
Either way: a **channel plan** on paper, labelled cables, spare of everything.

## 4. Plant mics
Hidden mics where a boom can't reach or a lav can't be worn:
- **Choice**: DPA 4060/4061/4071, Sanken COS-11, Countryman B6 (tiny omnis) or a
  boundary/PZM (Crown, DPA 4097) on a flat surface; small cardioids (Schoeps CCM41,
  Sennheiser MKH 50) in a plant for directionality. Feed them into a wireless TX with
  a lav input, or run cable where practical.
- **Placement**: within ~1 m of the mouth, pointed at it (for directionals), hidden in a
  flower vase, behind a monitor, on the sun visor/headliner/dashboard in cars, in a
  pillow, under a table lip, inside a lampshade. Use **Rycote Undercovers/Overcovers**,
  tape/putty to stop rattle, foam to decouple from vibrating surfaces.
- **Vehicles**: visor plants (one per seat row) plus lavs on the actors; car "hop" TX
  recorder in the boot (MixPre-3 or Zaxcom with its own TC) if the cart can't follow; the
  process trailer carries the mixer on the tray; shut engine/AC when the script allows;
  wild tracks of engine/road for post.
- **Scenes at a table**: a boundary mic in the centre plus a boom from the top; plants
  under the table edge catch overlapping dialogue the boom misses.
- Record plants on their own ISO; label them; note positions on the sound report.

## 5. Communication
Agree with the 1st AD when "roll sound" happens (sound rolls first, then camera);
state "speed" clearly. Tell the DP/gaffer early about hum from dimmers/LED ballasts
and the AD about generators and HVAC - they can only fix what they hear about before
the take. Deliver sound reports with the media every day.

## Gotchas
- Limiter used as the level control; the ISOs are squashed and pumpy.
- Mix track only, no ISOs ("to save space"); post cannot separate overlapping lines.
- Phantom power sent to a wireless receiver line input; noise or damage.
- Plants unlabelled: the editor hears a great track and nobody knows which mic.
- Timecode jammed once at 7 a.m.; cameras power-cycled at lunch and drift 3 frames.

## Verify
- [ ] Recorder setup file saved: 48k/24-bit poly WAV, ISOs pre-fade, mix post-fade, tracks named.
- [ ] Trims set in rehearsal for -20 to -12 dBFS peaks; limiters as safety only.
- [ ] Timecode jammed and re-checked after lunch; IFB/scratch feeds working.
- [ ] Plant mics placed, decoupled, isolated on their own tracks and noted on the report.
