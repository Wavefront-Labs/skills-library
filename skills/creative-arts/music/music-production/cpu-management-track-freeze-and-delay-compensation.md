---
id: creative-arts.music.music-production.cpu-management-track-freeze-and-delay-compensation
name: cpu-management-track-freeze-and-delay-compensation
category: creative-arts
field: music
product: music-production
tags: [music-production, logic-pro, pro-tools, daw, track-freeze, delay-compensation, cpu-management, plugin-latency, low-latency-mode, buffer-size, commit, bounce-in-place, system-overload, pdc]
level: practitioner
status: draft
description: "Keep big Logic and Pro Tools sessions running: freeze and commit, buffer strategy, low-latency modes, plugin delay compensation and overload diagnosis."
sources: ["https://support.apple.com/guide/logicpro/ (Freeze tracks; Low Latency Monitoring mode; Plug-in latency compensation)", "https://www.avid.com/pro-tools (Pro Tools Reference Guide - Track Freeze, Commit, Delay Compensation, Playback Engine)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPU management, track freeze and delay compensation

**Goal:** large sessions that play without overloads and stay sample-aligned.

## 1. Freeze, commit and bounce-in-place
- **Logic**: Freeze button (enable in Track Header Components); Freeze mode **Pre Fader** (renders instruments and effects) or **Source Only** (renders the instrument; you can still change effects). Bounce in Place (Ctrl+B) for a permanent audio version.
- **Pro Tools**: **Track Freeze** (renders everything up to a chosen insert), **Commit** (renders to a new audio track, optionally hiding/deactivating the original), **Track Bounce**.
- Freeze virtual instruments and heavy effects once parts are settled.

## 2. Buffer strategy
- Tracking: low buffer (32-128 samples); disable heavy plugins on other tracks or use Low Latency mode.
- Mixing: high buffer (1024-2048) for maximum plugin headroom.
- **Logic Low Latency Monitoring** mode bypasses plugins with high latency on the record-enabled track path. Pro Tools has **Low Latency Monitoring** on supported interfaces and Dynamic Plug-In Processing (disables processing on silent tracks).

## 3. Delay compensation
- Plugins report latency (look-ahead limiters, linear-phase EQ add a lot). The DAW delays other tracks to keep everything aligned: keep **Plug-in Latency Compensation** set to **All** (Logic) / **Delay Compensation** on (Pro Tools).
- While tracking, compensation can add monitoring latency; temporarily bypass latency-heavy plugins.
- Pro Tools shows per-track delay in the mix window's delay compensation view; Logic shows latency in plugin info.

## 4. Diagnosing overloads
- Logic: CPU/HD meter (Performance meter) shows which core is maxed; a single heavy instrument on one track overloads one core - spread work or freeze. **Live track** (selected, record-enabled) runs at the I/O buffer; select an audio track during mixing to relieve the CPU.
- Pro Tools: System Usage window; increase H/W buffer, adjust CPU usage limit, enable Dynamic Plug-In Processing.

## Gotchas
- Freezing then editing MIDI: unfreeze first (forgotten frozen tracks play the old version).
- External hardware inserts with manual latency settings misaligning prints.

## Verify
- Session plays end to end without overload at the mixing buffer.
- Loopback/ping test: a click through the latency-heavy chain aligns with the dry click.
