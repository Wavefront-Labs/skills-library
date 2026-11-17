---
id: creative-arts.animation.blender.rendering-amd-hip
name: rendering-amd-hip
category: creative-arts
field: animation
product: blender
tags: [blender, rendering, amd, hip, eevee, gpu, headless, windows, radeon]
level: advanced
status: verified
description: "Render EEVEE Next on AMD (HIP/Vulkan) headless on Windows: samples/TAA, Standard view transform, abspath trap, film-transparent, shot-chunking."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: Rendering on AMD (RX 6900 XT, Windows, headless)

**Hardware:** AMD Radeon RX 6900 XT (RDNA2, 16 GB — some tools misreport 4 GB),
12-thread CPU, 32 GB RAM, Windows 11. No CUDA/OptiX (not Nvidia), so the whole pipeline
is built around **EEVEE Next** with **HIP** reserved for rare Cycles work. Open-source,
local, no gen-AI.

## 1. Which engine, which device

- **EEVEE Next = the workhorse.** Every cel/NPR shot renders here. GPU-accelerated on AMD
  via the **Vulkan** backend — fast, near-real-time. ~95% of frames go through it.
- **Cycles** only for the odd photoreal/FX element. On AMD use **HIP** (RX 6000-series is
  HIP-supported; keep Radeon Software current). Cycles on one GPU is slow for
  volumetrics — keep FX stylised and composite instead (see `fx.md`, `smoke-fire-fx.md`).

## 2. The verified EEVEE Next render settings

From `shotkit.cinematic_render()` — the shared finish every shot calls:
```python
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.view_settings.view_transform = 'Standard'   # NOT Filmic/AgX
scene.eevee.taa_render_samples = 48               # samples (TAA) — the quality/time dial
try: scene.eevee.use_raytracing = True            # EEVEE Next ray-traced GI/reflections
except Exception: pass                             # guard: not all builds expose it
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.fps = 24
scene.render.image_settings.file_format = 'PNG'
scene.frame_start, scene.frame_end = start, end
```
Why these:
- **`view_transform = 'Standard'`** is load-bearing for a cel look. Filmic/AgX roll off
  highlights and desaturate; Standard keeps emissive cel colours flat and saturated. The
  trade-off: Standard has **no highlight rolloff**, so anything above 1.0 clips to
  paper-white — the set/sky must be exposed *below* the subject or backgrounds blow out.
  (The pipeline enforces this with an exposure law that caps world/emissive strength
  before characters append.)
- **`taa_render_samples = 48`** is the main cost/quality knob for EEVEE Next. 48 is a
  clean cel frame; raise toward 64-128 only if you see TAA noise in soft shadows/DOF.
  More samples ≈ linear more time — this is the number to cut first when a batch is slow.
- **`use_raytracing = True`** enables EEVEE Next ray-traced GI/reflections; wrap it in
  `try/except` because older 4.x builds don't expose the attribute and it would crash the
  batch.
- **PNG** sequence (not a video container) so frames are per-frame recoverable and
  assembled later with ffmpeg; **1920x1080 @ 24fps** is the show spec.

## 3. film_transparent for comp

When a shot's FX/character layer is composited over a separately-rendered background, set
`scene.render.film_transparent = True` so EEVEE renders a straight alpha (transparent
background) instead of the world. Leave it **off** for a finished beauty shot that already
contains its set — a transparent film there just loses the sky. Decide per layer, not
globally.

## 4. The relative-filepath trap (the one that silently eats frames)

Blender resolves a relative `render.filepath` (and `//` paths) against the **opened
.blend's directory, not the cwd**. A relative out path can report `Saved`/`DONE`, exit 0,
and write frames somewhere you never look. Always abspath:
```python
outdir = os.path.abspath(outdir)
os.makedirs(outdir, exist_ok=True)
scene.render.filepath = os.path.join(outdir, "f_")
bpy.ops.render.render(animation=True)
```
`cinematic_render()` does this. Same rule for OpenVDB sim caches. This bit the first
beauty render — zero frames on disk despite a clean exit.

## 5. Enabling HIP headless (only for Cycles)

GPU prefs don't carry into background mode — enable the device **in Python** before a
Cycles render:
```python
cp = bpy.context.preferences.addons['cycles'].preferences
cp.compute_device_type = 'HIP'
cp.get_devices()                       # MUST call, or the device list is empty
for d in cp.devices:
    d.use = (d.type == 'HIP')          # GPU only; also enable CPU for HIP+CPU hybrid
bpy.context.scene.cycles.device = 'GPU'
```
Empty HIP device list headless = driver too old or `get_devices()` not called. EEVEE Next
needs no such dance — it uses the GPU via Vulkan automatically given a current driver.

## 6. Throughput — what costs time, and chunking

- EEVEE Next cel frames at 1080p/48 samples: sub-second to a few seconds each. A full
  episode is feasible on this one box.
- A 10-15 min episode @ 24fps = **14,400-21,600 frames**. Never render as one monolith —
  render in **shot chunks**, one `blender -b` per shot (see `blendercraft-headless.md`),
  each recoverable and parallelisable; assemble with ffmpeg.
- **What costs time**, roughly in order: TAA sample count; ray-tracing (GI/reflections);
  volumetrics (avoid — the single biggest hog, stylise instead); DOF at high samples;
  resolution. Drop samples and kill volumetrics before anything else.
- **VRAM:** 16 GB is plenty for cel scenes and modest sims; ignore the 4 GB misreport.
  Watch it only on dense Cycles/volume work.

## 7. Batch reliability — surviving a long overnight render

A full-episode batch runs for hours unattended; build it to survive a crash:

- **Resume cheaply:** because output is a PNG sequence with a stable `f_####` name per
  shot, a re-run can skip frames already on disk. Gate the render with a check: if the
  expected frame count for a shot is present, skip it. One crash at frame 9,000 shouldn't
  cost 9,000 frames.
- **One process per shot** (see `blendercraft-headless.md`): a GPU driver timeout (TDR)
  or OOM kills one shot, not the night. Loop the shotlist firing a fresh `blender -b` per
  shot; capture exit codes and retry the failures once at the end.
- **Driver TDR:** Windows resets a GPU that stops responding for ~2 s, which aborts a
  frame mid-render. Keep per-frame time well under that (cel frames are; heavy Cycles
  volumetrics are the risk) — another reason to stylise FX.
- **Denoise:** EEVEE Next cel frames at 48 samples rarely need a denoiser; a flat cel area
  is clean. If a soft shadow/DOF area shimmers across frames, raise TAA rather than
  denoising — a denoiser can smear the hard cel edges you want crisp.
- **Log + probe:** every shot prints its frame range and `DONE`; after the batch, probe
  each shot folder's frame count against the expected `end` before calling it rendered.

## In this pipeline

`series/production/blender/shotkit.py` `cinematic_render()` sets `BLENDER_EEVEE_NEXT`,
`Standard` view transform, `taa_render_samples=48`, guarded `use_raytracing`, 1920x1080 @
24fps PNG, abspaths the output dir, and calls `render.render(animation=True)` over the
shot's frame range. `render_shot.py` wires the shot build into it. The Standard-transform
exposure discipline (subject brightest, set/sky capped below 1.0) is what keeps cel
colour flat without blown backgrounds.

## Verify

1. **Engine/transform:** rendered frames show flat saturated cel colour (Standard), not a
   filmic desaturated roll-off.
2. **No blown BG:** sample the sky/set — below paper-white; the subject is the brightest
   thing in frame.
3. **Output lands:** PNGs in the abspath folder; `DONE` + empty folder = the relative-path
   bug.
4. **Samples:** at 48 the frame is clean; if soft areas shimmer across frames, raise TAA.
5. **Determinism:** re-render a frame from a clean headless launch → byte-identical.
6. **HIP (if used):** the Python snippet lists a HIP device headless; empty = driver/prefs.

Sources: Blender 4.5 GPU rendering & command-line manuals; AMD HIP on Windows (Radeon
Software).
