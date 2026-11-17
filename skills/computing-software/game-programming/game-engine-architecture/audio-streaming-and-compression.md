---
id: computing-software.game-programming.game-engine-architecture.audio-streaming-and-compression
name: audio-streaming-and-compression
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, audio-streaming, audio-compression, audio, game-programming]
level: practitioner
status: draft
description: "Choose audio loading and codecs: streamed vs decompressed-in-memory vs compressed-in-memory, Vorbis, Opus and ADPCM trade-offs, stream counts and seek latency."
sources: ["https://www.fmod.com/docs/2.03/api/core-guide.html", "https://opus-codec.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audio streaming and compression

**Goal:** fit audio in memory and CPU budgets while keeping latency low for gameplay sounds.

## Load modes (FMOD/Wwise terms)
| Mode | Memory | CPU | Use |
|---|---|---|---|
| Decompress on load (PCM in memory) | Highest | None at playback | Short, frequent SFX (footsteps, gunshots) |
| Compressed in memory, decode on play | Medium | Decode per voice | Medium SFX, many variations |
| Streamed from disk | Small buffer | Decode + I/O | Music, ambience, long dialogue |
FMOD: `FMOD_CREATESAMPLE` vs `FMOD_CREATECOMPRESSEDSAMPLE` vs `FMOD_CREATESTREAM`.

## Codecs
- **PCM:** no decode, huge.
- **ADPCM:** ~3.5:1, very cheap decode; good for SFX with many voices.
- **Vorbis:** ~10:1, moderate CPU; FMOD's FSB Vorbis is common on PC/console.
- **Opus:** excellent quality at low bitrates, used for voice chat and increasingly for game audio.
- **Platform hardware codecs:** XMA (Xbox), ATRAC9 (PlayStation) decoded in hardware, free CPU.

## Streaming considerations
- Each stream needs disk bandwidth and a decoder; limit concurrent streams (e.g. 8-16) and
  prioritise.
- Prefetch the start of streamed sounds that must start instantly (dialogue triggered by gameplay):
  keep the first few hundred ms in memory.
- Seeking compressed streams has latency; seek tables help.
- Streaming from compressed archives: store audio uncompressed in the pak (already compressed) so
  reads are direct.

## Budgets
Track decoded memory, compressed memory, voices and decode CPU per platform; set per-category quality
(Vorbis quality 0.4-0.6 for SFX, higher for music).

## Verify
- Profiler (FMOD Studio profiler, Wwise Advanced Profiler): stream starvation warnings, CPU per codec
  under a busy combat scenario.
