---
id: creative-arts.music.music-production.interface-gain-staging-sample-rate-and-buffer
name: interface-gain-staging-sample-rate-and-buffer
category: creative-arts
field: music
product: music-production
tags: [music-production, recording, microphone-technique, interface-gain, buffer-size, sample-rate, bit-depth, latency, direct-monitoring, audio-interface, 24-bit, 48-khz, clipping, dbfs, headroom, round-trip-latency]
level: practitioner
status: draft
description: "Configure an audio interface for recording: sample rate and bit depth choice, preamp gain to sensible dBFS levels, buffer size vs latency, and direct monitoring."
sources: ["https://www.soundonsound.com/techniques/gain-staging-your-daw-software", "https://support.apple.com/guide/logicpro/audio-preferences-lgcpb3ab0d7a/mac", "https://www.avid.com/pro-tools (Pro Tools Reference Guide - playback engine)", "https://www.focusrite.com/ (interface user guides on direct monitoring and latency)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interface gain staging, sample rate and buffer

**Goal:** clean recordings with headroom and low enough latency to perform comfortably.

## 1. Sample rate and bit depth
- **24-bit** always (32-bit float if the interface supports it): ~144 dB of dynamic range means no need to record hot.
- **48 kHz** is the modern standard (video/broadcast compatible); 44.1 kHz fine for music-only; 88.2/96 kHz doubles CPU and disk for a debatable benefit. Choose at the session start and never change mid-project.

## 2. Preamp gain
- Set gain while the performer plays the **loudest** part. Aim for peaks around **-12 to -6 dBFS**; average around -18 dBFS (roughly 0 VU on analogue-modelled plugins).
- Never clip (0 dBFS on the converter is a hard ceiling); leave headroom for performance excitement.
- Pads: use the mic or interface pad on loud sources (kick, amps) instead of setting gain to minimum.
- Instrument inputs (Hi-Z) for guitar/bass DI; line inputs for keyboards and outboard.

## 3. Buffer size and latency
| Task | Buffer (samples) | Latency at 48 kHz (one way approx.) |
|---|---|---|
| Tracking with plugins on input | 32-128 | under 3 ms |
| Mixing | 512-2048 | not important |
- Round-trip latency also includes converter and driver overhead: check the DAW's reported value. Under ~10 ms round-trip is comfortable for most players.
- If the CPU can't cope at a low buffer: freeze/disable heavy plugins (look-ahead limiters, linear-phase EQ add latency), or use **direct monitoring**.

## 4. Direct monitoring
- Hardware monitoring in the interface (mixer app or a direct-monitor knob) gives near-zero latency; mute the DAW track's monitoring to avoid hearing a doubled, flanged signal.
- Downside: no plugins on the cue (some interfaces add DSP reverb/EQ for this).

## 5. Recording offset
- DAWs compensate for converter latency automatically if the driver reports it; verify with a loopback test (output a click into an input, record it, measure the offset). Adjust "recording delay" if needed.

## Gotchas
- Mixed sample rates in imported files play at the wrong speed/pitch if not converted.
- USB hubs and power-saving modes cause dropouts; connect directly and disable USB selective suspend.

## Verify
- Record a loud passage: peaks between -12 and -6 dBFS, no clip indicators.
- Loopback test shows recorded audio aligned to the timeline within a few samples.
