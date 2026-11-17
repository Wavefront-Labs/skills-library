---
id: creative-arts.animation.voice-tts.coqui-xtts-v2-local-generation
name: coqui-xtts-v2-local-generation
category: creative-arts
field: animation
product: voice-tts
tags: [xtts, coqui-tts, voice-cloning, local-tts, tts-engines, multilingual-tts, python]
level: practitioner
status: draft
description: "Run Coqui XTTS-v2 locally for multilingual speech with a reference clip: install, Python API call, reference audio rules, GPU use, licence caveat and consistency."
sources:
  - https://github.com/coqui-ai/TTS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Coqui XTTS-v2 local generation

XTTS-v2 is an open-weights, multilingual text-to-speech model that conditions on a short reference recording of the target voice (zero-shot cloning). It runs through the Coqui TTS library.

## Status and licence (read first)
- The company behind Coqui wound down in early 2024; the original repository is no longer actively developed. The `coqui-tts` package on PyPI is a community-maintained fork at the time of writing, so check which package and version you are installing.
- The XTTS-v2 model is released under the **Coqui Public Model License (CPML)**, which restricts commercial use. Read the licence before using output in anything sold. If the project is commercial, treat XTTS as a prototyping tool, or choose a model whose licence allows your use.

## Install and run
```bash
python -m venv xtts-venv && . xtts-venv/bin/activate   # Windows: xtts-venv\Scripts\activate
pip install coqui-tts          # community fork; the old name is `TTS`
```
```python
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")  # or "cpu"
tts.tts_to_file(
    text="Day three in Hollow Creek.",
    speaker_wav="refs/narrator_ref.wav",   # 6+ s clean mono reference
    language="en",
    file_path="out/line01.wav",
)
```
The first call downloads the model weights; accept the licence prompt if shown. Output is 24 kHz.

## Reference audio rules
- Clean, single speaker, no music, no reverb. About 6-30 seconds works; more clean audio helps a little but returns diminish.
- Match the reference's emotion to the target line; the model copies energy and pace. Keep one reference per emotion if the character needs range.
- WAV mono, 22.05 or 24 kHz or above; normalise levels first.

## Consistency
- Output varies between runs because sampling is stochastic. Keep the same reference file, text normalisation and generation settings, and review multiple candidates.
- Store the reference file and settings in the voice bible (`voice-casting-consistency.md`).

## Gotchas
- CPU generation is slow for long text; split by sentence.
- Language code must be supplied and match the text.
- Very short lines can come out with clipped endings; pad with a clause or trim in editorial.

## Verify
- [ ] Licence checked for the intended use.
- [ ] Same reference gives acceptably similar timbre across ten lines.
- [ ] Output is converted to the project sample rate once, in one place.
