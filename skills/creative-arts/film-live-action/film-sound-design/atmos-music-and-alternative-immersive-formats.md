---
id: creative-arts.film-live-action.film-sound-design.atmos-music-and-alternative-immersive-formats
name: atmos-music-and-alternative-immersive-formats
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, atmos-music, immersive-formats, auro-dts, dolby-atmos-music, spatial-audio, adm-bwf, binaural-render-mode, auro-3d, dts-x, sony-360-reality-audio, ambisonics, immersive-audio]
level: advanced
status: draft
description: "Mix music in Dolby Atmos for streaming (bed/object choices, binaural render modes, ADM masters, loudness) and know where Auro-3D, DTS:X, 360 Reality Audio and ambisonics differ."
sources:
  - "https://professional.dolby.com/music/ (Dolby - Atmos Music creation and delivery)"
  - "https://www.auro-3d.com/ (Auro Technologies - Auro-3D formats)"
  - "https://dts.com/dtsx/ (Xperi/DTS - DTS:X object-based audio)"
  - "https://www.sony.com/en/360RA/ (Sony - 360 Reality Audio)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Atmos for music and alternative immersive formats

**Goal:** an immersive music master (album track, soundtrack album, concert film) that
works on speakers and the far more common headphone (binaural) playback, delivered in
the format the platform needs.

## 1. Atmos music vs Atmos film
- Same renderer, same beds + objects model, ADM BWF master. Different priorities:
  most listeners hear **binaural on headphones** or a soundbar, not a 7.1.4 room.
- Monitor on speakers (7.1.4 is the Dolby music reference) **and** check the binaural
  render constantly.

## 2. Bed vs object decisions
- **Bed (7.1.2)**: reverbs, pads, wide stereo elements that should stay anchored.
- **Objects**: lead vocal (often a centred object or bed-centre plus phantom), solo
  instruments placed with intent, height elements, moving effects.
- Keep the lead vocal stable and present; immersive placement is not an excuse to bury it.
- Low end: keep bass and kick firm in the front; use LFE sparingly.

## 3. Binaural render mode
Each bed/object has a **binaural render mode** (Off, Near, Mid, Far) in the renderer
metadata. Vocals and bass often Off/Near to stay dry and centred; ambience Mid/Far.
This only affects headphone playback, so audition with headphones while setting it.

## 4. Delivery
- **ADM BWF** master from the renderer, 48 kHz/24-bit, plus a stereo master that matches.
- Loudness: Dolby's music guidance is around -18 LKFS integrated with -1 dBTP true peak
  for streaming Atmos (confirm the current distributor/platform spec).
- Platforms re-encode to Dolby Digital Plus JOC/AC-4; check the encoded result with
  Dolby's tools if available.

## 5. Other immersive formats
- **Auro-3D**: channel-based height layers (e.g. 9.1, 11.1, 13.1), with an upmixer
  (Auro-Matic); used in some cinemas and Blu-ray music releases.
- **DTS:X**: object-based cinema/home format, similar concepts to Atmos; IMAX Enhanced
  uses a DTS:X variant at home.
- **Sony 360 Reality Audio**: object-based music format (MPEG-H) with its own creation
  tools, aimed at headphones and specific speakers.
- **Ambisonics** (first/higher order): scene-based, used for VR/360 video and as a
  source for binaural rendering.
Confirm which format each distributor accepts before mixing; conversions between
formats are rarely lossless in intent.

## Gotchas
- Mixing only on speakers: binaural playback sounds phasey and distant.
- Everything as moving objects: gimmicky, tiring, unstable vocal.
- Stereo and Atmos versions that differ in arrangement or level - platforms flag it.
- Loudness measured on the stereo fold-down instead of the Atmos master.

## Verify
- [ ] Checked on 7.1.4 (or available speaker layout) and headphones.
- [ ] Binaural render modes set on purpose per element.
- [ ] ADM master and stereo master match in content.
- [ ] Loudness/true peak meet the platform spec.
