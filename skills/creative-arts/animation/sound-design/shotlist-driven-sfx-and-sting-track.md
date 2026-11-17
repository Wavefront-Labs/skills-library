---
id: creative-arts.animation.sound-design.shotlist-driven-sfx-and-sting-track
name: shotlist-driven-sfx-and-sting-track
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, sfx, foley, sting, riser, impact-frame, engagement, pacing, ffmpeg, numpy, sync, loudnorm, concat, retention]
level: advanced
status: draft
description: "Build a synced foley + reveal-sting track and anime impact frames from a shotlist with numpy/ffmpeg; sync to real clip starts, not summed durations."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Shotlist-driven SFX and sting track (plus impact frames)

**Goal:** a cut with VO and score but no effects feels dead. Viewers read sound as
impact. This skill adds the missing layer in one script and one assembly hook. It
builds a full-length foley track and synthesized reveal stings from the shotlist.
It also puts a 2-frame impact frame on picture at the same beats. Everything stays in
sync after any retime.

## Data in the shotlist, not in code

Give each shot two optional fields, in seconds from the shot start:

- `sting`: a riser that ends on this time, then a low boom and a minor-chord stab.
- `impact`: a one-drawing (2 frames at 24 fps) inverted, high-contrast flash, then a
  short shake.

Keep per-shot foley in a small dict in the SFX script. Each entry is a list of
(offset, library sound prefix, variant, gain). Use a lambda that gets the shot
duration so "mid-shot" glitches and footstep runs scale with retimes.

**Budget:** about one sting per 40 s of runtime. Nine in a 6-minute episode read as
punctuation. Twenty read as noise. Impact frames only on hard physical or reveal hits,
not on slow reveals.

## The sting recipe (numpy, no music tool)

```python
pre = int(0.8*SR); t = np.arange(int(2.4*SR))/SR
rise = lowpass(noise(pre), 3000) * np.linspace(0, 1, pre)**3 * 0.35   # ends on the hit
f = 38 + 32*np.exp(-t*3)                                              # pitch-dropping boom
boom = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*2.2)
hit = lowpass(noise(t.size), 1800) * np.exp(-t*22) * 0.6
stab = sum(np.sin(2*np.pi*hz*t) for hz in (130.8, 155.6, 196.0, 261.6)) * 0.12 * np.exp(-t*1.6)
```

Place it at `shot_start + sting - 0.8` so the riser crosses the cut. A sting at 0.0
on a shot rises out of the previous shot, which is the classic pull into a reveal.
Measured result: the hit sits about 9 dB over the bed and dialogue around it.

## Foley from a CC0 library

Pick files by name prefix with a recursive glob, mix to mono, resample to 48 kHz with
`scipy.signal.resample_poly`. Loop beds (hum, spark, rolling, faint applause) are
`np.resize`d to the shot end with a short fade. Normalise a quiet source such as an
applause recording to peak 1 before applying gain. An unnormalised applause swell
measured -31 dB and vanished under the score. Peak-limit the whole track to 0.95
and write it stereo so it mixes with the stereo dialogue bus.

Mix it un-ducked: the sidechain duck belongs to the music and ambience bed only.
Effects that duck under dialogue lose the hits that land on lines.

## Sync: measure real clip starts

Per-shot clips concatenated with the concat demuxer each run about 40 ms longer than
their scripted duration. AAC frames pad the audio and the container takes the longer
stream. Over 87 shots this drifted 1.6 s, so stings late in the episode landed a beat
early on picture.

**Fix:** after normalising each clip, probe its container duration and write a
`timing.json` of real shot starts. The SFX builder and the score placement read it,
falling back to summed durations only when it is missing. Run the SFX build inside
the assembly step, after the concat and before the mix.

## Silence that has to be exact (smash to black)

After `dynaudnorm` and `loudnorm`, filter timestamps are skewed by their lookahead.
`volume=0:enable='gte(t,T)'` and `afade=t=out:st=T` both fired about 2 s late.
Cut by sample count instead, at the end of the chain:

```
loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,atrim=end_sample=N,apad=whole_len=M
```

N is the black time times 48000 and M the full length times 48000. Verified: -180 dB
from the first sample of the black shot, and the track length still matches picture.

## Impact frame on picture (ffmpeg, during the per-clip grade)

```
hue=s=0:enable='between(t,A,A+0.083)',negate=enable='between(t,A,A+0.083)',
eq=contrast=2.2:enable='between(t,A,A+0.083)',
crop=1880:1058:'20+18*sin(t*95)*S':'11+10*cos(t*80)*S',scale=1920:1080
```

S is `gte(t,A)*exp(-(t-A)*9)`. Quote the crop expressions: the commas inside `gte()`
otherwise split the filter graph ("No such filter: '0.400)*exp(...'"). The crop holds
the whole shot about 2 % tighter, which is fine on a hit shot.

## Pacing retime that keeps every line

For a cold open, set each dialogue shot to the voice-over length plus 0.5 s, never
longer than before, with a 2 s floor. Silent beats go to 2 to 2.5 s, except a
deliberate held beat before the title. This took a 78 s cold open to 60 s with no
line cut. Re-trim existing frames to the new duration rather than re-rendering; an
eased push that stops at 75 % still reads as a push.

## Verify

1. Grab a tile of frames around each `impact` time from the final cut; the inverted
   frame must be the second or third tile, not a neighbouring shot.
2. Decode the whole mix to WAV and measure RMS windows in numpy. Do not trust
   `ffmpeg -ss X -i cut.mp4 -af volumedetect`: input seeking on the mp4 read stings as
   -33 dB that the decoded track showed at -11 dB.
3. Cross-correlate the mix envelope with the SFX track at a few points; lag must be 0.
4. Check RMS in 0.2 s windows across the smash to black.

## Failure modes

- Stings drift late in the episode: timing from summed durations instead of measured
  clip starts.
- Silence starts seconds late: pts-based mute after a lookahead filter.
- Applause or room beds inaudible: quiet source not normalised.
- Every reveal stung: the stings stop meaning anything. Keep the budget.

See `foley-design`, `cartoon-sfx-vocabulary` and `final-mix` for the craft behind
choosing the sounds; this skill is the build and sync mechanics.
