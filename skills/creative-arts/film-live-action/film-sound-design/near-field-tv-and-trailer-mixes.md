---
id: creative-arts.film-live-action.film-sound-design.near-field-tv-and-trailer-mixes
name: near-field-tv-and-trailer-mixes
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, near-field, tv-mix, trailer-mix, home-entertainment-mix, nearfield-remix, dynamic-range, dialogue-gated-loudness, ebu-r128, atsc-a85, tasa, leq-m, streaming-loudness, downmix]
level: advanced
status: draft
description: "Derive near-field home, TV and trailer mixes from a theatrical mix: reducing dynamic range, lifting dialogue, hitting streaming or broadcast loudness, and trailer Leq(m) limits."
sources:
  - "https://tech.ebu.ch/publications/r128 (EBU R 128 - loudness normalisation)"
  - "https://www.atsc.org/ (ATSC A/85 - Techniques for Establishing and Maintaining Audio Loudness for Digital Television)"
  - "https://partnerhelp.netflixstudios.com/ (Netflix Partner Help Center - audio mix specifications)"
  - "https://www.tasatrailers.org/ (Trailer Audio Standards Association)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Near-field, TV and trailer mixes

**Goal:** the film sounds right everywhere it is sold: a theatrical mix for 85 dB
cinemas, a near-field version for living rooms, broadcast-compliant TV versions and
trailers that pass the cinema's loudness rules.

## 1. Why a theatrical mix fails at home
Mixed in a large calibrated room, quiet dialogue and huge peaks play fine. At home
(lower playback level, noisy room, small speakers) dialogue disappears and explosions
are too loud - the "remote control ride".

## 2. Near-field (home entertainment) remix
- Recalibrate the room to the near-field reference (small-room level) and play the
  theatrical stems.
- **Lift dialogue** relative to music and effects, mostly in quiet scenes; ride rather
  than compress the whole mix.
- **Reduce dynamic range**: gentle stem compression on MX/FX peaks, trim the loudest
  moments, keep the intent.
- Surrounds and LFE: home systems vary; reduce extreme surround-only and sub-only content.
- Check the **downmix** (5.1/7.1 to stereo) - streaming often plays a downmix.

## 3. Loudness targets (confirm in the current spec)
- Streaming: e.g. Netflix specifies dialogue-gated loudness (-27 LKFS +/-2) and a
  true-peak ceiling (-2 dBTP).
- Broadcast: EBU R 128 -23 LUFS integrated (Europe), ATSC A/85 -24 LKFS (US), with
  true-peak limits; measure the whole programme.
- Measure on the delivered format and channel count.

## 4. TV mix (broadcast/airline versions)
- Same tools as near-field, tighter range and the broadcaster's loudness.
- Airline/TV edits: muted or replaced lines (profanity), recut scenes; keep stems so
  edits don't need a full remix.

## 5. Trailer mix
- Trailers are mixed hot and punchy but cinemas enforce **TASA**-style limits:
  measured in Leq(m) (a Dolby Model 737-style meter), with an 85 Leq(m) maximum for
  trailers in TASA member cinemas.
- Online trailers: platform loudness normalisation applies (YouTube, for example, turns
  loud uploads down to about -14 LUFS); a separate online master avoids squashed or turned-down audio.
- Deliver trailer stems (DX/MX/FX) for international versions.

## Gotchas
- Just normalising the theatrical mix to -24/-27: dialogue still lost in quiet scenes.
- Compressing the printmaster instead of stems: pumping, stems no longer sum.
- Measuring loudness on the stereo downmix for a 5.1 deliverable.
- Trailers over the Leq(m) limit get turned down by projectionists, losing impact.

## Verify
- [ ] Near-field mix checked at home level on TV speakers.
- [ ] Loudness and true peak meet each version's spec on the delivered format.
- [ ] Downmix checked for dialogue and phase.
- [ ] Trailer measured in Leq(m) under the limit; online master separate.
