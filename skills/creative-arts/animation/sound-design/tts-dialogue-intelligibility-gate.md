---
id: creative-arts.animation.sound-design.tts-dialogue-intelligibility-gate
name: tts-dialogue-intelligibility-gate
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, tts, dialogue, intelligibility, whisper, faster-whisper, wer, jiwer, pitch, prosody, librosa, qc, voice-over]
level: advanced
status: draft
description: "Gate synthesized dialogue with local Whisper: transcript vs script word error rate, pitch span for robotic reads, and context checks for non sequiturs."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# TTS dialogue intelligibility gate

**Goal:** prove each synthesized line is understood the way it was written before it
ships. Listening yourself fails: you know the script, so your ear fills in the words.
A speech recognizer doesn't know the script.

## Setup (local, CPU)

```
pip install faster-whisper jiwer
```

`WhisperModel("small.en", device="cpu", compute_type="int8")` transcribes a 3 s line
in about a second and pulls its weights from Hugging Face on first use. Put it in the
same environment that already has librosa.

## Per line

1. Transcribe with `beam_size=5, language="en"` and join the segment texts.
2. Normalise both texts: lowercase, hyphens to spaces, strip punctuation except
   apostrophes, collapse spaces. Then `jiwer.wer(script, heard)`.
3. Pitch span: `librosa.pyin(fmin=60, fmax=400)`, span = 12 · log2(p90 / p10) in
   semitones. A flat read measured 5.2 semitones; an expressive cast member 10.7; a
   professional animated benchmark about 28.
4. Store the previous line beside each row, so a reviewer reads exchanges and not
   isolated lines.

## Gate

- **WER over 0.10:** regenerate the line (new seed or reference) or rewrite it. Check
  each miss by ear; number formats ("12" for "twelve", "6 o'clock") are false
  alarms, so either spell numbers the way Whisper writes them or whitelist them.
- **Real misses look like this:** "shop" heard as "shot", "Clothes that fit" as
  "Close that fit", "frayed" as "afraid", "Cheers" as "Yours", "Mine's" as "Minds".
  These are words the TTS clips or merges. Fix them with a fuller sentence, a
  different word or a respelling, not by retrying the same take forever.
- **Pitch span far below the rest of the cast:** the voice reads robotic. Raise the
  model's exaggeration or emotion setting, or rewrite fragments into full sentences.
  Fragments give the model no phrase to shape.

## What the gate caught on a full re-voice

- On a 63-line re-voice with Chatterbox, 3 lines failed and passed on one
  regeneration each: "Oh! Oh, dear." heard as "plumb, oh dear", a lone "Oh!" heard
  as "Hey, oh", and one dropped word.
- **High exaggeration hallucinates.** Raising Chatterbox exaggeration to 0.9 for more
  pitch range made it repeat a sentence and add invented words ("None of this is
  normal. None of this is normal. The Pippl..."). Run this gate after any change to
  expressiveness settings; it catches the repetition as a high word error rate.
- Rewriting clipped fragments into full sentences raised the flattest character's
  pitch span from 5.2 to 6.3 semitones at the same settings.
- Normalise British spellings and number words before scoring, or "neighbour" and
  "eight hundred and forty-six" show up as false failures.
- Synthesize without squeezing lines to fit the shot. Time-stretching adds a robotic
  quality. Lengthen the shot to the line plus 0.5 s instead.

## What this gate cannot see

A line can transcribe perfectly and still not make sense. "Have we met?" answered by
"You can't leave, silly." scored zero errors on both lines. Pair this gate with a
read of each exchange in order and with `editorial.script-to-picture-audit`.

## Verify

On a 63-line episode: 55 lines passed, 6 were real misses and 2 were number formats.
The summary row is lines over threshold, mean WER and pitch span per speaker.
