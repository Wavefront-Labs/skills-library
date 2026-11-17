---
id: creative-arts.animation.voice-tts.voice-casting-consistency
name: voice-casting-consistency
category: creative-arts
field: animation
product: voice-tts
tags: [voice, casting, tts, consistency, kokoro, piper, chatterbox, voice-cloning, character, voice-bible, delivery, drift]
level: advanced
status: draft
description: "Cast and lock local TTS voices per character (Kokoro/Piper): the voice bible, fixed model/speed/pitch/FX, delivery direction, and preventing drift across episodes."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: Voice casting & consistency (per-character local TTS)

**Goal:** each character sounds the **same every episode, every season** — the audio
equivalent of the modeled-asset consistency law. A listener should recognize Chip from
one syllable in episode 7 exactly as in episode 1. With local, deterministic TTS
(Kokoro, Piper) this is achievable *by construction*: freeze the inputs and the output
is repeatable forever. Drift is always caused by changing something you forgot was a
variable.

## 1. Casting — match voice to character, not to "nicest voice"
Casting is a design decision, not a quality contest. Audition the catalogue against the
character's written voice-print (from the screenwriting voice bible):
1. **List the character's vocal traits** in words first: age, warmth vs coldness, tempo,
   register, the one defining colour (Chip = bright TV-host warmth with a one-frame
   crack; Dill = clipped, counting, young, sensible; Pidge = fast, high, sideways; Gran
   Wynn = older, dry, British mercy; Censors = processed, mouthless, "maintenance").
2. **Audition candidates on the same 3-4 test lines** — a calm line, an excited line, a
   threatening/quiet line. Kokoro's 9 US-English voices (Heart, Aoede, Puck, Michael,
   etc., graded C+ or better) and Piper's many onnx voices across locales are the pool;
   use a non-US locale (e.g. an en_GB Piper voice) when the character calls for it.
3. **Pick for distinctiveness across the cast**, not per-character in isolation. Two
   characters on neighbouring voices will blur in a mix; spread the ensemble across
   register and tempo so any two are instantly separable.
4. **Decide base engine per character.** Kokoro for the natural, expressive hero reads;
   Piper where its specific timbre or locale fits, or for speed on bulk/background
   lines. Record which engine in the spec — they are not interchangeable mid-series.

## 2. The voice bible (one locked row per character)
Store the cast as data the batch reads — the single source of truth
(`production/voices.json`). Lock the engine + model + params + FX the moment a
character's voice is approved:
```json
{
  "DILL":  {"engine":"kokoro", "voice":"am_michael", "speed":1.0,  "pitch_semitones":0},
  "CHIP":  {"engine":"piper",  "model":"en_US-lessac-high.onnx", "speaker":0, "length_scale":0.92, "fx":"crt_crackle"},
  "PIDGE": {"engine":"kokoro", "voice":"af_aoede", "speed":1.08, "pitch_semitones":2},
  "GRAN_WYNN": {"engine":"piper", "model":"en_GB-alba-medium.onnx", "speaker":0, "length_scale":1.12},
  "CENSOR":{"engine":"piper",  "model":"en_US-lessac-medium.onnx","speaker":0,"length_scale":0.9,"fx":"hold_music_processing"}
}
```
- One row = one locked identity. New episodes **read this file**; no character's params
  are ever typed ad-hoc into a command.
- **Never swap the model/voice mid-series** — it breaks identity even at the "same"
  settings, because the voice *is* the model.
- Keep the file in version control so a change to a voice is a reviewable, dated event.

## 3. Lock every variable, not just the voice
Drift creeps in through the parameters you didn't think of as part of the identity. All
of these must be fixed per character and applied identically every line:
- **Speed / rate** (Kokoro `speed`, Piper `length_scale`) — pace is identity; a faster
  read is a different character.
- **Pitch** (semitones; Kokoro has no pitch input, so pitch is a post-shift — lock the
  amount). Small moves only.
- **Expressiveness** (Piper `noise_scale` / `noise_w`) — leave at the approved value;
  these add variation, which is the enemy of consistency if they drift.
- **Sample rate / loudness normalization** applied before mixing — the same chain every
  time (Kokoro outputs 24 kHz, Piper ~22.05 kHz; resample to the project rate
  consistently).
- **FX chain** (below) — byte-for-byte the same processing.

## 4. Character-voice FX (identity on top of the base voice)
A base TTS voice gets a light, consistent processing chain per character, applied the
same every line, implemented as a fixed Python/ffmpeg/soundcraft chain keyed off `fx`
in the spec:
- **Chip:** subtle CRT crackle + needle-drop warmth + mild bitcrush = the "host" timbre.
  Keep it light — intelligibility first.
- **Censors:** telephone/hold-music band-pass + slight pitch-flatten + a touch of chorus
  = the processed, mouthless, "maintenance" voice.
- **Others:** mostly clean; small EQ to seat them in the mix.
Document the exact chain (filters + values) so it is reproducible; an undocumented FX
tweak is the most common silent drift.

## 5. Delivery direction (keeping performance in-character)
Consistency of timbre isn't enough — the *delivery* must stay in-character too. The
levers with deterministic TTS:
- **Punctuation is prosody.** Write VO lines with real commas, ellipses, em-dashes,
  question marks; "…" and "—" shape pauses and falls. The teleplay's trailing/overlap
  marks carry straight into delivery.
- **Per-line speed/pause overrides sparingly** (a slower, eerier Chip line) — but as a
  documented override on the locked base, not a new base. Record the override in the
  shotlist row, not in the voice bible.
- **Re-synthesize, don't hand-edit pitch.** If a read is wrong, change the input
  (phrasing, punctuation, the one override) and regenerate — editing the wav breaks
  repeatability.

## 6. If a stock voice isn't distinctive enough (upgrade path)
Only after the deterministic options are exhausted, and knowing it needs a torch /
Python 3.10 env:
- Fine-tune VITS (`generative/vits-finetuning`) on a target voice, OR
- Voice-conversion (`generative/storyteller-ml/.../seed-vc`) to recolor a Piper/Kokoro
  base into a bespoke character timbre.
Either way, **freeze the model once trained** — a frozen converted model is as
deterministic as a stock voice, and the same locking discipline applies.

### 6b. Prosody upgrade WITHOUT recasting (verified: cloning from the locked cast)
When the locked deterministic voices read flat (measured: pitch span over one sentence —
Kokoro ~69 Hz vs Chatterbox ~151 Hz at default settings), upgrade the *engine* while
keeping the *cast* by zero-shot cloning **from reference clips synthesized by the locked
voices themselves**:
1. Synthesize ~8–10 s of in-register reference speech per character with the locked
   Kokoro/Piper voice. The prompt sets timbre AND baseline affect — write a flat,
   even reference for a deliberately flat character.
2. Feed each clip as the clone prompt (`audio_prompt_path` in Chatterbox). Timbres
   survive; prosody comes from the new engine. Licence stays clean because the
   reference audio is your own synthetic output, not a recorded human.
3. Map shotlist emotion → the engine's expression params (Chatterbox: `exaggeration`
   0.30 flat … 0.90 panic; `cfg_weight` lower = slower, more deliberate). Clamp
   deliberately-even characters to low exaggeration — do not let the upgrade
   re-perform a character whose flatness is the point.
4. Keep the reference clips under version control next to the voice bible: they are
   now the identity. Re-cloning from the same clip is the new determinism boundary.
Gotchas (hit in production): CUDA-saved checkpoints need `torch.load(...,
map_location="cpu")` on CPU boxes; `torchaudio.save` defaults to float32 WAV
(format 3), which stdlib `wave`-based pipeline tools cannot read — save PCM16
(`encoding="PCM_S", bits_per_sample=16`). Fit overruns with ffmpeg `atempo` capped
~1.15 before it gets audible. pyin pitch-measurement fails on short breathy lines —
judge prosody on lines ≥ 3 s.

## 7. Continuity checks across episodes (catching drift early)
Drift is silent until a listener notices, so check for it deliberately:
- **A/B against the reference line.** Keep one approved "golden" line per character
  (the audition read that locked the cast). When you build a new episode, re-synthesize
  that golden line from the current spec and compare to the stored reference — any
  audible difference means a variable moved (a model update, a changed default, a new
  resample step).
- **Spot-check a line from an old episode.** Re-run it through the current pipeline; it
  should match the shipped audio. If it doesn't, the pipeline changed, not the
  character.
- **Watch the mix, not just the stem.** A voice can be consistent in isolation and
  still drift in perceived identity if the surrounding mix/loudness treatment changes.
  Normalize to the same loudness target every episode.
- **Pin tool versions.** A Piper/Kokoro/onnxruntime upgrade can subtly change output.
  Treat a voice-engine version bump like a model swap: re-audition and re-approve, or
  pin the old version for the series.

## 8. The rule
A voice is a locked asset like a model. Approve once → freeze engine + model + params +
FX in the voice bible → reuse forever. Consistency beats chasing a marginally better
read. Regenerate from locked inputs; never patch the audio.

## Verify
- [ ] Every speaking character has one locked row (engine, model/voice, speed, pitch,
      FX) in `production/voices.json`, under version control.
- [ ] Any two characters are instantly separable in a mix (spread across register/tempo).
- [ ] The batch reads the bible; no params typed ad-hoc per line.
- [ ] Re-synthesizing the same line from the locked spec is byte-stable (or audibly
      identical) across runs.
- [ ] FX chains documented with exact filters/values; sample rate + loudness normalized
      the same way every time.
- [ ] Per-line delivery overrides live in the shotlist row, not in the base spec; no
      hand-edited wavs.
- [ ] No model/voice swapped mid-series.

See also: `setup-windows.md`, `batch-vo.md`, `../storywriting/screenwriting-craft.md`.
