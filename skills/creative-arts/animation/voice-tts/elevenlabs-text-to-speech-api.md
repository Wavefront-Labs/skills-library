---
id: creative-arts.animation.voice-tts.elevenlabs-text-to-speech-api
name: elevenlabs-text-to-speech-api
category: creative-arts
field: animation
product: voice-tts
tags: [elevenlabs-api, elevenlabs, tts-engines, text-to-speech, voice-settings, rest-api, cloud-tts]
level: practitioner
status: draft
description: "Generate character dialogue with the ElevenLabs text-to-speech API: key handling, voice_id and model_id, voice settings, output formats, and repeatable lines."
sources:
  - https://elevenlabs.io/docs/api-reference/text-to-speech/convert
  - https://elevenlabs.io/docs/models
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# ElevenLabs text-to-speech API

Cloud TTS with a large voice library, voice cloning and a documented REST API. Check https://elevenlabs.io/docs for current model names, limits and pricing; they change often.

## Request shape (REST)
- Endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- Auth: header `xi-api-key: <KEY>`; keep the key in an environment variable, never in the repo or a script that is committed.
- JSON body: `text`, `model_id`, and optionally `voice_settings` (`stability`, `similarity_boost`, `style`, `use_speaker_boost`, `speed`), plus `language_code` and a `seed` for more repeatable output where supported.
- Query parameter `output_format` picks the encoding, for example an MP3 at 44.1 kHz / 128 kbps or raw PCM. For dialogue editing request PCM or the highest-quality option your plan allows, not a lossy MP3 that will be edited and re-encoded.

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"Day three in Hollow Creek.","model_id":"eleven_multilingual_v2"}' \
  -o line01.mp3
```
The official Python and JavaScript SDKs wrap the same call (`text_to_speech.convert`). Model IDs on offer have included multilingual and low-latency "turbo"/"flash" families; use the docs' model list rather than copying an ID from an old script.

Checked against ElevenLabs' API reference, SDK (`elevenlabs` 2.73.1) and models page on 2026-10-18: the endpoint, `xi-api-key` header, `model_id` (default `eleven_multilingual_v2`), `output_format` (default `mp3_44100_128`), `language_code`, `seed` and `voice_settings` fields exist as described; `VoiceSettings` has `stability`, `similarity_boost`, `style`, `use_speaker_boost` and `speed`; `client.text_to_speech.convert` exists. The models page then listed `eleven_v4`, `eleven_v4_turbo`, `eleven_v3`, `eleven_v3_conversational`, `eleven_multilingual_v2`, `eleven_flash_v2_5` and `eleven_flash_v2` (plus speech-to-speech and voice-design models), so the multilingual v2 ID in the example still works but is no longer the newest.

## Workflow rules for animation
1. Pick the voice once per character and store `voice_id`, `model_id` and settings in a voice bible (see `voice-casting-consistency.md`). Changing any of them changes the timbre.
2. Generate each line to its own file named by line ID (`vo-file-naming.md`), keep the request JSON beside it for re-generation.
3. Every generation is probabilistic. Generate 2-4 candidates per hero line and pick like a director (`vo-take-matching.md`).
4. Convert to the project's sample rate once and keep the original download as archive.
5. Mind rate limits and character quotas when batching (see `batch-tts-generation-from-a-script.md` for the loop); add retry with back-off on HTTP 429.

## Gotchas
- Long text in one request can drift in tone; split by sentence or beat.
- Numbers, acronyms and invented names are often mispronounced: use a pronunciation dictionary (`pronunciation-dictionaries-and-lexicons.md`).
- Plans differ in commercial rights and output quality; check the licence terms before using output in a commercial release.

## Verify
- [ ] Key comes from the environment and is not in version control.
- [ ] Voice id, model id, settings saved with each output.
- [ ] Output format is uncompressed or highest-quality for editing.
