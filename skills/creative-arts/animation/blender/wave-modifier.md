---
id: creative-arts.animation.blender.wave-modifier
name: wave-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, wave-modifier, wave-deform, wave, modifiers, flag-animation, ripples, procedural-animation]
level: practitioner
status: verified
description: "Animate ripples, flags and pulses with Blender's Wave modifier: motion axes, cyclic, normals mode, start position, time offset/life/damping, height/width/narrowness and masks."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/wave.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# wave-modifier

Goal: a procedural travelling wave with no keyframes — water-drop ripples, a waving flag, a sonar pulse, a wobbling jelly — that loops and can be masked.

## Fields

- **Motion**: *X* and/or *Y*; vertices are deformed in Z from the start point. Both enabled = circular wave fronts; one = straight fronts that travel along that axis (run in 4.5.14: with only X on, height depends on X alone, so the crests run across the X axis, not parallel to it).
- **Along Normals** (meshes only, with X/Y/Z toggles restricting the local axes): displace along surface normals instead of the object's Z axis.
- **Cyclic**: repeat the waves rather than a single pulse.
- **Falloff**: how fast the waves fade out away from the start position.
- **Time**: *Offset* (frame at which the pulse sits at the start position; the pulse eases in before it, and a negative number starts the wave already in progress), *Life* (duration in frames; 0 loops forever), *Damping* (extra frames over which the wave damps to zero after Life), *Speed* (per frame).
- **Start Position**: *Start Position X/Y* in local space, or **Object** (animate it to move the origin over time).
- **Height** (amplitude), **Width** (half the distance between the tops of two ripples when Cyclic), **Narrowness** (higher = narrower pulse; the pulse is `4 / Narrowness` units wide).
- **Vertex Group** (with invert) and **Texture** masking.

All values are in local object space, so multiply by the object scale for real dimensions. For a near-sinusoidal sea wave set Narrowness equal to `2 / Width` (Width 1, Narrowness 2). Pulses too close together make Blender lower the whole wave so the minimum is zero, reducing the apparent amplitude.

## Recipes

These recipes are practice; tune the numbers by eye.

- **Water drop**: a subdivided plane, Wave X+Y, Cyclic off, a Life and Damping so the ripple dies out, Start Position Object = Empty at the drop point.
- **Flag**: a dense plane, pinned edge via a Vertex Group gradient (0 at the pole, 1 at the tip), Wave X, Cyclic, plus a second Wave with Y motion for cross-flutter. Cheaper than Cloth.
- **Sonar pulse on a sphere**: Along Normals, Start Position Object inside the sphere.
- **Looping render**: pick Speed, Width and Life so the cycle repeats evenly across the loop length, then confirm by comparing the first and last frames.

## Gotchas

- Needs dense geometry like every deformer: a 4-vert plane shows nothing.
- Start Position is in the object's local space, so moving the origin shifts the ripple.
- Along Normals follows the surface normals, so flipped normals reverse the displacement direction; recalculate normals.
- Life 0 loops the animation forever; a wave that never ends is usually Life left at 0.

## Verify

- Scrub frames: the displacement peaks at the Offset frame and, with Life set, is back to zero at Offset + Life + Damping (run: Offset 5, Life 10, Damping 10, Cyclic off, Height 0.5 gave a peak of about 0.5 at frames 5 to 15, 0.02 at frame 20 and 0 at frame 25).
- Loop test: the frame at the start and the frame one cycle later look identical.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/deform/wave.rst: Motion, Cyclic, Along Normals, Falloff, Height, Width, Narrowness (4 / Narrowness, 2 / Width sinusoid hint), Time settings (Offset, Life 0 = forever, Damping, Speed), Start Position, local-space note. Removed the 1.5 default, the 4 x Width wave-length formula, motion blur claim and numeric recipe values (now practice).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: defaults Cyclic on, Speed 0.25, Height 0.5, Width 1.5, Narrowness 1.5, Life 0, Damping 0, Falloff 0; Life 0 still displaced at frame 500; Life plus Damping ended the wave as stated; X-only motion made height independent of Y; Width 1 with Narrowness 2 gave a peak of 0.49 for Height 0.5; Along Normals has per-axis X/Y/Z toggles; Start Position X/Y/Object properties exist. Corrected the X/Y front direction and the Offset and Verify wording.

Method: manual text confirmed from documentation; Wave behaviour run headless in Blender 4.5.14.
