---
id: creative-arts.animation.voice-tts.voice-direction
name: voice-direction
category: creative-arts
field: animation
product: voice-tts
tags: [voice-direction, tts, prosody, kokoro, piper, performance, pauses, breaths, emphasis, takes, comping, ffmpeg, rubberband, atempo, emotion, pacing, monotony, reads, beats]
level: advanced
status: draft
description: "Direct a performance out of local TTS (Kokoro/Piper): beat-split lines, pauses/breaths, per-beat rate/pitch/energy from emotion tags, takes+comping, and anti-monotony rules."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SKILL: Voice direction for local TTS (getting a performance, not a readout)

**Goal:** a line of local TTS (Kokoro, Piper) that a listener hears as *acted* — with
intention, pacing, breath and emotional shape — not read. TTS engines are not actors;
they are instruments. The performance lives entirely in how you *play* them: what you
feed in per beat, what you insert between beats, and which of several takes you keep.
This skill is the director's chair. The locked identity (engine, voice, base speed, FX)
comes from `voice-casting-consistency` and is never touched here: **direction varies
delivery on top of a frozen voice, never the voice itself.**

## 1. The core move: beat-split the line, synthesize per phrase

The single biggest fix for robotic reads. A TTS engine given a whole line flattens it
into one prosodic arc. An actor delivers a line as *beats* — thought-units separated by
micro-decisions. So split before you synthesize:

```
FLAT (one synth call):
  "I told you not to open the gate. Now look at it. Look at what came through."

DIRECTED (five synth calls + inserted gaps):
  [beat 1, controlled]   "I told you"            speed 0.95
  [beat 2, tightening]   "not to open the gate."  speed 0.90
  [gap 600ms — she looks at the gate]
  [beat 3, flat, quiet]  "Now look at it."        speed 0.85
  [gap 350ms + breath sample]
  [beat 4, breaking]     "Look at what"           speed 0.92, pitch +1 st
  [beat 5, landed]       "came through."          speed 0.80, pitch -1 st
```

Rules of the split:
- **Split on thought, not grammar.** A beat ends where the character makes a decision,
  notices something, or changes tactic — often mid-sentence.
- **One intention per beat.** If you can't name the beat's verb ("warn", "accuse",
  "plead"), split again or merge.
- **Keep beats ≥ 2 words where possible.** Single-word fragments synthesize with odd
  terminal prosody; prefer "not to open the gate." over "not." + "to open the gate."
- Concatenate with ffmpeg: render each beat to wav, write a `concat` list with
  `anullsrc`-generated silence files (or `adelay`/`apad`) for the gaps, then
  `ffmpeg -f concat -safe 0 -i list.txt -c copy line.wav`. Keep the per-beat files —
  re-direction means re-rendering one beat, not the line.

## 2. Pauses-for-thought and breaths

Silence is acting. TTS gives you none beyond punctuation; insert it deliberately:
- **Thought pauses:** 300–700 ms between beats where the character decides; 800–1500 ms
  for a genuine stop (bad news landing, a lie being constructed). Under 250 ms reads as
  a comma; over 2 s needs a visual to carry it.
- **Breaths:** keep a small per-character breath bank — 4–6 short samples (calm inhale,
  sharp inhale, tired exhale, pre-shout gulp). Record them yourself or synthesize
  near-silent "hh" / "ahh" fragments and gate them down ~−18 dB relative to dialogue.
  Place a breath **before** an effortful or emotional beat, never after every beat
  (that reads as asthma). One or two per line, maximum.
- **Reaction gaps in dialogue:** when another character's line lands, the response
  starts late — pad 200–500 ms of lead-in silence sized to how hard the previous line
  hit. The pacing between lines is edited in `dialogue-editing`; this skill only says
  *how long the thought takes*.

## 3. Per-beat rate / pitch / energy from the emotion tag

Every shotlist line carries an emotion tag; map it to concrete per-beat deltas applied
**relative to the character's locked base** from the voice bible:

| Emotion tag | Rate (× base) | Pitch (st) | Energy (gain/soft-clip) | Gap tendency |
|---|---|---|---|---|
| calm / neutral | 1.00 | 0 | 0 dB | normal |
| excited / joyful | 1.08–1.15 | +1 to +2 | +1.5 dB | short gaps |
| angry (hot) | 1.05–1.12 | +1 | +2 dB, slight drive | clipped gaps |
| angry (cold) | 0.88–0.95 | −1 | −1 dB | long gaps |
| afraid | 1.05–1.18 | +2 | −2 dB (quiet-fast) | irregular gaps |
| sad / defeated | 0.82–0.92 | −1 to −2 | −3 dB | long gaps, breaths |
| sarcastic | 0.92 on the key phrase | +1 then fall | 0 dB | pause *before* the barb |
| whisper / conspiratorial | 0.90 | 0 | −6 dB + presence EQ | tight gaps |

Implementation per engine:
- **Kokoro:** `speed` per beat (it has no pitch input — pitch is post, below). Energy is
  post gain.
- **Piper:** `--length_scale` per beat (inverse of rate: 0.9 = faster), and nudge
  `--noise_scale` / `--noise_w` ±0.1–0.2 from the approved value for shaky/afraid beats
  only — return to base after; these are delivery overrides, logged in the shotlist row,
  never written back to the voice bible.
- The table is a starting grid, not a law: direct by ear, log what you used.

## 4. Emphasis on the stressed word

TTS stresses the wrong word constantly ("I never said she stole it" has seven
meanings). Two tools, in order of preference:
1. **Re-synthesize the stressed phrase as its own beat** with +0.03–0.08 rate *drop*
   (stressed words are slower), +1 st, +1–2 dB — the engine's own voice doing the
   stress, so it sits naturally. Punctuation helps: isolating "never." with a full stop
   changes its contour.
2. **Post micro-automation with ffmpeg** when re-synthesis can't land it:
   - Tempo without pitch: `ffmpeg -i beat.wav -af "rubberband=tempo=0.93" out.wav`
     (or `atempo=0.93` — fine for ±10%, artifacts beyond).
   - Pitch without tempo: `rubberband=pitch=1.0595` (+1 st; semitone ratio 2^(n/12)).
   - Crude combined shift: `asetrate=24000*1.0595,aresample=24000,atempo=1/1.0595`.
   - Automate only the stressed word's region: split the beat at word boundaries
     (Rhubarb's timings from `vo-lipsync-pipeline` give you word-level cuts for free),
     process the slice, re-concat.
   Keep post moves under ±1.5 st and ±10% tempo — beyond that the voice stops being the
   cast voice and you've broken `voice-casting-consistency`.

## 5. Takes and comping

Even a deterministic engine gives you variation if you vary the inputs. Direct like a
session: multiple takes, pick the performance.
- **Generate 3–5 takes per emotional beat** by varying the *legal* knobs: rate ±5%,
  beat-split points, punctuation ("Now, look at it." vs "Now… look at it."), Piper
  noise params within the override window, breath placement.
- **Name takes deterministically**: `ep03_sc04_CHIP_L012_b3_t2.wav` — episode, scene,
  character, line, beat, take. The comped choice is recorded in the shotlist row
  (`"take": {"b3": 2}`) so the line re-renders identically forever.
- **Comp per beat, not per line** — take 2's beat 1 with take 4's beat 3 is normal.
- Listen on the dialogue bus, not solo: a take that wins in isolation can lose under
  music. Final level/placement is `dialogue-mix-master`'s job.

## 6. Reactions and efforts

The difference between a cartoon and a slideshow with narration is the non-verbal
layer: sighs, hms, gasps, effort grunts, laughs.
- **Synthesizable:** "Hm.", "Hmm?", "Huh.", "Oh.", "Ah—", "Ha. Ha ha." render
  surprisingly well as their own one-beat synth calls with aggressive rate/pitch
  deltas. Build each character a small reaction bank this way and reuse.
- **Recorded:** sighs, gasps, effort sounds (lifting, falling, shivering) rarely
  synthesize well — record a bank yourself and pitch/formant-shift per character
  (`rubberband=pitch=` to sit near the cast voice's register), or source CC0 efforts.
- **Place them as dialogue events** in the shotlist like any line, so lip-sync
  (`lip-sync`) and the mix see them. A reaction every 2–4 lines of listening keeps a
  scene alive.

## 7. Proximity and room

A directed read in the wrong acoustic reads as pasted-on. Per scene, after the
character FX chain (which is identity and never changes):
- **Distance:** close = dry + low-shelf +1–2 dB (proximity effect); far = high-shelf
  −3–6 dB above ~6 kHz, more reverb send, −3 dB per doubling of distance.
- **Room:** one reverb preset per location, stored with the scene, not per line
  (`afir` with a small IR set, or `aecho`/light `areverb` for stylized cel spaces).
  Shouting in a canyon and whispering in a cupboard must sound like it.
- **Off-screen / through-door:** band-pass `highpass=f=300,lowpass=f=3400` plus the
  room send. Keep the raw dry stem; the spatial chain is a mix layer
  (`dialogue-mix-master`), applied non-destructively.

## 8. Directing against monotony

The audience forgives a synthetic timbre long before it forgives sameness. Hard rules:
- **No two adjacent lines at the same rate *and* energy.** If line A shipped at base
  rate/0 dB, line B moves at least one knob (±5% rate or ±1.5 dB or a deliberate gap
  change) — even inside the same emotion.
- **Scene shape:** a scene has a pace arc like a shot has a line of action. Mark the
  scene's fastest and slowest line before rendering any of them, and grade the rest
  between.
- **Vary beat counts.** Three consecutive lines each split into two symmetric beats is
  its own monotony; let some lines run unbroken and some shatter.
- **Question/answer contour:** a reply should not mirror the question's contour —
  answer a fast question slowly, a quiet accusation loudly, unless sameness is the
  joke.
- Enforce it mechanically: a check script that measures each rendered line's duration
  ÷ word count (tempo proxy) and RMS, and flags any adjacent pair within 3% tempo *and*
  1 dB RMS of each other.

## 9. Worked example: one flat line to a directed read

Line (shotlist): `GRAN_WYNN, emotion: cold-fury, "You brought it into my house."`

Flat version: one synth call at base — even pace, polite fall at the end. Reads like a
weather report.

Directed:
1. **Name the beats:** accusation ("You brought it") / the unthinkable object ("into
   my house."). The intention: *make him understand what he's done*, cold, not shouted.
2. **Map cold-fury:** rate ×0.90, pitch −1 st, energy −1 dB, long gaps.
3. **Render:** beat 1 at ×0.92; 900 ms gap (she lets it land); slow exhale breath at
   −18 dB; beat 2 at ×0.85 with "my" isolated by re-synthesis as "into *my*… house."
   using an ellipsis and a 250 ms internal gap, the word "my" post-dropped
   `rubberband=tempo=0.95` for weight.
4. **Takes:** three variants of beat 2 (ellipsis position, ±3% rate); comp take 3.
5. **Room:** interior-cottage reverb preset, close mic distance.
6. **A/B** against the flat render with eyes closed: the directed one should tell you
   she is furious and controlled without a single word changed.

## Verify

- [ ] Pick any rendered scene: no two adjacent lines within 3% measured tempo (duration
      ÷ word count) *and* 1 dB RMS of each other (run the check script).
- [ ] Every emotional line is beat-split: per-beat wavs + a comp record exist in the
      shotlist row; re-rendering from the row reproduces the shipped line.
- [ ] Eyes-closed test: a listener who hasn't seen the script names the emotion of 8/10
      directed lines correctly from audio alone.
- [ ] Breaths/gaps present where thought happens; no line longer than ~8 words shipped
      as a single unsplit synth call unless deliberately flat.
- [ ] All rate/pitch/energy moves are logged overrides on the locked voice-bible base
      (`voice-casting-consistency` untouched); post pitch moves ≤ ±1.5 st.
- [ ] Reactions/efforts placed as shotlist events and visible to `lip-sync`; scene
      room/distance chain applied as a non-destructive mix layer.

See also: `voice-casting-consistency.md`, `setup-windows.md`,
`../sound-design/dialogue-editing.md`, `../sound-design/dialogue-mix-master.md`,
`../pipeline/vo-lipsync-pipeline.md`, `../blender/lip-sync.md`,
`../blender/acting-performance.md`.
