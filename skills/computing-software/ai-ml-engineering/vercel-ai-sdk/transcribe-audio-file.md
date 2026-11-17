---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.transcribe-audio-file
name: transcribe-audio-file
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [transcription, transcribe, audio, whisper, download-limits, speech-to-text]
level: practitioner
status: docs-checked
description: "Transcribe an audio file or URL with transcribe, read text and segments, cap URL download size, and handle NoTranscriptGeneratedError."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/transcription
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn recorded audio into text with `transcribe`.

```ts
import { transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
});
```

`audio` may be `Uint8Array`, `ArrayBuffer`, `Buffer`, a base64 string, or a `URL`.

Result: `transcript.text`, `segments` (start/end times, if available), `language` (for example en, if available), `durationInSeconds` (if available), and `warnings` (for example unsupported parameters).

Provider options: `providerOptions: { openai: { timestampGranularities: ['word'] } }`.

URL audio and size limits:
- When `audio` is a URL and the model has no native URL transcription (Groq has it, and its provider fetches the URL directly), the SDK downloads the file with a default 2 GiB limit. Supplying `download` always uses local downloading.
- Lower it: `download: createDownload({ maxBytes: 50 * 1024 * 1024 })` (import `createDownload` from `ai`).
- Or supply `download: async ({ url }) => ({ data: new Uint8Array(await res.arrayBuffer()), mediaType: res.headers.get('content-type') ?? undefined })` to fetch with auth.
- Exceeding the limit throws `DownloadError`; test with `DownloadError.isInstance(error)`.
- Pair with `abortSignal: AbortSignal.timeout(5000)` to bound slow downloads. `headers` adds custom request headers.

Errors: `NoTranscriptGeneratedError.isInstance(error)` (AI_NoTranscriptGeneratedError) means the model produced nothing or an unparseable response. It carries `responses` (timestamp, model, headers) and `cause`; log both.

Telemetry: pass `telemetry: { functionId: 'transcribe-customer-call' }`. Raw audio is never put in telemetry events; set `recordInputs: false` or `recordOutputs: false` to withhold fields. If URL download or decoding fails, the start event still fires before the error event but audio byte length and media type may be undefined.

Models listed include OpenAI `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize`; ElevenLabs `scribe_v2`; Groq `whisper-large-v3-turbo`; Deepgram `nova-3`; AssemblyAI `universal-3-pro`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Qualified the 2 GiB URL download default: it applies when the model has no native URL support, and supplying download always downloads locally.

Method: documentation only; no commands were run.
