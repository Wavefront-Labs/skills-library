---
id: creative-arts.animation.blender.story-props-staging
name: story-props-staging
category: creative-arts
field: animation
product: blender
tags: [blender, props, story-props, staging, choreography, extras, crowd, action-text, hand-attach, bone-parent, keyframe, drop, roll, camera-aim, beat, set-dressing, performance, pipeline, shot-level]
level: advanced
status: verified
description: "Per-shot story props and crowd choreography from the action text: hand-attached objects, drops and rolls on the beat, extras keyed via empties, camera aiming at the prop beat."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# SKILL: Story props and staging (per shot, from the action text)

Set dressing is per LOCATION and static (`set-dressing`). This skill is per SHOT and
moves: the objects the action line names, the extras the sequence needs, the lights
that have to pop on a beat. Without it an action beat renders as a character miming
at nothing — the owner watched the grocery-bag gag that is the premise of an episode
play as a man crouching on an empty kerb, and the dialogue that referenced it read
as random words.

## 1. Every noun in the action text is a prop or a defect

Grep the shotlist's action lines for hand-prop nouns (bag, can, orange, receipt,
letter, cup…) and resolve each to a sourced asset (`asset-sourcing`: a CC0 food kit
had bag, can and orange; a blaster kit had the box). Only build from primitives what
no kit has and that IS a primitive (a hydrant is a cylinder and a cap; a drain is a
dark slot and five bars). Keep a per-shot table keyed by shot id, not by location.

The QC check is five lines: action nouns vs the quoted names in the dress list and
the props module; every miss is a red row.

## 2. Attach, drop, roll — three verbs cover most beats

- **In hands:** bone-parent to `hand_l` / `hand_r` with an identity parent-inverse and
  a small offset. Bone parenting is fine in a shot scene because the scene is never
  saved; the parent-space matrix that does not survive a save never has to.
- **Drop:** read the hand bone's world position at the start frame (set the frame
  first, then `rig.matrix_world @ pose_bone.head`), key to the ground with one short
  bounce, stagger each item a few frames ("can, can, box" is three frames apart, not
  one). LINEAR interpolation on prop keys; bezier floats.
- **Roll:** key a path with a bounce point and a rotation of several turns to the
  destination; the last key drops it below the surface (into the drain).

## 3. Place relative to the ACTUAL character, not the mark

Marks are assigned by cast INDEX in most pipelines, so "Okafor's mark" is wherever
his slot put him this shot. Scatter around `rig.matrix_world.translation`, on the
camera side (−y), never around a hard-coded mark. The first version put the cans at
mark B while Okafor stood at mark A.

## 4. The camera aims at the beat

When the beat is the prop (the bag splitting, the orange in the drain), the aim point
is the prop — head or no head. Return an aim from the props pass and let it override
the head-bone aim; a CLOSE on a face while the cans drop out of frame bottom is the
beat not rendering. Mind the shot size: a MED frames knee-up, so anything on the
ground needs the aim dropped to ~0.5 m or it is below frame.

## 5. Extras and choreography

- Append the locked extra characters, assign an idle clip, and **parent each rig to an
  empty; key the empty.** Object-level keys on the rig land in the rig's active action,
  which is the shared library clip.
- Space extras for the LENS: a 50 mm MED is ~2 m wide at 3 m, so extras a stride
  apart, not spread along a street (spread for a WIDE at 28 mm).
- Lights that pop: **key a point light's energy, not a material socket.** Socket keys
  silently fail on rebuilt (celified) materials (`NodeSocket.default_value not found`),
  and the material path leaves no visible pop. Swell the practical's mesh too so it
  reads at 10 m in a WIDE.
- Verify practicals are not INSIDE the geometry: a set builder placed porch lamps on
  the house origin line, which was 3 m deep in the kit's wall. Hang them off the
  nearest house's bounding-box front face.
- A WIDE back-distance is measured from the aim: if the far row starts 6 m out, aim
  near (2 m) so the pull-back lands the camera 9 m from the row, or one house fills
  the frame.

## 5b. Paper inserts are a 2D job, not a 3D prop

Any INSERT whose beat is something *written* — the back of a photo, a menu, a blank
warranty card, a note — is a flat object with legible text. Modelling it in the set
buys nothing: a 3D card at 60 mm is a blurred rectangle, and the text has to be
readable or the line that reacts to it ("Back.") is a non sequitur. Three kitchen
inserts rendered as the same empty counter before this rule because the 3D set had no
menus, no card and no photo, and the noun check only knew food.

Draw the card: paper tint, grain, a drop shadow, real fonts (a serif for print, a
pencil face for handwriting), composited over the shot's own rendered frame blurred
and darkened so the insert still lives in that room. Then a slow push (ffmpeg
`zoompan`, ~6 % over the shot) to an FX clip the assembly splices over the slot — the
same path title cards and glitches use. No renderer involved, so it also cannot
disturb a batch render that is mid-run.

Two traps: drawing grain with an alpha colour on an RGBA canvas punches see-through
stripes (draw grain in RGB, then convert); and the noun check must know the insert's
words (keep a quoted `PROPS` list in the inserts module and grep it with the dress
list) or the row stays red after the card exists.

## 6. Verify

Render a proof still per prop shot at a frame AFTER the beat, and check three things
by eye: the prop is in frame, it is in the character's hand or on the ground where the
action says, and the camera is on it. Then grep the action nouns again: the list must
be empty.
