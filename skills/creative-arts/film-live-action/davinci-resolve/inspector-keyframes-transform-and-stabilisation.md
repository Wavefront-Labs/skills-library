---
id: creative-arts.film-live-action.davinci-resolve.inspector-keyframes-transform-and-stabilisation
name: inspector-keyframes-transform-and-stabilisation
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, inspector-keyframes, resolve-stabilisation, inspector-transform, keyframe-curves, dynamic-zoom, cropping, lens-correction, retime-in-inspector]
level: practitioner
status: draft
description: "Use Resolve's Inspector on the Edit/Cut pages: transform, crop and dynamic zoom, keyframing with curves, stabilisation settings, lens correction, and when to do it on the Color page instead."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Inspector, Keyframe editor, Stabilization)"
  - "The Definitive Guide to DaVinci Resolve (Blackmagic official training) - Edit page effects"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inspector: keyframes, transform and stabilisation

**Goal:** reframes, push-ins and stabilised shots done in the edit that survive into the
finish without quality loss.

## 1. Transform and crop (Inspector > Video)
- **Zoom, Position, Rotation, Anchor Point, Pitch/Yaw, Flip**; **Cropping** (left/right/
  top/bottom, softness).
- Reframing high-res sources (6K/8K) in a 4K/HD timeline: set *Project Settings > Image
  Scaling* (Input scaling: scale to fit/fill/ crop) so zooms use the source resolution -
  "super scale" only when upscaling.
- **Dynamic Zoom**: a two-point Ken Burns move (start/end rectangles in the viewer;
  ease options).

## 2. Keyframing
- Click the **keyframe diamond** next to a parameter to set a keyframe; move playhead,
  change value -> new keyframe. Navigate with the arrows beside the diamond.
- Open the **keyframe editor** on the timeline clip (curve icon) to see keyframes and
  **curves** - right-click a keyframe for **Ease In/Out/Linear**; use the curve editor for
  bezier shaping.
- Keyframe several parameters together (position + zoom) for a smooth digital push.

## 3. Stabilisation
- Inspector > **Stabilization**: modes **Perspective**, **Similarity**, **Translation**;
  **Camera Lock** (lock off fully), **Zoom** (auto-crop to hide edges), **Cropping Ratio**,
  **Smooth** and **Strength** sliders. Click **Stabilize** to analyse.
- Lower smoothing keeps intentional camera movement; Camera Lock for locked-off look.
- Rolling shutter jello can't be fixed by stabilisation - consider Fusion/ third-party.

## 4. Lens correction
Inspector > **Lens Correction** (distortion) for wide-angle barrel; the Color page has
more precise tools.

## 5. Edit page or Color page?
The Color page has its own **Sizing** (Edit sizing vs Input sizing) and **Tracker
> Stabilizer**; colourists often prefer to stabilise/reframe there. Agree who owns
reframes: Edit-page transforms carry through to Color as "Edit sizing"; XML/AAF to other
apps may not translate keyframed transforms reliably - bake complex moves or document them.

## Gotchas
- Zooming into HD proxies and judging sharpness - check on full-res media.
- Linear keyframes giving robotic moves; ease them.
- Stabilise Zoom cropping more than expected on shaky shots.
- Transforms lost in an XML round trip to another NLE.

## Verify
- [ ] Image scaling settings appropriate for the source/timeline resolution.
- [ ] Keyframes eased; curves checked.
- [ ] Stabilisation mode and smoothing chosen; crop acceptable.
- [ ] Ownership of reframes agreed (Edit vs Color) and documented for handoff.
