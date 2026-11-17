---
id: creative-arts.animation.sound-design.dialogue-mix-master
name: dialogue-mix-master
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, mix, master, dialogue, loudness, loudnorm, lufs, ffmpeg, ducking, sidechain, dynaudnorm, youtube, stems]
level: advanced
status: verified
description: "Dialogue cleanup + sidechain-ducked bed + two-pass loudnorm to YouTube -14 LUFS/-1.5 dBTP, in one ffmpeg filter_complex."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# dialogue-mix-master

Goal: take a rendered cut whose timeline already carries per-shot VO (or silence)
and produce one balanced, legal-loudness stereo master where dialogue sits clearly
on top and everything else — pad, ambience, music, FX — supports it and gets out of
the way the instant anyone speaks. Done entirely in `ffmpeg` (our audio stdlib); no
DAW, no new deps. The whole chain is one `filter_complex` graph, which makes it
deterministic and re-runnable: same input cut, same master, every time.

## The stem model (why there is no mixer window)

We never bounce a mixing-console project. The "stems" are logical graph nodes inside
one filter chain:

- **Dialogue stem** = the input video's existing audio `[0:a]`. VO is baked onto the
  episode timeline shot-by-shot upstream (each shot clip is cut to its `dur_s` with
  its line's wav or `anullsrc` silence — see `series/production/build_episode.py`), so
  by mix time the dialogue is already in sync with picture. We do not re-time it here.
- **Pad stem** = synthesized tonal bed (atmosphere, not melody).
- **Ambience stem** = filtered pink noise (air/room tone).
- **Music / FX stems** (future): extra `-i` inputs summed into the bed the same way.

Keeping them as named labels (`[dry]`, `[bed]`, `[bedduck]`, `[aout]`) means a fix is
surgical: change one node's `volume=` or one filter, re-run, done.

## In this pipeline

`series/production/build_audio.py` is the whole master. `series/production/final_assembly.py`
calls it as the last step after concatenating the picture cut. The real graph:

### 1. Dialogue cleanup + split for the key

```
[0:a]highpass=f=80,lowpass=f=12000,dynaudnorm=f=250:g=5,asplit=2[dry][key]
```

- `highpass=f=80` kills rumble/handling/DC below the voice fundamental.
- `lowpass=f=12000` tames TTS hiss and sibilant fizz above the intelligibility band
  (Kokoro/Piper synthesis carries junk up top; 12 kHz keeps crispness, drops the fizz).
- `dynaudnorm=f=250:g=5` is the workhorse: frame-based (250 ms) dynamic normalization
  with gaussian smoothing window `g=5`, so quiet lines come up and loud ones sit back
  **without** a hard compressor pumping. This is our automatic level-automation — it
  replaces riding faders per line.
- `asplit=2[dry][key]` forks the cleaned dialogue into two: `[dry]` is what you hear,
  `[key]` is the **sidechain key** that drives the ducker. Ducking off the *cleaned*
  dialogue (not raw `[0:a]`) means silence stays silence — rumble can't trip the duck.

### 2. Synthesize the bed (pad + ambience)

Pad — an eerie C-minor triad (C3 130.8 / Eb3 155.6 / G3 196.0 Hz), the "gold town
that curdles" tone:

```
sine=frequency=130.8:sample_rate=48000,atrim=0:{D},asetpts=PTS-STARTPTS[s1];
sine=frequency=155.6:sample_rate=48000,atrim=0:{D}[s2];
sine=frequency=196.0:sample_rate=48000,atrim=0:{D}[s3];
[s1][s2][s3]amix=inputs=3:normalize=0,
tremolo=f=0.13:d=0.5,aecho=0.8:0.88:900|1300:0.3|0.2,lowpass=f=1100,volume=0.06[pad]
```

`{D}` is the cut's duration from `ffprobe` so the bed spans the exact runtime.
`normalize=0` on **every** `amix` is critical — ffmpeg's default divides by input count,
which would silently halve levels each time you sum. The `tremolo=f=0.13` gives a slow
0.13 Hz throb; `aecho` smears it into a reverb tail; `lowpass=f=1100` removes brightness
so it reads as under-the-floor dread; `volume=0.06` parks it ~24 dB down.

Ambience — pink-noise air:

```
anoisesrc=d={D}:color=pink:amplitude=0.6:sample_rate=48000,
highpass=f=90,lowpass=f=1800,volume=0.05[amb]
```

Band-limited 90–1800 Hz room tone at `volume=0.05`. Pink (not white) because its
1/f spectrum sits under dialogue instead of hissing over it.

### 3. Duck the bed under dialogue (sidechaincompress)

```
[pad][amb]amix=inputs=2:normalize=0[bed];
[bed][key]sidechaincompress=threshold=0.06:ratio=8:attack=12:release=320[bedduck]
```

`sidechaincompress` compresses the **first** input (`[bed]`) whenever the **second**
(`[key]` = dialogue) exceeds `threshold=0.06` (linear amplitude, ~ -24 dBFS). `ratio=8`
is a firm duck (8:1), `attack=12` ms pulls the bed down fast enough that the first
syllable isn't masked, `release=320` ms lets it breathe back up in the gaps so it
doesn't pump audibly between words. Tune `threshold` first if ducking is too eager/lazy,
`release` second if it pumps.

### 4. Sum and master to the YouTube target

```
[dry][bedduck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]
```

Dialogue + ducked bed, then `loudnorm` to **I=-14 LUFS integrated, TP=-1.5 dBTP,
LRA=11**. YouTube normalizes playback to ~ -14 LUFS, so mastering there means the video
is neither turned down (losing punch) nor pumped. TP -1.5 leaves headroom for
inter-sample peaks the lossy transcode can push over 0.

Output: `-c:a aac -b:a 384k -ar 48000 -movflags +faststart`, video `-c:v copy` (we only
re-lay audio, never re-encode picture).

## Two-pass loudnorm for the final master (do this for delivery)

`build_audio.py` runs loudnorm **single-pass inline** — fine for a review cut, but a
single pass only estimates the correction. For the delivery master, measure then apply:

```bash
# pass 1 - measure (JSON to stderr)
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
# pass 2 - apply the measured values with linear gain
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:\
measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true \
 -ar 48000 master.wav
```

`linear=true` applies one linear gain from the measurement instead of dynamic
loudnorm re-riding the program, so transients and the LRA survive intact.

## Adding real music / FX stems

When scoring (see `creative-arts.animation.sound-design.scoring`) and designed SFX
(`creative-arts.animation.sound-design.sfx-design`) exist as wavs, add them as inputs
and fold them into the bed **before** the sidechain, so they duck under dialogue too:

```
[music][sfx]amix=inputs=2:normalize=0,volume=0.4[musfx];
[pad][amb][musfx]amix=inputs=3:normalize=0[bed]
```

FX that must punch *through* dialogue (a glitch stab, the applause smash) route around
the ducker: sum them into `[dry]`'s branch instead of the bed. The scoring cue replaces
the temp pad entirely once a real cue exists — drop the `[pad]` node, keep `[amb]`.

## De-ess / per-line automation (not yet in-pipeline)

`dynaudnorm` covers broad level automation; it does **not** de-ess. If Kokoro/Piper
sibilance spikes on a specific voice, insert `deesser` or a narrow `highpass`/`equalizer`
dip around 6–8 kHz on `[0:a]` before the split. Add only if you hear it — it is not
currently in `build_audio.py`.

## Verify

- [ ] Dialogue intelligible over bed at every line — scrub the loudest-bed moments and
      the quietest lines; the duck must win.
- [ ] `ffmpeg -i master.mp4 -af loudnorm=...:print_format=json -f null -` re-measures
      **I ≈ -14 LUFS, TP ≤ -1.5 dBTP, LRA ≈ 11**.
- [ ] No clipping; output is 48 kHz stereo AAC, `+faststart` set.
- [ ] Every `amix` carries `normalize=0` (no silent halving).
- [ ] Silence between lines is actually silent (the duck keyed off cleaned, not raw,
      dialogue).

status draft: the graph is implemented and runs in `build_audio.py`/`final_assembly.py`
on one production cut; not yet re-confirmed against real music/SFX stems (none
produced yet) or the two-pass delivery master. See scoring, sfx-design, and the
encode/mux step in `creative-arts.animation.pipeline.shot-episode-structure`.
