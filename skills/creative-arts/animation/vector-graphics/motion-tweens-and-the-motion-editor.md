---
id: creative-arts.animation.vector-graphics.motion-tweens-and-the-motion-editor
name: motion-tweens-and-the-motion-editor
category: creative-arts
field: animation
product: vector-graphics
tags: [motion-tween, motion-editor, animate, tweening, property-keyframes, motion-path, adobe-animate]
level: practitioner
status: draft
description: "Animate symbols with motion tweens in Adobe Animate: tween spans, property keyframes, motion paths and the Motion Editor panel versus classic tweens."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Motion tweens and the Motion Editor (Adobe Animate)

Motion tweens animate properties of **symbol instances** (and text fields) over a tween span, with property keyframes rather than full keyframes.

## Basics
1. Put a symbol instance (movie clip, graphic or button) on a layer, right-click it > Create Motion Tween. The layer span turns into a tween span (blue).
2. Move the playhead and change position, scale, rotation, skew, colour effects or filters; Animate records **property keyframes** (a diamond for each).
3. Dragging the object adds a **motion path**, an editable bezier, shown on stage. The path can be reshaped with the Selection and Subselection tools.
4. Resize the span by dragging its end.

## Motion Editor
- The Motion Editor gives a curve per property so that eases and values can be edited with bezier handles. Open it from the tween span (double-click it) or the Window menu, depending on version.
- Add easing per property: Simple (Slow) presets or custom curves.
- Use it to change timing without re-keying: move property keyframes along time.

## Motion tween versus classic tween
- **Motion tween** (object-based): keyframes live on the span; one tweened object per layer; supports 3D rotation and translation in compatible document types.
- **Classic tween** (frame-based): the older approach with keyframes on the timeline; use it if you need frame-by-frame control or the older workflow.
- Convert or copy a motion tween's frames with right-click options, such as Copy Motion as XML, to reuse timing.

## Gotchas
- A symbol instance is required: a raw shape needs Convert to Symbol (F8) first.
- A second object on the same layer breaks the tween; use separate layers.
- Rotating around the wrong pivot: set the transformation point before tweening.

## Verify
- [ ] Easing and path inspected in the Motion Editor.
- [ ] One object per tween layer.
