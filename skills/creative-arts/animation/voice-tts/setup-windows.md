---
id: creative-arts.animation.voice-tts.setup-windows
name: setup-windows
category: creative-arts
field: animation
product: voice-tts
tags: [piper, kokoro, rhubarb, tts, windows, setup, voice, onnx, wav, visemes, lipsync, batch]
level: advanced
status: draft
description: "Install and run local TTS (Piper, Kokoro) and Rhubarb on Windows: binaries, voice models, CLI synthesis to wav, and batch text->wav->viseme for an episode."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: Local TTS + visemes on Windows (Piper, Kokoro, Rhubarb)

**Why local:** natural neural voices that run **offline on CPU** (fast for short lines),
no cloud, no per-call cost, and fully deterministic — the same input makes the same wav
every time, which is what per-character consistency depends on. This replaces the
robotic Windows SAPI voices from the pilot. Torch-GPU is painful on this AMD/Windows
box, so the stack is deliberately torch-free: **Piper** (ONNX) and **Kokoro-82M**
(pure-CPU) for voice, **Rhubarb Lip Sync** for visemes. (Fine-tuned VITS / voice
conversion is a later torch-env upgrade; not needed to ship.)

## 1. Piper — install (we have Python 3.10)
```bash
py -3.10 -m venv <TOOLS_DIR>/piper-venv
<TOOLS_DIR>/piper-venv/Scripts/python -m pip install piper-tts
```
`piper-tts` ships a win_amd64 wheel + CLI. Alternative: the standalone Windows zip from
the **OHF-Voice/piper1-gpl** releases — unzip and run `piper.exe --help` (no Python
needed).

### Piper voice models
Each voice = **two files**: `<voice>.onnx` + `<voice>.onnx.json` (config). Download from
Hugging Face **rhasspy/piper-voices**. Keep them in `<TOOLS_DIR>/piper-voices/`. Examples:
`en_US-lessac-medium`, `en_US-ryan-high`, `en_GB-*` — many locales/qualities
(low/medium/high; higher = better and slower).

### Piper — generate a line
```bash
PY=<TOOLS_DIR>/piper-venv/Scripts/python
echo "Day three in Hollow Creek. And something is off." | \
  "$PY" -m piper -m <TOOLS_DIR>/piper-voices/en_US-ryan-high.onnx -f line01.wav
# multi-speaker model: add --speaker <N>
# pacing: --length_scale 1.1 (slower);  sentence gap: --sentence_silence 0.3
```
Output is a WAV (usually 22.05 kHz mono). `--noise_scale` / `--noise_w` tweak
expressiveness — small changes only, and lock them per character (see
`voice-casting-consistency.md`).

## 2. Kokoro — install and run (pure-CPU neural, higher quality)
Kokoro-82M is an 82M-param model (ALBERT text encoder + StyleTTS2 prosody + iSTFTNet
vocoder) that runs on CPU; ~9 US-English voices graded C+ or better (Heart, Aoede, Puck,
Michael, …). Two practical routes on Windows:
```bash
# A) Python package (torch-free path via onnxruntime):
py -3.10 -m venv <TOOLS_DIR>/kokoro-venv
<TOOLS_DIR>/kokoro-venv/Scripts/python -m pip install kokoro-onnx soundfile
# needs the model weights + voices pack (onnx + voices .bin) downloaded once to
# <TOOLS_DIR>/kokoro/ ; see the kokoro-onnx release assets.
```
```python
# minimal synth (kokoro-onnx): text -> 24 kHz wav
import soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("<TOOLS_DIR>/kokoro/kokoro.onnx", "<TOOLS_DIR>/kokoro/voices.bin")
audio, sr = k.create("Day three in Hollow Creek. And something is off.",
                     voice="am_michael", speed=1.0, lang="en-us")
sf.write("line01.wav", audio, sr)      # sr == 24000
```
- Kokoro output is **24 kHz**; Piper ~22.05 kHz. Resample both to the project mix rate
  (e.g. 48 kHz) the same way every time so levels/pitch stay consistent.
- Kokoro has **no pitch input** — do pitch shifts in post and lock the amount per
  character. `speed` controls pace.
- **Determinism:** the vocoder noise is seeded; same text + voice + speed → same wav.

## 3. Rhubarb Lip Sync — install and run (wav → visemes)
Rhubarb reads a wav (and optionally the dialog text) and emits mouth-shape cues — the
input our Blender lip-sync script (`build_pixel_talk.py`) keyframes from.
1. Download the **Rhubarb Lip Sync** Windows release (DanielSWolf/rhubarb-lip-sync),
   unzip to `<TOOLS_DIR>/rhubarb/`. It's a standalone `rhubarb.exe`, no install.
2. Generate cues:
```bash
R=<TOOLS_DIR>/rhubarb/rhubarb.exe
"$R" -f json -o line01.json line01.wav                 # basic
"$R" -f json -o line01.json --dialogFile line01.txt line01.wav   # better: give it the text
# --extendedShapes for the full A-H + X set (9 visemes); default is the 6 basic
```
Output JSON has `mouthCues` = `[{start, end, value}]` with values `A`-`H`/`X`. Blender
keyframes each viseme mesh's visibility from this with **constant interpolation** (hard
swaps). Passing the exact dialog text via `--dialogFile` sharpens alignment markedly —
always do it, since we have the line text from the shotlist.

## 4. Batch an episode's VO (the real workflow)
Drive the whole episode from the shotlist JSON + the voice bible — one wav + one viseme
JSON per dialogue line, named by a stable line id so shots can find them:
```python
# pseudo: for each line in EP01_shotlist.json -> synth with that character's locked
# voice -> rhubarb -> write <OUT>/EP01/<line_id>.wav and <line_id>.json
import json, subprocess, os
voices = json.load(open("production/voices.json"))
lines  = json.load(open("series/scripts/EP01_shotlist.json"))   # has {id, speaker, text}
OUT = "<OUT_DIR>/EP01"; os.makedirs(OUT, exist_ok=True)
R = "<TOOLS_DIR>/rhubarb/rhubarb.exe"
for ln in lines["dialogue"]:
    spec = voices[ln["speaker"]]
    wav  = f"{OUT}/{ln['id']}.wav"
    # ... synth wav via Piper or Kokoro per spec['engine'] (sections 1-2) ...
    txt = f"{OUT}/{ln['id']}.txt"; open(txt, "w").write(ln["text"])
    subprocess.run([R, "-f", "json", "-o", f"{OUT}/{ln['id']}.json",
                    "--dialogFile", txt, "--extendedShapes", wav])
```
- **Stable line ids** are the join key across teleplay → shotlist → wav → viseme JSON →
  shot. Don't rename them.
- Keep the text file beside each wav so Rhubarb (and later re-runs) always gets the
  dialog.
- Apply each character's locked FX chain (CRT crackle, censor band-pass) *after* synth,
  *before* Rhubarb only if the FX doesn't distort timing — band-pass is fine; heavy
  time-stretch would desync the visemes, so viseme off the clean wav then apply timbre
  FX to the final.

## 5. Piper vs Kokoro — which, when
- **Kokoro** for hero/foreground reads: more natural prosody and expression, 24 kHz,
  CPU-fine for a short line, but a slightly heavier dependency (weights + voices pack).
  Prefer it where delivery nuance matters.
- **Piper** for speed and breadth: huge voice/locale catalogue, tiny ONNX models, very
  fast on CPU, trivial standalone exe. Prefer it for bulk/background lines, non-US
  accents it covers well, and anywhere its specific timbre fits a character.
- You can mix engines across the cast — the voice bible records which engine each
  character uses; just never switch a given character's engine mid-series.
- Both are deterministic, so either supports the consistency law equally once locked.

## 6. Common Windows gotchas
- **`echo` on Windows pipes trailing/odd characters** into Piper in some shells; prefer
  writing the line to a `.txt` and piping that file in, or call the Python API directly,
  so punctuation reaches the model intact.
- **Path separators:** keep model/voice paths forward-slashed or properly quoted in the
  shell; a backslash before a quote can eat the quote.
- **First Kokoro run downloads/loads weights** — slow once, fast after; pre-warm before
  a big batch so timing numbers aren't skewed.
- **Rhubarb wants PCM wav.** If a synth step emits a float/odd-format wav, convert to
  16-bit PCM (ffmpeg) before Rhubarb, or cue detection gets flaky.
- **Sample-rate mismatch bites at mix time**, not synth time — resample everything to
  one project rate up front.

## 7. Expert tips
- `--length_scale`/`speed` >1 slows delivery (good for an eerie host); <1 speeds up.
- Punctuation drives prosody — write VO lines with real commas, ellipses, em-dashes,
  question marks; "…" and "—" shape pauses.
- Resample all TTS output to one project rate before mixing (see
  `../soundcraft/sfx-design.md`).
- Quality order for us: Kokoro / Piper now → fine-tuned VITS / voice conversion from
  `generative/` later (needs a torch env, Python 3.10).

## Verify
- [ ] `piper.exe --help` (or `-m piper`) runs; a test line writes a playable wav.
- [ ] Kokoro synth writes a 24 kHz wav; re-running the same text+voice+speed is
      identical.
- [ ] `rhubarb.exe` produces a `mouthCues` JSON; `--dialogFile` used for alignment.
- [ ] Visemes generated off the clean wav (not a time-stretched one) so they stay in
      sync; timbre FX applied after.
- [ ] A full episode batched to `<line_id>.wav` + `<line_id>.json` from the shotlist +
      voice bible, ids stable for the Blender lip-sync step.

See also: `voice-casting-consistency.md`, `batch-vo.md`,
`../scripting/scripting-basics.md` (keyframing visemes in Blender).
Sources: OHF-Voice/piper1-gpl; rhasspy/piper-voices (HF); kokoro-onnx; Kokoro-82M model
card; DanielSWolf/rhubarb-lip-sync; sherpa-onnx Piper docs.
