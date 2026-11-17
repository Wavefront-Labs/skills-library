---
id: creative-arts.animation.pipeline.vo-lipsync-pipeline
name: vo-lipsync-pipeline
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, vo, tts, kokoro, piper, rhubarb, lip-sync, ffmpeg, visemes]
level: practitioner
status: verified
description: "Full local VO-to-lip-sync chain: Kokoro/Piper TTS to Rhubarb visemes to Blender mouth keys to ffmpeg mux (verified commands)."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: VO → lip-sync → clip pipeline (verified end-to-end)

Turn a script line into a **non-robotic voice** + a **mouth that matches**, in a
rendered clip. This is the chain that fixes the two cardinal failures (robotic TTS,
mouths not matching). Verified 2026-10-12 on a production character.
Tools: Piper (neural TTS) · Rhubarb (viseme detection) · Blender (mouth) · ffmpeg (mux).

## 0. Environment (verified paths)
- **Python 3.10:** `py -3.10`
  (3.14 has no torch/onnx wheels; use 3.10). Install once: `python -m pip install piper-tts`.
- **ffmpeg:** `/c/ffmpeg/bin/ffmpeg` (ffmpeg 8). On PATH as `ffmpeg`.
- **Blender:** `<BLENDER_EXE>`.
- **Rhubarb:** install by downloading the GitHub release zip (below) → `<TOOLS_DIR>/rhubarb/...`.

## 1. Voice (Piper) — neural, non-robotic
Download a voice (`.onnx` + `.onnx.json`) from HF `rhasspy/piper-voices`:
```
base=https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/medium/en_US-ryan-medium
curl -sL -o voice.onnx "$base.onnx"; curl -sL -o voice.onnx.json "$base.onnx.json"
```
Generate (invoke as a MODULE — `python -m piper`, the `piper.exe` script isn't on PATH):
```
echo "A new viewer! No, better than that. Welcome to the show, Ivy!" | \
  "$PY" -m piper -m voice.onnx -f out.wav
```
Output = mono 16-bit PCM WAV @ 22050. Tuning: `--length_scale 1.1` (slower/warmer),
`--speaker N` (multi-speaker models). **Voice-casting:** lock one voice file per
character (consistency law) — see `../piper-tts/voice-casting-consistency.md`.
Duration check: `python -c "import wave;w=wave.open('out.wav');print(w.getnframes()/w.getframerate())"`.

## 2. Visemes (Rhubarb)
Install: latest Windows release is a zip (~87 MB):
```
url=$(curl -sL https://api.github.com/repos/DanielSWolf/rhubarb-lip-sync/releases/latest \
  | grep -oiE "https://[^\"]*-win[^\"]*\.zip" | head -1)
curl -sL -o rhubarb.zip "$url"; tar -xf rhubarb.zip -C <TOOLS_DIR>/rhubarb
```
Run (flags are exact — `-d/--dialogFile` NOT dialogueFile; extended shapes give G/H/X):
```
rhubarb.exe -f json -r pocketSphinx -d line.txt --extendedShapes GHX -o line.rhubarb.json line.wav
```
`line.txt` = the spoken text (improves accuracy a lot). Output JSON = `mouthCues`:
`[{start,end,value}]` where value ∈ **A B C D E F** (basic) + **G H X** (extended).
Meaning: A=closed(M/B/P) · B=slightly open · C=open(E) · D=wide open(ah) ·
E=rounded(O) · F=pucker(U/OO) · G=F/V · H=L · X=idle/rest.

## 3. Mouth in Blender (9-viseme swap, constant interp)
For a **screen/drawn face** (Pixel): build 9 emissive mouth objects (one per shape)
and keyframe VISIBILITY from the cues — NOT an oscillator (the pilot's bug), NOT
shape-key morphs. Open shapes = scaled emissive torus rings; closed (A/X) = a bezier
smile curve. For a **modeled organic mouth** (Ivy): map the 9 shapes to shape keys
on the face mesh instead (see `../blender/lip-sync.md`), same cue→frame timing.
```python
f = max(1, round(cue['start']*FPS) + 1)          # cue start → frame (24fps)
for k,obj in V.items(): obj.hide_viewport=obj.hide_render=(k!=active); keyframe both
# then set every keyframe interpolation = 'CONSTANT'  (hard swaps, holds the shape)
```
Verified builder: `series/production/blender/build_pixel_talk.py` (loads the locked
asset, replaces the static mouth, animates, renders a PNG seq). Render EEVEE Next,
view_transform Standard, fps 24, frame_end = round(duration*fps).

## 4. Assemble + mux (ffmpeg — fast path)
```
ffmpeg -y -framerate 24 -i f_%04d.png -i line.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -shortest out.mp4
```
`-pix_fmt yuv420p` = players/YouTube compatibility; `-shortest` trims to audio.
For real **editing** (cuts, multi-shot timeline) use filmcraft (project/sequence API:
`commands`, `run script.jsonl`, `export`), not ffmpeg. ffmpeg is for single-shot
assemble/mux. **Probe every output** (`filmcraft probe out.mp4`).

## 5. Measure the read, don't trust the ear
Two numbers per character, run over every line after synthesis and again after any
recast, written into the episode scorecard (`episode-qc-cold-viewer`):
- **Pitch span**: `librosa.pyin(fmin=60, fmax=400)`, voiced frames only, 10th→90th
  percentile in semitones (`12·log2(hi/lo)`), mean per character. Below ~4 a directed
  character reads as a robot whatever the timbre (a lead measured 1.6 against 7–9 for
  the rest of the cast and ~28 for a dialogue slice of the benchmark show). The fix is
  the synthesiser's expressiveness control with a per-character floor, not EQ.
- **Loudness**: `ffmpeg -af ebur128 -f null -`, integrated `I` per line; more than 6 LU
  between one character's lines reads as a different take. Measure only files the
  shotlist names — stray tests and backups in the folder produce false reds.
pyin lives with the synthesiser's venv (librosa), not the pipeline's interpreter; QC
shells out to it and reads JSON back.

## Pitfalls (hard-won)
- `piper.exe` not on PATH → call `python -m piper`.
- Rhubarb flag is `-d`/`--dialogFile` (singular, no "ue"); wrong flag = "Invalid command line".
- Without `--extendedShapes`, you only get A–F (no G/H/X idle) — rest pose looks wrong.
- Oscillating/looping a single mouth = the amateur tell. Drive from REAL cues.
- Non-constant keyframe interp = mouths tween through wrong shapes. Set CONSTANT.
- VO FIRST: generate voice before animating — it sets the true shot duration + the cues.

Cross-refs: `../piper-tts/setup-windows.md`, `../piper-tts/voice-casting-consistency.md`,
`../blender/lip-sync.md`, `../filmcraft/probe.md`.
