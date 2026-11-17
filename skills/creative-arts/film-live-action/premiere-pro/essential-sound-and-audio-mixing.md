---
id: creative-arts.film-live-action.premiere-pro.essential-sound-and-audio-mixing
name: essential-sound-and-audio-mixing
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, essential-sound, essential-sound-panel, audio-mixing, audio-track-mixer, audio-clip-mixer, ducking, auto-ducking, dialogue, music, sfx, ambience, loudness, loudness-radar, lufs, lkfs, ebu-r128, atsc-a85, clip-gain, audio-gain, normalize, keyframes-audio, rubber-band, submix, submixes, buses, track-types, mono, stereo, 5-1, adaptive-track, audio-channel-mapping, modify-audio-channels, remix, auto-remix, enhance-speech, denoise, dereverb, deess, parametric-eq, multiband-compressor, hard-limiter, audio-effects, track-effects, clip-effects, export-audio, stems, audition, audio-tagging, essential-sound-types, dialogue-repair, enhance-speech-use, auto-ducking-use, ducking-keyframes, audio-effects-use, track-effects-use, submix-use, loudness-radar-use, premiere-loudness, remix-tool, auto-remix-use, channel-mapping-use, modify-audio-channels-use]
level: practitioner
status: draft
description: "Mix in Premiere Pro: channel mapping and track types, Essential Sound with auto-ducking and loudness match, submixes and the Track Mixer, Enhance Speech and denoise, loudness-compliant export."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/essential-sound-panel.html (Adobe - Essential Sound panel)"
  - "https://helpx.adobe.com/premiere-pro/using/audio-track-mixer.html (Adobe - Audio Track Mixer)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional - Premiere Pro exam objectives, Domain 4)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Essential Sound and audio mixing in Premiere Pro

**Goal:** a mix that delivers at the required loudness with clear dialogue, music that
ducks itself, and a structure (submixes, named tracks) that exports stems and survives
a handoff to a mixer.

## 1. Get the channels right before cutting
- `Modify > Audio Channels` on source clips: poly WAV ISOs should be **Mono** clips
  (one channel per track) or *Adaptive*; camera stereo scratch *Stereo*. Set
  `Preferences > Audio > Default Audio Tracks` so multichannel files import as mono
  tracks automatically.
- Track types in the sequence: mono for dialogue, stereo for music/ambience, **5.1** or
  **Adaptive** master only if delivering surround. Right-click track header > rename
  (`DX1`, `DX2`, `FX`, `MX`).
- **Submixes**: `Sequence > Add Tracks > Audio Submix` (stereo): `DX SUB`, `MX SUB`,
  `FX SUB`; in the **Audio Track Mixer** (`Shift+6`) set each track's output to its
  submix and submixes to Master. Bus processing and stems come from this.

## 2. Levels: clip gain, keyframes, faders
- **Audio Gain** (`G`): *Normalize Max Peak to* (-6 dB for dialogue is a safe start) or
  *Normalize All Peaks* across a selection; or set gain by dB. This is per clip and
  pre-fader.
- The rubber band on the clip is **volume** keyframes (pen tool or `Ctrl/Cmd`-click);
  track-level keyframes in the **Audio Clip Mixer** (`Shift+9`) / **Track Mixer**
  with *Write/Latch/Touch* automation while playing.
- Faders for balance between tracks/submixes; keep Master at 0 and fix upstream.
- Fades: `Ctrl/Cmd+Shift+D` default audio transition (Constant Power) on every cut;
  Exponential Fade for music tails.

## 3. Essential Sound panel
`Window > Essential Sound`. Select clips > assign a type: **Dialogue, Music, SFX,
Ambience**. Each exposes task-based controls:
- **Dialogue**: *Loudness > Auto-Match* (levels to -23 LUFS target by default, adjustable
  in panel settings), **Repair** (*Reduce Noise*, *Reduce Rumble*, *DeHum*, *DeEss*,
  *Reduce Reverb*), **Clarity** (*Dynamics*, *EQ presets*, *Enhance Speech*), **Creative**
  reverb presets. **Enhance Speech** (2024+): AI cleanup with a Mix amount - listen for
  artefacts at 100%; 50-70% is usually safer.
- **Music**: *Duration > Remix* (auto-edits the song to a target length - set the
  duration, Premiere finds musical cut points; adjust *Segments/Variations*), **Ducking**
  (duck against Dialogue/SFX/Ambience; *Sensitivity*, *Reduce by* dB (-12 to -18 typical),
  *Fades* ms; *Generate Keyframes* writes volume keyframes you can edit).
- **SFX**: pan/placement, reverb; **Ambience**: stereo width, reverb.
Essential Sound writes real effects (Parametric EQ, Dynamics, DeNoise...) into the
clip's Effect Controls - open them to fine-tune beyond the panel.

## 4. Effects and where to put them
- **Clip effects** (Effect Controls) for problems local to a clip: DeNoise, DeReverb,
  DeHum, Parametric EQ (high-pass ~80 Hz on dialogue), Dynamics.
- **Track effects** (Track Mixer insert slots, `fx` button): the chain for a whole track/
  submix - *Parametric EQ > Multiband Compressor (Broadcast preset) > Hard Limiter* on
  `DX SUB`; *Tube-modeled Compressor* light on music; **Hard Limiter** (-1 to -2 dBTP) on
  the Master as safety.
- VST/AU third-party plug-ins load via `Preferences > Audio > Audio Plug-In Manager`.

## 5. Loudness
Add **Loudness Radar** (Effects > Special > Loudness Radar) on the Master track effect
slot; set the standard (EBU R128 -23 LUFS, ATSC A/85 -24 LKFS, or a custom -16 for web;
True Peak -1/-2). Play the whole program; read Integrated and the radar ring (green =
within tolerance). Adjust submix faders (not the limiter) to hit the target. On export,
*Effects > Loudness Normalization* in the Export panel can normalise to a standard - use
it as a final guard, not instead of mixing.

## 6. Export and handoff
Export panel > *Audio*: 48 kHz, 24-bit, codec per deliverable (PCM in ProRes/MXF; AAC
320 kbps for web). **Stems**: solo each submix and export audio-only passes, or enable
*Export > Audio > Channels* with a multichannel master mapped from submixes (Adaptive
master). For an external mix: `File > Export > OMF`/`AAF` (embed, 48 kHz 24-bit, 2-4 s
handles) or *Edit in Adobe Audition > Sequence*.

## Gotchas
- Stereo clip on a mono track: one channel lost.
- Auto-Match applied to every dialogue clip, then ducking written as keyframes - later edits break both; re-run after the cut is locked.
- Enhance Speech at 100% on music or ambience-heavy clips; underwater sound.
- Loudness fixed with the Master hard limiter; pumping and distortion.
- Export at 44.1 kHz because the music track was 44.1.

## Verify
- [ ] Channels mapped (mono dialogue), tracks named, submixes routed to Master.
- [ ] Essential Sound types assigned; dialogue repaired; music ducked with editable keyframes.
- [ ] Track chain on DX submix; Hard Limiter on Master as safety only.
- [ ] Loudness Radar reads the target integrated/true peak over the full program; stems exported.
