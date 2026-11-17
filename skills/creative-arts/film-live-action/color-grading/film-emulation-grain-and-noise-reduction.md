---
id: creative-arts.film-live-action.color-grading.film-emulation-grain-and-noise-reduction
name: film-emulation-grain-and-noise-reduction
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, colorist, colourist, film-emulation, print-emulation, film-look, film-print-lut, kodak-2383, fuji-3513, halation, bloom, film-grain, grain, grain-overlay, scanned-grain, procedural-grain, dehancer, filmconvert, film-look-creator, resolve-film-look-creator, color-density, subtractive-saturation, split-toning, gate-weave, noise-reduction, temporal-nr, spatial-nr, denoise, neat-video, resolve-noise-reduction, noise-vs-grain, chroma-noise, luma-noise, banding, dithering, texture, film-look-creator-use, print-lut, print-emulation-lut, grain-application, grain-settings, grain-plugins, halation-effect, bloom-effect, halation-technique, temporal-nr-settings, spatial-nr-settings, nr-settings, neat-video-use, third-party-nr, nr-plugins, subtractive-saturation-use, colour-density-use, film-density, split-toning-technique]
level: practitioner
status: draft
description: "Give digital footage film texture on purpose: print emulation LUTs and subtractive saturation, halation and bloom, correctly sized grain, and noise reduction in the right node order."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - Noise reduction, Film Look Creator, Film Grain chapters)"
  - "https://www.dehancer.com/ (Dehancer film emulation documentation)"
  - "https://www.neatvideo.com/ (Neat Video noise reduction guides)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Film emulation, grain and noise reduction

**Goal:** texture and colour behaviour that feel like photochemical film without the
tells of a cheap "vintage" preset - and a noise-reduction pass that cleans the sensor
without smearing skin, done in the right order.

## 1. Order of operations (one node chain)
`balance -> NR (temporal then spatial) -> secondaries -> film emulation (colour) ->
halation/bloom -> grain -> output`. Noise reduction first so it works on the sensor
noise, not on added grain; grain last so it isn't blurred or keyed; halation before
grain so grain sits on top of the glow.

## 2. Noise reduction
Digital noise is per-pixel, fine and chroma-heavy; film grain is clumped, luma-dominant
and larger. Remove the former before adding the latter.
- **Resolve** (Motion Effects palette): **Temporal NR** first - *Frames: 2-3*, *Motion
  Est.: Better/Faster*, *Motion Range: Medium*, *Luma/Chroma threshold* starting ~5-10
  (chroma higher) - it uses neighbouring frames and preserves detail; then **Spatial
  NR** - *Mode: Enhanced/Faster*, *Radius: Small/Medium*, *Luma 5-15, Chroma 15-30*,
  *Blend* 20-40% to keep texture. Watch at 100% on skin and hair; smearing in motion
  means temporal thresholds too high. NR on its own node, before the look; cache it.
- **Neat Video** (OFX in Resolve/Premiere/Avid): build a **noise profile** from a flat
  area of the actual clip (or a camera profile at that ISO), then adjust temporal
  (2-4 frames) and spatial amounts; best quality, slowest.
- Chroma noise is the ugly part and the cheapest to remove; be gentle on luma.
- Banding from heavy NR/grades in 8-bit sources: add tiny grain/dither before output.

## 3. Film emulation (colour)
Three properties distinguish print film from a Rec.709 LUT:
- **Subtractive saturation / colour density**: saturated colours get *darker* as they
  saturate (dyes absorb light) rather than brighter. Resolve's *Color Slice* /
  **Film Look Creator** (Resolve 19 OFX: film stock presets, *Color Density*, *Halation*,
  *Bloom*, *Grain*, *Gate Weave*) and Dehancer's *Film Density* model this. A cheap
  approximation: Lum vs Sat curve pulling saturation in highlights, *Sat vs Lum*
  slightly darkening saturated regions.
- **Print emulation LUTs** (Kodak 2383, Fuji 3513DI - shipped with Resolve under
  *Film Looks*): expect **Cineon log input** - put a Color Space Transform to Cineon
  Film Log (or use the LUT in a log timeline) before it; drive the look with the grade
  underneath, keep the LUT at reduced intensity if too much. A print LUT also sets
  contrast and shoulder; don't fight it with a second S-curve.
- **Tone**: film's soft shoulder/gentle toe; highlights roll to a slightly warm white,
  shadows to a cooler/denser black (*split toning* via Log wheels: a touch of warmth
  in highlights, cool in shadows, both low saturation).
- Negative stocks differ (Vision3 500T vs 250D) in grain and colour; pick one reference
  and keep it per show.

## 4. Halation and bloom
Halation = red/orange glow around bright highlights (light bouncing off the film base
into the red layer). Resolve: *Film Look Creator > Halation*, or ResolveFX **Glow**
with a warm tint, luma threshold high (only speculars), small radius, screen/add at
low opacity; **Bloom** is softer, neutral and wider. Keep it visible only on light
sources and strong backlights; halation on a face is a tell. Dehancer and FilmConvert
include stock-specific halation.

## 5. Grain
- **Source**: scanned film grain plates (Resolve's *Film Grain* OFX has stock presets
  35mm 200T/500T etc.; Dehancer/FilmConvert scan-based; commercial grain scans) beat
  procedural noise. Overlay via the OFX or on a track above in Overlay/Soft Light.
- **Size and amount**: grain is sized relative to resolution - set *Grain Size* for
  the delivery (a 2K grain at 4K looks like noise); 35mm grain is finer than 16mm.
  Typical starting points in Resolve Film Grain: *Grain Strength* 0.2-0.4, *Size* 0.5-1.0
  at UHD, *Saturation* 0.1-0.3 (colour grain is subtle on print), *Blur* slight.
- **Response**: film grain is strongest in the midtones, finer in highlights and
  coarser in deep shadows; the *Shadow/Mid/Highlight* amounts in the OFX model it.
- Grain must be **temporal**: changes every frame, never a static overlay (dead
  giveaway). Review at 100% at the delivery resolution and in a compressed preview
  (streaming encoders eat fine grain - a touch more than looks right in the suite is
  usual; some platforms accept film grain synthesis metadata instead).
- Apply once on an output node or a timeline node, after everything.

## 6. Keep it consistent
Build the look as a node group/LUT applied to every shot; adjust only the primary
beneath per shot. Shots with mismatched NR or grain amounts scream in a cut. Render
tests through the delivery codec before signing off texture.

## Gotchas
- Grain added before noise reduction or before a key - grain keyed, NR smears grain.
- Print LUT fed Rec.709 instead of Cineon log; crushed, over-saturated.
- Halation radius too large; the whole frame glows like a music video.
- Static grain overlay or grain at 50% strength on a 4K master; delivery QC flags noise.
- Temporal NR on fast motion with high thresholds; ghosting trails behind hands.

## Verify
- [ ] Node order: NR before look and grain; grain last.
- [ ] NR checked at 100% on skin and motion; chroma clean, luma textured.
- [ ] Film emulation uses density/subtractive behaviour and a log-fed print LUT if used.
- [ ] Grain sized for delivery resolution, temporal, consistent across shots; checked after encode.
