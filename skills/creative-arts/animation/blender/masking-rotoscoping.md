---
id: creative-arts.animation.blender.masking-rotoscoping
name: masking-rotoscoping
category: creative-arts
field: animation
product: blender
tags: [blender, masking, rotoscoping, roto, mask-editor, mask-node, splines, feather, movie-clip-editor, garbage-matte, holdout-matte, keyframed-mask, mask-layers]
level: advanced
status: docs-checked
description: "Rotoscoping with the Blender Mask editor: layers and splines, feather, shape keys, parenting to tracks, the Mask node, Mask strips and modifiers, and garbage and holdout mattes."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/introduction.html
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/sidebar.html
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/editing.html
  - https://docs.blender.org/manual/en/latest/compositing/types/input/mask.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# masking-rotoscoping

Goal: hand-drawn, animated mattes to isolate or exclude parts of footage, such as garbage mattes for keys, holdouts for CG behind actors, and shape-based grading.

## Where masks live

A **Mask** data-block is created and edited in the **Movie Clip Editor** or the **Image Editor** by switching the header mode to *Mask*. Masks are independent of a particular image or movie clip, so they also work for motion graphics. The Compositor and the Sequencer only use finished masks. The Mask settings panel sets a **Start Frame** and **End Frame** for the mask in the Sequencer.

## Layers and splines

- **Mask Layers** panel (Sidebar > Mask tab): each layer has Opacity, Invert, **Blend** (Merge Add, Merge Subtract, Add, Subtract, Lighten, Darken, Multiply, Replace, Difference), **Falloff**, **Holes**, **Overlap**. Details in `creative-arts.animation.blender.mask-layers-blend` and `creative-arts.animation.blender.mask-holes-overlap`.
- Drawing: Ctrl LMB adds points with handles (see `creative-arts.animation.blender.mask-splines-feather`); Alt C toggles cyclic; V sets the handle type; Alt S scales feather; Shift Ctrl LMB adds feather points; Mask > Add has Circle and Square primitives.
- **Active Spline** panel: Feather Offset (Even or Smooth), Weight Interpolation (Linear or Ease), Cyclic, Fill, Self Intersection Check.
- **Parenting** (Active Point panel): parent selected points to a point track or a plane track with Make Parent (Ctrl P); Clear Parent is Alt P. See `creative-arts.animation.blender.mask-parent-to-track`.

## Animating shapes

- Mask > Animation > **Insert Shape Key** (I) keys all splines of the active layer at the current frame; **Clear Shape Key** (Alt I) removes it; **Feather Reset Animation** and **Re-Key Points of Selected Shapes** help clean up. Timing is edited in the Dope Sheet's Mask mode. See `creative-arts.animation.blender.mask-shape-keyframes`.
- The Mask node has **Motion Blur** (Samples, Shutter) for animated masks.
- Header **Mask Display**: *Spline* (with a display type) and *Overlay* with an overlay mode of *Alpha Channel* or *Combined* (Combined adds a Blending Factor), to judge the matte while drawing.

## Using the mask

- **Compositor**: Add > Input > **Mask** node. Properties: the Mask data-block, **Feather** (use or ignore feather points), **Size Source** (*Scene Size*, *Fixed*, or *Fixed/Scene*), **Motion Blur**. The output is a black and white mask that works with Invert, Multiply, Mix, or as a factor input. A Mask node into a Viewer gives live feedback while editing.
- **Keying**: the Keying node has **Garbage Matte** and **Core Matte** inputs for masks.
- **Sequencer**: a *Mask* strip generates a mask image from a Mask data-block at render resolution (like the Mask node without its finer options), and strips have a *Mask* modifier.
- Typical patterns (practice, not from the manual): garbage matte before a key, mask as the factor of a grade, holdout in an Alpha Over.

## Roto practice (not from the manual)

Several simple shapes beat one complex outline; parent to tracks first and key by hand only what deforms; name layers and restrict selection on finished ones; check frames between keys, where roto usually breaks.

## Verify

- Overlay set to Combined: the matte hugs the subject on key frames and on the frames between.
- A Mask node into a Viewer shows white inside, black outside, and soft where feather was set.
- Clear Parent (Alt P) makes a track-parented spline stay put, which confirms the parent.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/masking/*, compositing/types/input/mask, compositing/types/keying/keying, video_editing mask strip and modifier pages) and the 5.2 source (rna_mask.cc, properties_mask_common.py, rna_space.cc overlay modes, blender_default keymap). Fixed: Falloff and Overlap belong to the layer panel, handle-type names, Size Source options (Scene Size, Fixed, Fixed/Scene). Removed unconfirmed claims: Auto Keying for masks, linear interpolation per point, point-count and key-spacing figures, aspect-ratio behaviour, Use Overlap on the spline, and the Grease Pencil remark.
Method: documentation only; no commands were run.
