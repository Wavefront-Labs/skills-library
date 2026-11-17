---
id: creative-arts.animation.blender.layout-blocking
name: layout-blocking
category: creative-arts
field: animation
product: blender
tags: [blender, layout, blocking, staging, append, 180-line, tangents, shot]
level: practitioner
status: verified
description: "Assemble a shot: append locked characters into a locked set, stage to the beat, hold the 180-line, avoid tangents."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SKILL: Layout & blocking (shot assembly) — expert

Assemble a shot: put locked characters into a locked set, stage them for the beat,
place the camera, light the balance. Verified Ep1 Act-3 key shot (Chip+Dill, alley).
Pairs: `../environment-design/set-building`, `camera-cinematography`, `lighting`,
`../pipeline/character-consistency`, `blendercraft-headless`.

## Assemble = append locked assets (consistency law)
Open the locked SET `.blend`; **append** each character's objects; never rebuild.
```python
bpy.ops.wm.open_mainfile(filepath=SET)            # set carries its own lights/cam
def append_char(path):
    before=set(bpy.data.objects)
    with bpy.data.libraries.load(path, link=False) as (src,dst): dst.objects=list(src.objects)
    new=[o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.name not in scene.collection.objects: scene.collection.objects.link(o)
    root=next((o for o in new if o.type=='EMPTY' and o.name.startswith('TURN')),None)  # char root
    return root
```
- Each char is parented to its **root empty** (`TURN`) → move/rotate the whole character
  by that empty. Stage by `root.location`/`root.rotation_euler` only.
- **Name clashes** (both chars have `head`, `OUTLINE_BLACK`, `face_mint`) auto-suffix
  `.001` on append — harmless for rendering; grab roots by scanning NEW objects, not by
  hard-coded names.
- `link=True` (library link) instead of append when you want edits to the source asset
  to propagate to every shot — stronger consistency, but can't tweak per-shot. Default
  to append for shots that need small per-shot pose offsets.

## Staging / blocking (the craft)
- **Block for the beat first:** who's where, who faces whom, who enters. Place feet on
  the ground (char assets built feet≈z0 → root z=0 grounds them). Check scale by eye
  against the set (built to character height).
- **Two-shot rules:** avoid **tangents** — don't let two characters just touch/overlap
  at the edges (Chip was tangent to Dill); separate in depth so one overlaps clearly in
  front, reading foreground/background. Stagger along the camera axis for depth.
- **Stage line / 180°:** keep the camera on one side of the line between two characters
  across a scene so screen-direction stays consistent (who looks left/right).
- **Lead room / looking room:** leave space in frame in the direction a character looks
  or moves.
- **Silhouette the acting:** pose so the read is clear in silhouette (see character-
  design). Entering-backlit = strong silhouette (Chip at the street mouth).

## Light balance at assembly
- The set's lights define mood; **re-balance for the characters in frame.** A char
  backlit by a bright source (the gold street) goes to silhouette — if an emissive
  feature must still read (Chip's mint face), **raise its emission strength** or lower
  the backlight, or add a small cool kicker on the front. (Lesson: street at ~900W area
  washed Chip's face at emission 3; bump face to ~6–8 or add a front kick.)
- With `view_transform='Standard'` there's no filmic rolloff, so a very bright emissive
  backdrop blows out and crushes mid emissives — balance by eye in a test render.

## Camera
Set lens/height for the shot (wide ~28–35mm for a corridor two-shot to hold depth;
longer for a clean single). See camera-cinematography. The set ships a default camera;
reposition it per shot, don't rebuild.

## Output
Render a **composition still (key frame) first** — cheap, proves staging+scale+light
before committing to animation. Then animate (blocking passes → spline). Archive the
key still with the shot. Builder: `series/production/blender/build_shot_alley_key.py`.

## Self-check
- [ ] Set + chars are APPENDED locked assets, not rebuilt?
- [ ] Characters grounded (feet on floor), scale reads against the set?
- [ ] No tangents; depth stagger; clear fore/background read?
- [ ] 180° line respected; lead/looking room present?
- [ ] Poses read in silhouette?
- [ ] Light balanced so required emissives read against backlight?
- [ ] Composition still rendered + approved before animating?

## Pitfalls
- Rebuilding assets per shot → drift (break the consistency law). Append/link.
- Grabbing chars by hard-coded names after append → hits `.001` clashes; scan NEW objs.
- Tangents/overlap at frame edges = flat, ambiguous depth.
- Bright emissive backdrop + Standard transform crushes other emissives → balance test.
