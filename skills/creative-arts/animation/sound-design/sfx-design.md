---
id: creative-arts.animation.sound-design.sfx-design
name: sfx-design
category: creative-arts
field: animation
product: sound-design
tags: [sound, sfx, audio, design, foley, ambience, ffmpeg, sox, synthesis, cc0, freesound, layering, spotting, diegetic]
level: advanced
status: draft
description: "Design and source SFX locally: ffmpeg/sox synthesis, CC0 libraries, attack/body/tail layering, pitching, spotting to the shotlist."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sfx-design

Goal: give every action and every stylized beat a sound — foley, hits, UI blips, the
show's diegetic glitches — built or sourced entirely locally (no gen-AI, no paid
libraries), cut to the exact on-screen action, and delivered as wavs the mix ducks and
masters (see `creative-arts.animation.sound-design.dialogue-mix-master`). Two sources
only: **synthesize it** (`ffmpeg`/`sox`, zero deps, fully reproducible) or **source it
CC0** and shape it. Prefer synthesis for the stylized/diegetic layer because it is
deterministic and re-renders identically every time — the same consistency law that
governs the picture (`creative-arts.animation.pipeline.character-consistency`).

## Spotting to picture (the shotlist IS the spotting sheet)

Do not invent cues — read them. Each shot in `series/scripts/EP01_shotlist.json`
carries an `fx` array and a `dur_s`. That is the spotting list:

- `SH050` `"fx":["sfx bag tear"]` dur 3.0 — paper/plastic rip + cans dropping.
- `SH060` `"fx":["sfx roll"]` dur 4.0 — orange one bounce, roll, into the drain.
- `SH010` (SQ03) `"fx":["bell"]` — six slow tolls; `SH040` `"bell6"` the sixth.
- `SH050` (SQ03) `"fx":["glitch","scanline","static"]` — the one-frame world-tear.
- `SH020` (SQ04) `"fx":["applause"]`; the finale `applause`/`applause cut`.
- `SH080` (SQ04) `"fx":["counter reveal"]` — the diegetic UI blip when numbers appear.
- `"hum"` recurring — the CRT bed (owned by the mix/pad, see dialogue-mix-master).

Rule: **the SFX length is the action length, never arbitrary.** Build each cue to the
shot's `dur_s` (or shorter, placed at the hit frame), so it lands with picture and the
concat timing holds. A tail longer than the shot bleeds over the cut — trim it or let
it ring under the next shot deliberately, never by accident.

## Synthesis with ffmpeg (primary)

ffmpeg is already our audio stdlib (it masters the episode). Build at 48 kHz to match
delivery. Core generators: `sine`, `anoisesrc` (white/pink/brown), `aevalsrc` (arbitrary
math). Core shapers: `afade` (attack/decay envelopes), `atrim`, `volume`, `asetrate`+
`aresample` (pitch), `aecho`/`aphaser` (space/texture), `highpass`/`lowpass` (band).

**Bag tear** (noise burst + a couple of can thuds):
```bash
ffmpeg -f lavfi -i "anoisesrc=d=0.5:color=white:amplitude=0.7" \
 -af "highpass=f=400,lowpass=f=6000,afade=t=in:d=0.02,afade=t=out:st=0.25:d=0.25" tear.wav
ffmpeg -f lavfi -i "sine=f=90:d=0.18" -af "afade=t=out:d=0.18,volume=0.8" can.wav
```

**Orange roll + drain** (low rolling tone wobbling down in pitch):
```bash
ffmpeg -f lavfi -i "aevalsrc=0.4*sin(2*PI*(140-40*t)*t):d=3:s=48000" \
 -af "tremolo=f=9:d=0.4,lowpass=f=900,afade=t=out:st=2.4:d=0.6" roll.wav
```

**Bell toll** (struck partials — a fundamental plus inharmonic overtones, exp decay):
```bash
ffmpeg -f lavfi -i "sine=f=220:d=4" -f lavfi -i "sine=f=528:d=4" \
 -f lavfi -i "sine=f=698:d=4" -filter_complex \
 "[0][1][2]amix=inputs=3:normalize=0,afade=t=out:d=4,volume=0.6" bell.wav
```

**Glitch / scanline / static** (the world-tear — harsh, one-frame-ish):
```bash
ffmpeg -f lavfi -i "anoisesrc=d=0.4:color=white:amplitude=1.0" \
 -af "highpass=f=1200,bitcrush=bits=4,afade=t=out:st=0.08:d=0.3" static.wav
# scanline whine: the 15.734 kHz CRT line + a sweep
ffmpeg -f lavfi -i "sine=f=15734:d=0.4" -af "volume=0.3,afade=t=out:d=0.4" scanline.wav
```
(If your ffmpeg lacks `bitcrush`, approximate with `aeval`/quantize or route through
sox below.)

**Counter-reveal blip** (clean UI bing — tone + octave, fast decay):
```bash
ffmpeg -f lavfi -i "sine=f=880:d=0.25" -f lavfi -i "sine=f=1760:d=0.25" \
 -filter_complex "[0][1]amix=inputs=2:normalize=0,afade=t=out:d=0.25,volume=0.5" blip.wav
```

**Applause** (dense filtered noise, no single clap readable — mass, not events):
```bash
ffmpeg -f lavfi -i "anoisesrc=d=5:color=pink:amplitude=0.8" \
 -af "highpass=f=700,lowpass=f=5000,tremolo=f=11:d=0.3,volume=0.5" applause.wav
```
The finale `applause cut` is just a hard `afade=t=out:d=0.02` → dead silence for
contrast; the smash-to-black is the silence, not a sound.

## Synthesis / shaping with sox (alternative)

sox is handy for things ffmpeg expresses awkwardly — swept `synth`, `pitch`, `reverb`:
```bash
sox -n whoosh.wav synth 0.6 pinknoise fade h 0 0.6 0.3 bandpass 1200 900 reverb 40
sox can.wav can_low.wav pitch -400          # drop a sourced thud 4 semitones
```

## Layering: attack / body / tail

A convincing effect is almost never one sound. Build in three strata and sum:

- **Attack** (0–30 ms): the transient that sells the hit — a click, a snap, noise spike.
  This is what the ear locks timing onto; place it exactly on the action frame.
- **Body** (the sustain): the recognizable tone/texture — the roll, the ring, the tear.
- **Tail**: decay/space — reverb, room, the drain's hollow. Sell size and place.

Sum with `amix=...:normalize=0` (never let ffmpeg auto-halve), ride each layer with
`volume=` first. Example — the bag tear as a full cue:
```bash
ffmpeg -i tear.wav -i can.wav -i can.wav -filter_complex \
 "[1]adelay=180|180[c1];[2]adelay=420|420[c2];\
  [0][c1][c2]amix=inputs=3:normalize=0,volume=0.9" bag_tear_full.wav
```
`adelay` places the two cans *after* the tear (ms per channel) so you hear rip → can →
can, matching the shot's "can, can, box".

## Pitching without time-change

To pitch a sourced sample and keep its length, resample-and-correct:
```bash
# up ~ +5 semitones (ratio 1.335), then back to 48k so duration is unchanged
ffmpeg -i src.wav -af "asetrate=48000*1.335,aresample=48000,atempo=0.749" up.wav
```
`asetrate` pitches *and* speeds; `aresample` fixes sample rate; `atempo` restores the
original duration. For a quick layered-detune thickener, sum the original with a copy
pitched a few cents off.

## Sourcing CC0 (when synthesis is the wrong tool)

Real-world complexity (a true crowd, specific foley, field recordings) is better
sourced. Use **CC0 / public-domain only** — this library and show must be safe to
resell, so no CC-BY-NC, no "attribution" clips, no ripped library audio:

- **Freesound.org** filtered to **Creative Commons 0**.
- **BBC Sound Effects** (check the specific licence terms per clip before use).
- Public-domain / CC0 foley packs; record your own foley (always clear).

Log every sourced file's origin + licence in a `CREDITS` note next to the stems. Shape
sourced clips to the show (band-limit, add the room, trim to action) so they sit with
the synthesized layer rather than sounding pasted in.

## Delivery to the mix

Render each cue as a 48 kHz wav. Leave headroom — peak ≤ ~0.95, let the master's
`loudnorm`/limiter do the final ceiling, don't pre-smash. Hand the SFX to the mix as a
stem that folds into the bed **before** the sidechain if it should duck under dialogue,
or into the dry branch if it must punch through (the glitch stab, the applause smash) —
see dialogue-mix-master "Adding real music / FX stems".

## Verify

- [ ] Every `fx` cue in the shotlist has a cue, and each cue length ≤ its shot `dur_s`.
- [ ] Transient lands on the action frame (scrub frame-by-frame at the hit).
- [ ] Layers summed with `normalize=0`; peak ≤ 0.95; 48 kHz.
- [ ] Sourced clips are CC0/PD with origin+licence logged.
- [ ] Re-running the synthesis scripts produces byte-identical wavs (deterministic).

status draft: synthesis recipes are standard ffmpeg/sox and the spotting is grounded in
`EP01_shotlist.json`, but the designed SFX stems have not yet been produced/placed for a
A production episode (the current cut uses only the pad+ambience bed). See scoring and
dialogue-mix-master.
