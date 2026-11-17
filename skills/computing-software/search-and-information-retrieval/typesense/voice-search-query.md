---
id: computing-software.search-and-information-retrieval.typesense.voice-search-query
name: voice-search-query
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [voice-query, whisper, multi-search, typesense]
level: advanced
status: docs-checked
description: "Transcribe a base64 audio clip into a Typesense query using voice_query_model (Whisper) and send it through multi_search; WAV format and ffmpeg conversion."
sources: ["https://typesense.org/docs/30.2/api/voice-search-query.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Voice query search

Typesense can take a short audio clip, transcribe it with a configured model, and use the text as the query. The audio is sent as base64 data.

## Configure the collection

Attach a voice model when creating the collection through the `voice_query_model` property, for example `"voice_query_model": {"model_name": "ts/whisper/base.en"}` next to the normal `name` and `fields`.

## Prepare the audio

The clip must be 16 kHz, 16-bit WAV. Convert with ffmpeg: `ffmpeg -i <your_file> -ar 16000 -ac 1 -c:a pcm_s16le voice_query.wav`. Then base64 encode it.

## Search

Use the multi-search endpoint, not the single-collection GET search, because the GET endpoint limits query text length and an encoded clip is long. The body is `{"searches": [{"collection": "products", "query_by": "name", "voice_query": "<base64 encoded audio file>"}]}`, POSTed to `/multi_search` with the `X-TYPESENSE-API-KEY` header.

A quick recording script from the docs uses sox: `sox -d -r 16000 -b 16 -c 1 -e signed-integer output.wav trim 0 5` records 5 seconds, which you pipe through `base64` into a curl request.

## Hardware

Like text embedding models, Whisper models run on a GPU when Typesense is installed with GPU support, or when a GPU-enabled instance is picked in Typesense Cloud.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Voice Query page (https://typesense.org/docs/30.2/api/voice-search-query.html). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
