---
id: creative-arts.animation.sound-design.scoring
name: scoring
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, music, scoring, score, music-bed, stinger, drone, leitmotif, mido, midi, fluidsynth, soundfont, sf2, local, open-source]
level: advanced
status: verified
description: "Score a cue to picture locally: Python/mido-generated MIDI -> FluidSynth + a free SoundFont -> wav stems for the final mix."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# scoring

Goal: real music — a warm, too-pleasant "sitcom" bed that curdles, a low drone under
everything, stingers on the reveals — composed **under code control**, rendered
locally, no cloud music-gen. This closes the project's open scoring gap and **replaces
the temporary pad** synthesized in `series/production/build_audio.py` (the detuned
C-minor sines are a placeholder standing in for a score; once a real cue exists, drop
the `[pad]` node and sum the cue into the bed instead — see
`creative-arts.animation.sound-design.dialogue-mix-master`).

## Tool decision (settled)

**Python `mido` → MIDI → `fluidsynth` + a free SoundFont (`.sf2`) → wav.** This beats
the alternatives for *this* pipeline because it is scriptable, reproducible, and
diffable: a cue is a Python file, so it re-renders byte-stable and version-controls like
the rest of the show. Sonic Pi (Ruby live-coding) and SuperCollider are strong but add a
second language/runtime; LMMS/MuseScore are GUI-first and don't fit a headless batch.

Install once:
```bash
pip install mido
# FluidSynth binary: winget install FluidSynth  (or apt/brew install fluidsynth)
```
SoundFont — use one whose licence permits commercial redistribution (the show is meant
to be sold): **GeneralUser GS** or **FluidR3_GM** for a General-MIDI palette (piano,
strings, celesta, organ — everything the sitcom-bed and the "wrong" variant need).
Confirm the specific `.sf2` licence and keep a `CREDITS` note beside the stems. Reference
it as `<SOUNDFONT>` below.

## Read the cue from picture first

A cue is written to a span of the cut, not in the abstract. Pull the span from
`series/scripts/EP01_shotlist.json`: sum the `dur_s` of the shots the cue covers.
Example — the Act-3 "stutter" build (SQ03 `SH005`→`SH050`) runs 4.0+4.5+4.5+3.5+4.0+2.5
+2.5 = **25.5 s**. That length, the tempo, and the key fix the bar count:

```
bars = round(length_s * tempo_bpm / 60 / beats_per_bar)
```

## Tempo / key / mood from the color-script

The look drives the music. The production's color-script is "permanent gold late-afternoon,
too clean, that curdles":

- **Comfort / gold:** slow, warm **C major**, ~76–84 BPM, simple triads, celesta or
  tack-piano — a jingle that resolves a little *too* neatly and loops a little *too*
  long, so it reads as canned.
- **Wrongness / the tear:** the **same motif** detuned and slowed, pushed to **C minor**
  (which is exactly why the placeholder pad is C-minor 130.8/155.6/196.0 Hz — the score
  should agree with it), lower register, strings sul-tasto or an organ drone.
- **The hum/drone:** a sustained low C under the whole episode (the "television-left-on"
  feeling) — see the drone track below.

## Motif / leitmotif discipline

Write **one** short "comfort" theme (3–5 notes, a jingle) and derive everything from it,
so the score is recognizable across episodes and seasons (the audio sibling of the
character-consistency law). The "wrong" cue is not a new tune — it's the comfort motif
transformed: flatten the third (major→minor), slow it, detune, voice it an octave down.
Same DNA, curdled.

```python
# cue.py — comfort motif + its "wrong" variant, as MIDI
import mido

TPB = 480                       # ticks per beat
mid = mido.MidiFile(ticks_per_beat=TPB)
tempo = mido.bpm2tempo(80)      # 80 BPM, warm

def track(program, name):
    t = mido.MidiTrack(); mid.tracks.append(t)
    t.append(mido.MetaMessage('track_name', name=name, time=0))
    t.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    t.append(mido.Message('program_change', program=program, time=0))
    return t

def notes(t, seq, vel=70):
    # seq = [(midi_note, beats)]; note 0/None = rest
    for n, beats in seq:
        dur = int(beats * TPB)
        if n is None:
            t.append(mido.Message('note_off', note=0, velocity=0, time=dur)); continue
        t.append(mido.Message('note_on',  note=n, velocity=vel, time=0))
        t.append(mido.Message('note_off', note=n, velocity=0,  time=dur))

C4, E4, G4, A4 = 60, 64, 67, 69
# COMFORT motif in C major (celesta=8), resolves too neatly
mel = track(8, 'comfort')
notes(mel, [(G4,1),(E4,1),(C4,2),(E4,1),(G4,1),(A4,.5),(G4,1.5)], vel=64)

# WRONG variant: same shape, minor third, slowed, lower, strings (program 48)
def minorify(n): return n - 1 if n in (E4,) else n        # E->Eb curdle
wr = track(48, 'wrong')
notes(wr, [(minorify(n)-12, b*1.5) for n, b in
           [(G4,1),(E4,1),(C4,2),(E4,1),(G4,1),(A4,.5),(G4,1.5)]], vel=55)

mid.save('cue.mid')
```

For the **drone**, one long held low note on an organ/pad patch for the whole cue length
(compute beats from the span above), very low velocity:
```python
dr = track(89, 'drone')                       # pad patch
C2 = 36
dr.append(mido.Message('note_on', note=C2, velocity=40, time=0))
dr.append(mido.Message('note_off', note=C2, velocity=0, time=int(bars*4*TPB)))
```

## Dynamics to picture

Shape with velocity and entries, not post-gain: start the bed sparse, **swell into the
reveal** by raising velocities / adding the string layer over the bars leading to the
cut, and **cut to silence on the glitch** (`SH050` one-frame tear) for contrast by simply
ending the MIDI there. The mix will duck the whole cue under dialogue anyway, so compose
as if dialogue weren't there — write the *music*, let the sidechain handle the voice.

## Render to wav — one pass per stem

Keep bed / drone / stinger as **separate wavs** so the mix can balance and duck them
independently. Easiest reproducible way: write one `.mid` per stem (or mute tracks per
render) and render each with FluidSynth at the delivery rate:

```bash
fluidsynth -ni -F cue_bed.wav   -r 48000 -g 0.8 <SOUNDFONT> cue_bed.mid
fluidsynth -ni -F cue_drone.wav -r 48000 -g 0.8 <SOUNDFONT> cue_drone.mid
fluidsynth -ni -F cue_sting.wav -r 48000 -g 0.9 <SOUNDFONT> cue_sting.mid
```
`-n` no MIDI-in, `-i` no shell, `-F` render-to-file, `-r 48000` match delivery, `-g`
master gain (keep ≤ 1.0 for headroom). Trim/pad each to the exact cue length with
`ffmpeg -af apad -t <len>` so it lines up with the picture span.

## Hand to the final mix

Drop the stems in `workspace/music/ep01/` (bed/drone/stinger wavs, 48 kHz). In the mix
graph they replace the temp pad: fold bed+drone into `[bed]` before the sidechain so they
duck under dialogue; route a reveal stinger that must punch *through* into the dry branch.
Exact filter wiring is in dialogue-mix-master → "Adding real music / FX stems".

## Verify

- [ ] A reusable comfort leitmotif exists **and** the "wrong" cue is a transform of it
      (same intervals, minor/slowed/detuned), not a different tune.
- [ ] A continuous low drone spans the cue/episode.
- [ ] Cue length == the summed `dur_s` of the shots it covers (lines up at the cut).
- [ ] Stems are separate 48 kHz wavs (bed / drone / stinger) for independent ducking.
- [ ] Re-running `cue.py` + fluidsynth reproduces identical wavs.
- [ ] SoundFont licence permits commercial redistribution; logged in CREDITS.

status draft: the mido→FluidSynth→wav workflow is the chosen, runnable path and the
motif/key logic is grounded in the show's color-script and the placeholder pad's
C-minor, but no cue has yet been produced and folded into a production mix — that is the
next production step. See dialogue-mix-master, sfx-design.

## Verified (proof)
Ran end-to-end on one episode (14 Oct 2026): `compose_score.py` wrote five cues with
mido (one leitmotif across the episode: a looping pleasant-wrong music-box waltz, sparse
minor piano, six tubular-bell tolls timed to the scripted ritual, a detuned-cheerful host
theme over pizzicato, and the minor-augmented theme at the finale) and rendered them
through FluidSynth + GeneralUser GS to 48k wavs, placed at sequence offsets and ducked
under dialogue in the final mix. The leitmotif + mood-per-sequence discipline held;
sparse cues sat under dialogue without wallpapering.
