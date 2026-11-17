---
id: creative-arts.film-live-action.premiere-pro.effects-keyframes-masking-and-dynamic-link
name: effects-keyframes-masking-and-dynamic-link
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, effects, effect-controls, keyframes, keyframing, temporal-interpolation, spatial-interpolation, ease-in, ease-out, bezier, motion-effect, opacity, blend-modes, masking, masks, mask-tracking, track-mask, feather, warp-stabilizer, stabilization, speed-duration, time-remapping, speed-ramp, optical-flow, frame-blending, adjustment-layers, transitions, cross-dissolve, morph-cut, ultra-key, chroma-key, nest, dynamic-link, after-effects-round-trip, replace-with-after-effects-composition, audition-round-trip, edit-in-audition, render-and-replace, gpu-acceleration, effects-presets, keyframe-interpolation, easing, mask-tracking-use, mask-feather, warp-stabilizer-settings, stabilizer-methods, adjustment-layer-use, effect-preset-save, dynamic-link-ae, audition-link, transitions-use, morph-cut-use, default-transition, gpu-rendering, render-previews, speed-duration-use, time-remapping-use, frame-blend-use]
level: practitioner
status: draft
description: "Effects in Premiere Pro: eased keyframes in Effect Controls, masks and mask tracking, Warp Stabilizer rules, time remapping with optical flow, adjustment layers, Dynamic Link to After Effects."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/adding-navigating-setting-keyframes.html (Adobe - Keyframes)"
  - "https://helpx.adobe.com/premiere-pro/using/masking-tracking.html (Adobe - Masking and tracking)"
  - "https://helpx.adobe.com/premiere-pro/using/dynamic-link.html (Adobe - Dynamic Link)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional - Premiere Pro exam objectives, Domain 4)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effects, keyframes, masking and Dynamic Link in Premiere Pro

**Goal:** the fixes and moves an editor does every day - reframes, stabilisation,
speed ramps, a masked brightness lift, a comp sent to After Effects - done so they
render fast and survive a re-cut.

## 1. Effect Controls and keyframes
`Shift+5` opens **Effect Controls** for the selected clip: fixed effects (**Motion**:
position/scale/rotation/anchor; **Opacity** with blend modes; **Time Remapping**;
**Audio**) plus any applied effect.
- Click the stopwatch to enable keyframes; move the playhead and change the value to add
  one; `Ctrl/Cmd`-click the value's stopwatch area to add at the playhead.
- **Temporal interpolation** (right-click a keyframe): Linear, Bezier, Auto Bezier,
  Ease In/Out, Hold. Default to *Ease In/Ease Out* for any move the audience sees;
  open the value graph (triangle beside the property) to shape velocity.
- **Spatial interpolation** (for Position): Bezier curves in the Program Monitor for
  curved paths; Linear for straight.
- Scale a **4K clip in a 1080 timeline** by setting *Scale to Frame Size* off and
  *Set to Frame Size* (right-click) so punch-ins stay sharp - or use Motion scale on the
  native-resolution clip.
- Save **effect presets** (right-click effect name > Save Preset: Scale/Anchor to In/Out
  Point) for reusable moves (standard push-in, lower-third slide).

## 2. Masks and tracking
Under any effect (including Opacity, Lumetri, Blur) click the ellipse/rectangle/pen
icons to add a **mask**; set *Feather*, *Expansion*, *Inverted*. Track the mask with
the play button beside *Mask Path* (Position / Position+Scale / Position+Scale+Rotation;
*Faster* vs *More accurate*). Uses: brighten a face (Lumetri + mask), blur a logo or
licence plate (Gaussian Blur + tracked mask), vignette (Opacity mask inverted with
feather on an adjustment layer). Mask tracking is 2D and loses on occlusion - re-track
from the frame it fails.

## 3. Warp Stabilizer (rules)
`Video Effects > Distort > Warp Stabilizer`: analyses, then stabilises.
- *Result: Smooth Motion* for handheld takes; *No Motion* for lock-off attempts.
- *Method*: Subspace Warp (default; can wobble) -> Position, Scale, Rotation or
  Position only when it warps edges.
- *Smoothness* 5-20% for subtle; *Framing: Stabilize, Crop, Auto-scale* with
  *Maximum Scale* ~110-115% to limit zoom; check *Detailed Analysis* for difficult shots.
- Apply to a clip at its own speed and frame rate; it **can't coexist** with Speed/
  Duration changes on the same clip - nest first (`right-click > Nest`), then stabilise
  the nest or vice versa.
- Rolling-shutter jello: enable *Advanced > Rolling Shutter Ripple: Enhanced Reduction*.

## 4. Speed, ramps and optical flow
- `Ctrl/Cmd+R` **Speed/Duration**: percentage, reverse, *Maintain Audio Pitch*, *Ripple
  Edit, Shifting Trailing Clips*, and the **Time Interpolation** (Frame Sampling / Frame
  Blending / **Optical Flow** - best for slow-mo under ~50%, render to check artefacts).
- **Time Remapping** (Effect Controls > Time Remapping > Speed, or clip FX badge menu):
  add keyframes on the speed line, drag the halves of a keyframe apart to create a ramp,
  drag the blue handle for easing. Use for speed ramps inside a clip; expand the track
  height to see the rubber band.
- Export with the interpolation set; optical flow is CPU-heavy - *Render and Replace*
  once final.

## 5. Adjustment layers and transitions
`File > New > Adjustment Layer` (Project panel New Item) on a track above: Lumetri,
blur, vignette, film grain affect everything beneath for the duration. Trim it like a
clip. Transitions: `Ctrl/Cmd+D` default video (Cross Dissolve), `Ctrl/Cmd+Shift+D`
audio (Constant Power); set defaults in `Effects` panel right-click. **Morph Cut**
hides jump cuts in interviews (small gaps, straight heads only; render to judge).
**Ultra Key** for quick greenscreen (Key Color eyedropper, *Matte Generation* pedestal,
*Spill Suppression*).

## 6. Dynamic Link
- **To After Effects**: select clips > right-click > *Replace With After Effects
  Composition*. AE opens with a comp of those clips; the Premiere clip becomes a live
  link (changes in AE appear in Premiere on save). Keep AE and Premiere versions
  matched; store the AE project with the Premiere project. For heavy comps,
  *Render and Replace* in Premiere (keeps the link - *Restore Unrendered* to go back).
- **To Audition**: right-click audio clip > *Edit Clip in Adobe Audition* (creates a
  copy with "Audio Extracted", processed in Audition, updates on save) or *Edit in
  Adobe Audition > Sequence* for the whole mix (sends video reference and tracks).
- Dynamic-linked comps don't carry to a conform (XML/AAF) - render them before turnover.

## 7. Performance
`File > Project Settings > General > Renderer: Mercury Playback Engine GPU` so GPU-
accelerated effects (Lumetri, blur, Warp Stabilizer, transforms) play in real time;
yellow render bar = GPU real-time, red = render. `Sequence > Render In to Out`
(`Enter`) for the heavy sections; *Render and Replace* for permanent ones.

## Gotchas
- Linear keyframes on camera moves; mechanical look.
- Warp Stabilizer on a nested, speed-changed clip - "clip must not have speed changes".
- Optical flow on clips with fast motion or transparency; smeared artefacts.
- Dynamic Link project moved to another machine without the AE file.
- Effects stacked on clips rather than on one adjustment layer; a look change takes an hour.

## Verify
- [ ] Moves use eased keyframes; value graphs checked for velocity bumps.
- [ ] Masks tracked and reviewed at speed; occlusions re-tracked.
- [ ] Stabilised/retimed clips nested where needed and rendered-and-replaced when final.
- [ ] Dynamic-linked comps rendered before any XML/AAF turnover.
