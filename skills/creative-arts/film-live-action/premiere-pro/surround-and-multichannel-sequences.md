---
id: creative-arts.film-live-action.premiere-pro.surround-and-multichannel-sequences
name: surround-and-multichannel-sequences
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, surround-sequence, multichannel-master, premiere-5-1, audio-master, 5-1-mix, track-output-channel, stems-export, multichannel-export, channel-mapping, audio-track-mixer, surround-panner]
level: practitioner
status: draft
description: "Set up Premiere Pro sequences for 5.1 and multichannel masters: audio master choice, surround panning, mapping track outputs to channels, and exporting stems in the right order."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/mixing-audio-tracks-clips.html (Adobe - Audio Track Mixer and panning)"
  - "https://helpx.adobe.com/premiere-pro/using/creating-changing-sequences.html (Adobe - Sequence settings, audio master)"
  - "https://helpx.adobe.com/premiere-pro/using/exporting-multichannel-audio.html (Adobe - Multichannel audio export)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Surround and multichannel sequences in Premiere Pro

**Goal:** a sequence that outputs a correct 5.1 mix or a multichannel file of stems
(e.g. stereo mix + DX/MX/FX splits) that the broadcaster's QC accepts.

## 1. Choose the audio master at creation
*New Sequence > Tracks > Audio Master*: **Stereo**, **5.1**, **Multichannel** (up to 32
channels) or Mono. Decide before cutting - the master type is fixed once the sequence
exists. To change it later, make a new sequence with the right master and paste or nest
the old one.

## 2. 5.1 sequence
- Dialogue on mono tracks, music/ambience on stereo tracks, all sent to the 5.1 master.
- *Audio Track Mixer*: double-click a track's panner to open the **surround panner**;
  set dialogue to centre, music spread front with a little surround, ambience wide.
- Centre and LFE levels are in the panner; keep LFE for deliberate low-end only.
- Monitoring: *Preferences > Audio Hardware* output mapping to a 6-channel interface;
  on stereo monitors you only hear a downmix.

## 3. Multichannel master for stems
Typical layout requested: ch1-2 stereo mix, ch3-4 stereo M&E, ch5-6 DX, ch7-8 MX.
- Master = Multichannel with the required channel count.
- In the Audio Track Mixer, right-click a track's output > **Track Output Channel
  Assignment**, route each stem's submix to its channel pair.
- Build submixes (DX, MX, FX) and route those, not individual tracks.

## 4. Export
- *Export > Audio*: format WAV/broadcast or embedded in the MXF/MOV; **Channels** =
  5.1 or the multichannel count; sample rate 48 kHz, 24-bit.
- Check channel order against the spec (SMPTE 5.1 is L, R, C, LFE, Ls, Rs). Do not
  assume: play an exported **channel ident** (voice "left", "right"... per channel) or
  tone on each channel and confirm in a DAW.

## Gotchas
- A stereo master sequence nested into a 5.1 sequence arrives as stereo only.
- Mono tracks left panned centre in a 5.1 master go to C only - fine for dialogue,
  wrong for a mono music stem.
- Adaptive tracks with unmapped channels drop audio on export.
- Loudness measured on the stereo downmix does not prove the 5.1 meets spec.

## Verify
- [ ] Master type matches the deliverable before cutting starts.
- [ ] Channel idents in the exported file land on the spec'd channels.
- [ ] Stems sum to the full mix (null test in a DAW).
- [ ] Loudness measured on the actual delivery format.
