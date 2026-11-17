---
id: creative-arts.animation.voice-tts.batch-tts-generation-from-a-script
name: batch-tts-generation-from-a-script
category: creative-arts
field: animation
product: voice-tts
tags: [tts-batch, batch-generation, tts-engines, shotlist, line-ids, retry, idempotent]
level: practitioner
status: draft
description: "Batch-generate TTS dialogue from a script file: line-ID manifest, idempotent runs, retry and rate limits, candidates per line, logging and QC before editorial."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Batch generation from a script

Generating hundreds of lines by hand does not scale. A small script that reads a structured dialogue list and calls the TTS engine gives repeatable, reviewable output. `setup-windows.md` covers the local Piper/Kokoro/Rhubarb version; `elevenlabs-text-to-speech-api.md` covers the cloud call.

## Input manifest
One row per line, with a stable ID (never reuse IDs), speaker, text and optional notes:
```
id,speaker,text,emotion
S014_L07,MIRA,"We should not be here.",tense
```
The speaker maps to a voice-bible entry holding engine, voice id, model and settings (`voice-casting-consistency.md`).

## Script rules
1. **Idempotent**: skip lines whose output file exists and whose text/voice/settings hash is unchanged. Re-running after a script change then regenerates only the lines that changed.
2. **Candidates**: N takes per line (for example 3) named `<id>_t01.wav` ... (see `vo-file-naming.md`) so a director can choose (`vo-take-matching.md`).
3. **Sidecar JSON** per output: text, engine, voice, settings, timestamp, hash. It is your audit trail.
4. **Retry** on transient errors with exponential back-off, honour HTTP 429/`Retry-After`, and cap concurrency to the provider's limits.
5. **Secrets** from environment variables only.
6. **Normalise** all outputs to the project sample rate and bit depth in one step; keep the raw download.

```python
# skeleton
import csv, hashlib, json, pathlib, time
for row in csv.DictReader(open("lines.csv", encoding="utf-8")):
    spec = voices[row["speaker"]]
    h = hashlib.sha1(json.dumps([row["text"], spec], sort_keys=True).encode()).hexdigest()
    meta = pathlib.Path(f"out/{row['id']}_t01.json")
    if meta.exists() and json.loads(meta.read_text())["hash"] == h: continue
    # call engine with retry here; write wav, then meta with {"hash": h, ...}
```

## QC pass
- Automatic: duration within expected range, no digital silence, peak below 0 dBFS, sample rate correct.
- Human: listen to every line once, flag mispronunciations into the pronunciation dictionary (`pronunciation-dictionaries-and-lexicons.md`), and regenerate.
- Run `tts-artifact-repair.md` for clicks and clipped endings.

## Verify
- [ ] Re-running with no changes generates nothing.
- [ ] Every output has a sidecar with hash and settings.
- [ ] Failed lines are listed in a report, not silently skipped.
