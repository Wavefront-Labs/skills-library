---
id: creative-arts.animation.motion-graphics.ae-multi-frame-rendering
name: ae-multi-frame-rendering
category: creative-arts
field: animation
product: motion-graphics
tags: [multi-frame-rendering, render-queue, after-effects, mfr, render-performance, cache, ram, expressions-performance, composition-profiler]
level: advanced
status: draft
description: "Speed up After Effects renders with Multi-Frame Rendering: enabling and tuning MFR, finding non-MFR effects and slow expressions, cache and RAM settings."
sources:
  - https://helpx.adobe.com/after-effects/using/multi-frame-rendering.html
  - https://helpx.adobe.com/after-effects/using/composition-profiler.html
  - https://helpx.adobe.com/after-effects/using/improve-performance.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-Frame Rendering

**Goal:** use all CPU cores when rendering AE comps. MFR (After Effects 22+) renders several frames in
parallel during Render Queue, AME and previews.

## Enabling and tuning

- Preferences - Memory & Performance: **Enable Multi-Frame Rendering** (on by default). "CPUs reserved
  for other applications" keeps the machine usable; AE adjusts the number of concurrent frames
  automatically based on RAM and CPU.
- RAM: MFR needs memory per concurrent frame; more RAM means more parallel frames. Disk cache on a fast
  SSD (Media & Disk Cache) helps previews.

## Finding what slows it

- **Composition Profiler** (the stopwatch icon in the timeline, AE 23+): shows render time per layer and
  effect, so you can target the worst layers.
- Effects not supporting MFR force serial rendering for that comp; Adobe maintains a list of MFR-
  supported effects and third-party plugins must be updated for MFR.
- Expressions: per-frame expensive expressions (loops over many layers, `sampleImage`, reading
  `sourceRectAtTime` repeatedly) and expressions referencing "previous frame" state are slow; legacy
  ExtendScript expression engine is slower than JavaScript engine (Project Settings - Expressions).

## Habits that render fast

- Pre-render heavy, static precomps (Import & Replace Usage) instead of re-rendering them every frame.
- Avoid unnecessarily high-res nested comps scaled down.
- Disable effects not visible in the final (motion blur on static layers, unused layers set to guide).
- 32 bpc only where needed.

## Gotchas

- Third-party plugins that are not MFR-safe can crash or render inconsistently; update them or render
  those comps with MFR off.
- Render on the farm with `aerender` uses MFR as well, with the same preferences of the user account.

## Verify

Render a 10-second test with MFR off and on, note times in the Render Queue log; the Composition
Profiler shows the remaining hotspots after optimisation.
