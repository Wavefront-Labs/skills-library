---
id: creative-arts.animation.motion-graphics.glitch-scanline
name: glitch-scanline
category: creative-arts
field: animation
product: motion-graphics
tags: [motion-graphics, glitch, scanline, static, vhs, crt, datamosh, compositor, blender, ffmpeg, dead-channel]
level: advanced
status: verified
description: "The stylized 'signal breaks' look: gold-peel-to-gray stutter, a crawling green scanline (drawbox y=f(t)), static/noise and horizontal tear, done in comp."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# glitch-scanline — the "it's all a broadcast" break

**Goal:** the show's signal-break beats — the gold light **STUTTERS** (gold peels
back to flat gray, a green scanline crawls up, static roars, then it's gone), and
the Act-5 unrendered/dead-channel edge. A reusable glitch vocabulary that lands as a
real broadcast fault, not a cartoon "hacking" effect. The whole power is in
**brevity and hard cuts** — the unsettle is in how fast it's over.

## In this pipeline

Grounded in `series/production/build_fx.py` → `glitch(out, d=2.5)`, the verified
ffmpeg builder (1920x1080 @ 24fps, no gen-AI). Palette from that script: gold
`#e0a93b`, flat broadcast gray `#8c8c8c`, glitch-green `#19e36b` (a hotter mint than
the HUD's `#5fe39b`, so the scanline pops). Built as one `-vf` chain over an `lavfi`
color source; the final assembly splices the clip in on the glitch frames.

## The gold-peel-to-gray stutter (the key beat)

Swap/blend to the degraded "unrendered" state, then let the gold fault back:

1. **Flatten to gray** — fill the frame with `#8c8c8c`
   (`drawbox=...:color=0x8c8c8c:t=fill`). This is the "gold grade dropped" state:
   the warm look peels off to a dead, flat broadcast gray.
2. **Gold flash / the peel** — a hard gold frame at the very start, then a half-alpha
   gold, timed by `enable`:
   ```
   drawbox=...:color=0xe0a93b:t=fill:enable='lt(t,0.18)',
   drawbox=...:color=0xe0a93b@0.5:t=fill:enable='between(t,0.18,0.34)'
   ```
   Full gold for <0.18s, then a 0.18–0.34s half-strength gold, then it's gone — the
   light "peeling back." `enable` gates a filter to a time window; use it (not alpha
   ramps) when you want **hard in/out** with no ease.

## Crawling green scanline (drawbox y = f(t))

A horizontal green band that scrolls up and wraps, driven by time in the `y`
expression:

```
drawbox=x=0:y='h-mod(t*620\,h+60)':w=1920:h=6:color=0x19e36b:t=fill,
drawbox=x=0:y='h-mod(t*620\,h+60)+10':w=1920:h=2:color=0x19e36b@0.5:t=fill
```

- `y = h - mod(t*620, h+60)` — starts at the bottom and climbs `620 px/s`; `mod(...,
  h+60)` wraps it past the top so it loops seamlessly. The comma inside `mod` is
  **escaped** `\,` so libavfilter doesn't read it as an argument separator.
- Two bands: a solid 6px line plus a fainter 2px trailing line 10px below at half
  alpha — the pair reads as a scanning beam, not a painted stripe.

## Horizontal tear + static

- **Scanline tear** via `geq`:
  `geq=lum='lum(X,Y)*(0.8+0.2*sin(Y*1.2))':cb='cb(X,Y)':cr='cr(X,Y)'` — luma
  modulated by a sine of Y (a coarser, harsher banding than the title card's; chroma
  untouched). This is the CRT line structure under the whole effect.
- **Static roar** — `noise=alls=26:allf=t+u`. A strong noise (strength 26) with
  `allf=t+u` = both **t**emporal (re-randomised each frame) and **u**niform, so it
  boils like dead-channel static rather than a frozen grain.

## The discipline — keep it short, snap in/out

- A stutter is **1–3 frames** at 24fps (≈ 0.04–0.12s) when used as a tear over a live
  shot; the standalone FX clip above runs longer because it *is* the shot. Over a
  rendered shot, keep the full-strength break to a blink.
- **Hard cuts, no ease.** Gate with `enable='between(t,a,b)'` / constant-interpolation
  keyframes, never a smooth fade — the glitch is jarring *because* it doesn't ramp.
- **Snap back clean.** The frame after the glitch must be the untouched render; a
  lingering half-effect kills the "it was never there" unease.

## Blender compositor route (tracks the render, preferred over a shot)

When the glitch rides over a rendered shot (not a full-frame FX card), do it in comp
so it sits under the same beauty grade:

- A **Mix** node blends the clean render with the degraded stack:
  **Lens Distortion** (dispersion, for a 1-frame RGB tear) + a scrolling
  **Wave/Gradient** texture for the green scanline + a **Noise** texture `ADD`ed for
  static + an RGB split via three **Translate + Combine**.
- Drive the Mix `Fac` with a **keyframed value = 1 only on the glitch frames**, set
  to **CONSTANT interpolation** so it pops on/off with no blend.
- This keeps the glitch under the shot's lens distortion/grade, so it reads as a
  fault in the same image, not a sticker on top.

## Dead-channel static (Act-5 void)

A flat emissive gray panel driven by an **animated Noise texture** (`Fac` → emission)
so it shimmers *in motion* (a frozen noise texture reads as dirt, not signal). Keep
emission **strength low** so it reads as a dead channel, not a light source — it
should fall under the Fog Glow threshold and *not* bloom. (Already prototyped in the
edge-set build.)

## RGB split / chroma tear (exact)

For a 1-frame colour tear in ffmpeg, split channels, offset one, and recombine:

```bash
rgbashift=rh=-6:bh=6:enable='between(t,0.5,0.54)'
```

`rh=-6` shifts red -6px, `bh=6` shifts blue +6px (green stays), `enable` gates it to
a single frame window. In the Blender compositor the same effect is three
**Translate** nodes (one per channel, a few px apart) feeding a **Combine Color** —
or just the Lens Distortion `dispersion` cranked for one frame. Either way: one or
two frames only, hard-gated.

## Splicing the glitch segment back in

When the glitch is built as its own short clip (like `glitch()`), cut it into the
picture with the **concat demuxer** at a shot boundary (matched codec/fps/pixfmt, see
`creative-arts.animation.encode-delivery.probe`), never a cross-fade — a `xfade`
would ease the very thing that must snap. If the glitch is a per-frame-range filter
over a continuous shot, apply it with `enable='between(t,a,b)'` so the surrounding
frames stream through untouched.

## Sound ties the break together

A glitch beat reads twice as hard with a 1–3-frame **static burst / digital crunch**
on the audio, hard-cut in and out on the same frames as the picture (the roar that
the `noise` filter implies). Mismatched timing between the visual tear and the audio
hit instantly reads as cheap — cut them on the identical frame.

## Reusable glitch vocabulary

Mix and match, always brief and hard-cut: grade-drop (gold→gray), RGB/chroma tear,
crawling scanline, line-boil static, 1-frame black/white flash, horizontal slice
offset (`crop`+`overlay` a band shifted X), and the dead-channel shimmer panel.

## Verify

- [ ] Each break is a blink (1–3 frames over a shot), **hard in/out** (`enable` or
      CONSTANT keys, no ease).
- [ ] Gold genuinely drops to flat `#8c8c8c` gray on the fault frames.
- [ ] Green `#19e36b` scanline crawls up and wraps smoothly (comma in `mod` escaped);
      twin band reads as a beam.
- [ ] Static boils (`allf=t+u`) — not a frozen grain; brief, not a wash.
- [ ] The frame after the glitch is the untouched render (clean snap-back).
- [ ] Dead-channel panel shimmers in motion, low emission, does **not** bloom.

status draft: `glitch()` and the dead-channel panel are verified (built in
`build_fx.py` / the edge-set build); the full stutter beat is not yet timed into a
rendered shot. See
`creative-arts.animation.motion-graphics.title-cards`,
`creative-arts.animation.blender.compositing-grade`.
