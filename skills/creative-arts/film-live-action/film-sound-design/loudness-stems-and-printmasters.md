---
id: creative-arts.film-live-action.film-sound-design.loudness-stems-and-printmasters
name: loudness-stems-and-printmasters
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, re-recording-mixer, loudness, lufs, lkfs, true-peak, dbtp, ebu-r128, atsc-a85, bs-1770, dialogue-gated, dialnorm, leq-m, leq-m-85, trailer-loudness, netflix-sound-spec, amazon-sound-spec, apple-sound-spec, loudness-range, lra, stems, dme, dx-mx-fx, printmaster, printmasters, m-and-e, music-and-effects, optional-stem, fully-filled-me, audio-deliverables, delivery-spec, track-layout, smpte-channel-order, film-channel-order, l-r-c-lfe-ls-rs, 5-1-layout, 7-1-layout, atmos-adm, adm-bwf, iab, dcp-audio, broadcast-wav, poly-wav-delivery, sample-rate-48k, 24-bit, mix-qc, loudness-report, loudness-standards, platform-loudness, stem-layouts, stem-naming, me-creation, fully-filled, printmaster-versions, dialogue-gated-measurement, true-peak-limiting, audio-deliverables-list, audio-qc]
level: practitioner
status: draft
description: "Deliver sound that passes QC: loudness standards (R128, A/85, dialogue-gated streamer specs), stems and printmasters with correct channel orders, a fully-filled M&E, ADM BWF for Atmos."
sources:
  - "https://tech.ebu.ch/publications/r128 (EBU R128 loudness normalisation)"
  - "https://www.atsc.org/ (ATSC A/85 recommended practice)"
  - "https://partnerhelp.netflixstudios.com/ (Netflix sound delivery specifications)"
  - "https://professional.dolby.com/ (Dolby Atmos ADM BWF and printmaster guidelines)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loudness, stems and printmasters

**Goal:** a delivery package that a broadcaster, streamer or DCP facility accepts first
time: the right loudness by the right measurement, stems that sum to the printmaster,
an M&E that works for any language, and files whose channel order nobody has to guess.

## 1. Loudness - which measurement
All modern specs use **ITU-R BS.1770** (LKFS/LUFS, K-weighted) but differ in gating and target:
| Spec | Target | True peak | Notes |
|---|---|---|---|
| **EBU R128** (EU/UK broadcast) | -23 LUFS integrated (±1), LRA often ≤ 20 LU | -1 dBTP | Programme-wide, gated at -70/-10 relative |
| **ATSC A/85** (US broadcast) | -24 LKFS (±2), dialnorm set to match | -2 dBTP | Dialogue-anchored in practice |
| **Netflix** | -27 LKFS **dialogue-gated** (±2) | -2 dBTP | Measured on dialogue only (Dolby Dialogue Intelligence); 5.1 and 2.0 both |
| **Amazon / Apple TV+ / Disney+** | Similar -24/-27 dialogue or integrated per spec; check the current doc | -2 dBTP | Each has its own version; specs change yearly |
| **Theatrical** | No normalisation; mixed at 85 dB C | n/a | Trailers limited by **Leq(m) 85** (TASA) |
| **Web/social** | -14 to -16 LUFS integrated | -1 dBTP | Platforms normalise down, not up |
Measure the **whole programme** (not a scene), on the delivered printmaster, with a
compliant meter (Nugen VisLM, iZotope Insight, Dolby Media Meter, Fairlight/Pro Tools
built-ins). Dialogue-gated specs need a meter that supports speech gating. Record the
numbers in the delivery report.

## 2. Hitting the target without wrecking the mix
Adjust overall level to the target (a stem-wide offset is fine if dynamics are
right); reduce **true-peak** excursions with a transparent limiter at -1/-2 dBTP only
on the last pass; if LRA is too high for TV, compress gently on stems (dialogue less,
FX/MX more) and re-check. Never normalise a theatrical printmaster to -24 and call it
the TV mix - re-balance dialogue up and LFE down for small rooms.

## 3. Channel orders and formats
- **SMPTE/ITU order** (most file-based delivery): `L R C LFE Ls Rs` (5.1); `L R C LFE
  Lss Rss Lsr Rsr` (7.1). **Film order** (`L C R Ls Rs LFE`) still appears in older
  Pro Tools sessions and some DCP houses - state the order in the filename and the
  delivery note; mislabelled C/LFE is the most common QC fail.
- Files: 48 kHz, 24-bit **BWF** (poly or mono-per-channel `_L`, `_R`, `_C`, `_LFE`,
  `_Ls`, `_Rs` suffixes); start at the reel's timecode with a 2-pop; identical lengths
  for every stem of a reel.
- **Atmos**: deliver the **ADM BWF** (Dolby Atmos master as a single WAV with beds and
  objects + metadata) plus the 7.1/5.1/2.0 **re-renders** from the Atmos Renderer; for
  DCP, the **IAB** (Immersive Audio Bitstream) MXF; for streaming, ADM or Dolby Atmos
  MP4 (via Dolby encoders). Also provide the binaural re-render if asked.
- **Stereo**: LoRo (plain stereo downmix) for most; LtRt (matrix-encoded) only when
  specified.

## 4. Stems and the M&E
- **DME stems** (Dialogue, Music, Effects) per format, summing to the printmaster
  (within ~0.5 dB); often also **separate stems**: DX, ADR/group, FX, BGs, Foley,
  Score, Source.
- **M&E (music and effects)**: the full mix minus dialogue - **fully filled** (all
  foley, all effects that were covered by dialogue, backgrounds through the dialogue
  gaps) so a foreign dub drops in. Include an **optional stem** (`OPT` or `DX FX`):
  dialogue-dependent sounds (English-language crowd walla, singing, efforts/breaths
  that a dub may or may not replace) kept separate; and the **dialogue stem** itself
  for reference. Some specs want "M&E with opt mixed in" and "M&E without".
- Check the M&E by playing it with the dialogue stem muted: any hole (a glass set down
  that was only on the production track) is a fix before delivery.
- Printmasters per format: `5.1`, `7.1`, `2.0 LoRo`, `2.0 LtRt`, near-field variants,
  descriptive-audio version if ordered, **TV mix** with narrower dynamics.

## 5. The package
`SHOW_Rn_5.1_PRINTMASTER_24b48k_SMPTE.wav`, stems and M&E with the same naming, a **PDF
delivery note** (formats, channel order, timecode start, 2-pop, loudness measurements
per file with meter used, LRA, true peak, sample rate/bit depth, Atmos renderer
version), and a QC log (listened start to end, no clicks/dropouts, sync to picture at
head/tail). Checksums (MD5/xxHash) with the files.

## Gotchas
- Integrated loudness correct, dialogue-gated wrong (quiet dialogue under loud FX) - fails Netflix.
- Film order files labelled SMPTE: LFE in the centre speaker.
- M&E with a dialogue-covered door missing; dub house sends it back.
- True peak measured as sample peak; inter-sample overs clip on consumer decoders.
- Stems that don't sum to the printmaster because the final limiter was only on the mix bus.

## Verify
- [ ] Loudness and true peak measured on each printmaster with the spec's gating; numbers in the delivery note.
- [ ] Channel order stated and verified by soloing C and LFE; stems same length and TC as the printmaster.
- [ ] M&E fully filled; optional stem separated; checked with dialogue muted.
- [ ] Atmos ADM/IAB plus re-renders delivered where ordered; checksums and QC log included.
