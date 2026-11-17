---
id: creative-arts.film-live-action.film-sound-design.premix-and-the-re-recording-mix
name: premix-and-the-re-recording-mix
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, re-recording-mixer, final-mix, premix, premixing, mix-stage, dubbing-stage, dubbing-theatre, dialogue-premix, effects-premix, music-premix, foley-premix, predubs, stems, printmaster, mix-in-the-box, dolby-atmos-mix, 5-1-mix, 7-1-mix, stereo-mix, near-field-mix, theatrical-mix, calibration-85db, reference-level, x-curve, mix-notes, playback-sessions, director-mix-review, panning, lfe, dialogue-intelligibility, dynamic-range, loudness-range, cinema-vs-tv-mix, downmix, fold-down, mix-schedule, pro-tools-mix, avid-s6, dialogue-premixing, music-balance, music-vs-dialogue, mix-panning, perspective-mix, mix-playback, mix-fixes, stage-calibration, monitoring-level]
level: practitioner
status: draft
description: "Run the mix: premix dialogue, effects, foley and music into stems, then the final on a calibrated stage - dialogue-first balance, panning and LFE rules, director playbacks, printmasters per format."
sources:
  - "https://cinemaaudiosociety.org/ (Cinema Audio Society - re-recording mixing craft)"
  - "https://www.mpse.org/ (Motion Picture Sound Editors)"
  - "https://professional.dolby.com/ (Dolby - theatrical mix room calibration and Atmos mixing guidelines)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Premix and the re-recording mix

**Goal:** hundreds of tracks become a handful of stems and then one mix that tells the
story at every level - in a room calibrated so what you hear is what the audience
will, and in a schedule that survives the director's notes.

## 1. Structure of the mix
- **Premixes (predubs)**: each editorial department's tracks are balanced, EQ'd,
  cleaned and panned into a manageable set of **stems**: `DX` (dialogue, often split
  dialogue/ADR/group), `FX` (hard effects, backgrounds, design), `FOL` (foley), `MX`
  (music, split score/source). Premixing happens over days, often with the department's
  editor present; it's where 80% of the work is.
- **Final mix**: the re-recording mixer(s) (traditionally one on dialogue/music, one on
  effects) balance the stems against each other reel by reel with the director, then
  fine-tune.
- **Printmasters**: the final per format (5.1, 7.1, Atmos, stereo LtRt/LoRo, near-field
  TV) printed from the stems with any format-specific trims.
Keep everything **stem-based and automated** so a change to one line of dialogue in
week 3 doesn't mean remixing a reel.

## 2. The room
Theatrical stages are calibrated to **85 dB C SPL at the mix position for -20 dBFS
pink noise per channel** (surrounds 82 dB, LFE +10 dB in-band), with the **X-curve**
room EQ for large rooms; near-field/TV rooms use 79-82 dB and a flat response.
Mixing in an uncalibrated room produces a mix that is wrong everywhere else. Set the
monitor level once and never mix "a bit louder" for the client.

## 3. Dialogue first
- Level and consistency of **dialogue** anchors the mix; everything else is placed
  relative to it. Target theatrical dialogue around -27 to -24 dBFS average (LKFS
  dialogue-gated ~ -27 for streaming specs), with the loudest shouts leaving headroom.
- EQ for intelligibility (presence 2-5 kHz, roll low rumble), gentle compression
  (2:1-3:1), de-essing, and **matching across cuts** (the dialogue editor's split
  tracks give you per-mic EQ). Noise reduction already done in the edit; the mixer
  only touches what the stage reveals.
- Room reverb/perspective: match reverb to shot size and space; ADR gets the
  production's room via convolution/impulse responses; **futz** (phone, radio) via EQ/
  distortion plug-ins with the clean line underneath for later.
- Keep dialogue centred (C channel) in theatrical mixes; pan only for off-screen or
  specific effect.

## 4. Effects, foley, music
- **Backgrounds** set the space, under dialogue, panned to the surrounds for
  envelopment; never let a BG fight a line.
- **Hard effects** sync and weight; the **LFE** carries only what needs it (impacts,
  rumble) - high-pass the main channels of big effects to keep clarity; LFE in
  theatrical is +10 dB in-band so be conservative.
- **Foley** usually sits lower than editors expect - felt, not heard.
- **Music**: the composer's stems (or the premixed score) balanced to breathe with
  dialogue - duck by automation, not compression; score enters on cue points agreed with
  the music editor; source music gets room/futz treatment.
- **Panning**: picture-consistent for movement; avoid hard pans on cuts; Atmos objects
  for sounds that move or sit overhead; beds for ambiences.

## 5. Running the sessions
- Schedule: premix days per department, then final per reel (a feature reel ≈ 1-2
  days), then playbacks, fixes, printmasters, QC. Build buffer for director notes.
- **Playbacks**: play a reel uninterrupted; take notes with timecodes; fix, replay.
  Directors note what they *can't hear* (a line) and what *pulls them out*; ask for
  feelings, translate to moves.
- Mix at the reference, then listen once at -6 dB and once quietly for intelligibility.
- Check **downmixes** (5.1 -> stereo LtRt/LoRo, mono) and the **near-field** version
  on small speakers/TV; the TV mix often needs a narrower dynamic range (compress stems
  gently, raise dialogue 2-3 dB relative, reduce LFE).

## 6. Deliverables from the mix
Printmasters per format; **stems** (DX/MX/FX, plus foley/BG splits when asked) at the
same timecode; the **M&E** (music and effects, full foley, no dialogue, with optional
dialogue-dependent FX on a separate "opt" stem); loudness measurements and QC report;
the session archived with plug-in list. See the loudness and stems skill for the specs.

## Gotchas
- No premixes; the final becomes a 400-track fight and notes take a day each.
- Monitor level creeping up during the day; the mix is too quiet in the cinema.
- Dialogue drowned by score the director loved in the edit (temp love); explain and demonstrate.
- LFE used as a "sub" for music; theatrical playback shakes the walls.
- Stereo/TV version made by folding down the theatrical printmaster without re-balancing.

## Verify
- [ ] Premixed stems per department, automated, consistent across reels.
- [ ] Room calibrated (85 dB C / -20 dBFS, X-curve if applicable) and the level never moved.
- [ ] Dialogue intelligible at reference and at -6 dB; checked on near-field and in mono.
- [ ] Printmasters per format, stems, M&E and QC report delivered from the same session.
