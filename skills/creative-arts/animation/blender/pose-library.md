---
id: creative-arts.animation.blender.pose-library
name: pose-library
category: creative-arts
field: animation
product: blender
tags: [pose-library, asset-browser, pose-assets, blender, posing, silhouette, line-of-action, blocking, character, armature, data-driven, shotlist, acting, body-language]
level: advanced
status: docs-checked
description: "Build and use a Blender pose library (Asset Browser pose assets) so characters never hold one default pose: core pose sets, posing craft, per-beat application, data-driven apply."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/posing/editing/pose_library.html
  - https://docs.blender.org/api/current/bpy.ops.poselib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# SKILL: Pose library (characters never hold one pose)

**Goal:** every character in every shot stands, sits, leans and gestures in a pose
chosen for that story beat — never the rig's default A-pose-with-arms-down held for an
episode. The fix is a **pose library per character**: a curated, versioned set of named
pose assets that a shot can apply in seconds, by hand or by pipeline. A character with
twelve good poses applied thoughtfully reads as *alive*; a character with perfect
animation on one pose reads as a mannequin. This skill covers building the library,
the craft of the poses in it, and wiring it into a data-driven renderer. What happens
*between* poses (moving-hold animation, breakdowns, polish) belongs to
`animation-blocking-to-polish` and `body-mechanics`; the ambient breathing/blink layer
is `procedural-idle-life` — this skill supplies the poses they animate between.

Counts, percentages, frame numbers and ratios in this skill are animation and pipeline practice, not values from the Blender manual; the manual was used to check the Blender tools and operators.

## 1. Blender pose assets (the mechanism)

A pose asset is an action marked as an asset that contains exactly one frame of animation
data; each pose has its own action data-block, name, preview image and catalog.
1. Open the character's **locked rig asset** file (the library is part of the asset,
   not scattered across shot files).
2. In Pose Mode, pose the rig. Select the bones the pose should own (usually: select
   all controls; for partials, see §5).
3. Click **Create Pose Asset** in the Action Editor, or use the same option in the 3D
   Viewport's `Pose` menu in Pose Mode. Blender creates a new action with keys for the
   current location, rotation, scale and Bendy Bone values of the selected bones. If the
   "Current File" library is chosen the action is created in the current file; another
   library creates a `.asset.blend` file containing just that asset.
4. Name it with the convention `<CHAR>.<category>.<name>.v<N>` — e.g.
   `DILL.stand.guarded.v1`, `CHIP.gesture.point-left.v1`. The Asset Browser filters on
   the prefix, and the pipeline (§6) resolves tags against these exact names.
5. Organise poses in **catalogs** per character. Preview images are rendered with the
   active **scene camera** using the Workbench engine, so set up a camera for thumbnails
   (practice: a ¾ angle, the silhouette-reading angle, not front-on) and use the Generate
   Preview button after changing the look.
6. Put the library blend-files in an asset library (preferences, asset libraries; point it
   at `<REPO>/assets/characters/`) so every shot file sees the poses without appending.

Applying: in a shot file (rig linked + library override), select the controls and use the
pose from the Asset Browser (right-click **Apply Pose**, or double-click) or from the Asset
Shelf in the 3D Viewport (click a pose to apply it; drag the thumbnail left to right to
blend it into the current pose). If bones are selected the pose applies only to those
bones. **Apply Pose Flipped** mirrors left and right. **Blend Pose** blends gradually: move
the mouse left/right, `Tab` toggles original/blended, dragging left subtracts the pose,
`E` allows extrapolation past 100%, and `Ctrl` while blending blends the flipped pose.
Then keyframe the result as usual.

Existing assets can be changed from the right-click menu (Adjust Pose, Replace, Add, Remove
on the selected bones; works on the active object only). Poses can also be copied between
files with Copy Pose as Asset and Paste as New Asset.

## 2. The core pose set per character

Build deliberately, not ad hoc. The starter set every speaking character needs (~15–20
poses) — each in the character's *own* body language, not generic:
- **Neutral ×3** — not one: relaxed-neutral, alert-neutral, tired-neutral. "Neutral"
  held all episode is the exact bug this library fixes; three neutrals means even rest
  states can change per scene.
- **Listening** — weight settled, head slightly toward speaker, hands occupied.
- **Guarded / closed** — arms-crossed or hands-clasped, weight back, chin down.
- **Open / warm** — chest open, arms free, weight forward.
- **Pointing** (left and right, or rely on `Ctrl`-flip), **reaching** (low/high).
- **Lean-in** (conspiratorial) and **lean-back** (skeptical).
- **Hands-on-hips**, **thinking** (hand to chin), **sitting ×2** (engaged, slumped).
- **2–3 signature poses** — the stance only this character does (from the character
  bible). These carry identity harder than the face does.
Grow the set from production: any pose you build twice in shots gets promoted into the
library. Cap categories, not count — a 60-pose library with catalogs stays usable;
60 uncategorized assets don't.

## 3. Posing craft (what makes a library pose good)

A pose asset is reused for years; build each to the feature bar. Thumbnail first
(`pose-planning-thumbnailing`), then pose:
- **Silhouette:** flat-shade the viewport (or matcap black) — the pose must read as the
  emotion in pure silhouette. Negative space between arms and torso; no limbs lost
  inside the body mass from the ¾ view.
- **Line of action:** one dominant C or S curve from foot through spine to head.
  A straight vertical spine is the default-pose disease re-entering through the
  library door.
- **Asymmetry everywhere:** never both arms at the same angle, both shoulders level,
  both feet square. Offset hips vs shoulders (contrapposto). If the left side mirrors
  the right, the pose is unfinished.
- **Weight:** one leg carries it; hips shift over the supporting foot; the spine
  counter-curves. A guarded pose and an open pose differ in *where the mass commits*
  before they differ in the arms.
- **Hands pose too:** a library pose with default-flat hands is half a pose. Key finger
  controls into the asset.
- **Push 20% past life, then pull back 5%** — cel-look characters need theatrical
  poses; a pose that feels right in the viewport reads as timid in the shot.

## 4. Applying poses per shot — and per beat within a shot

The anti-mannequin rule: **a pose change is a story event, and every story beat gets
one.**
- **Per shot:** at layout, every character in the shot gets a named pose from the
  library on frame 1 — chosen from the beat's emotion, never "whatever the file opened
  with". Two characters in frame never hold mirror-same poses.
- **Per beat within the shot:** when the character's intention shifts (hears the bad
  news, decides to lie, spots the gate), the body re-poses. Blend to the next asset
  over 6–12 frames at 24 fps (drag-blend to ~70–100%, key, let
  `animation-blocking-to-polish` turn it into a proper breakdown). A 10-second
  dialogue shot usually wants 2–4 pose events; zero pose changes in a shot over
  5 seconds needs a reason.
- **Blend, don't snap-to-100:** applying an asset at 60–80% over the current pose
  keeps continuity with the previous beat and avoids the "everyone returns to the same
  guarded.v1" sameness across shots.
- **Listening is a pose, not an absence:** the non-speaking character changes pose in
  *reaction* to the speaker's beats. This is where held-default-pose is most visible.
- The acting choice of *which* pose belongs to `acting-performance`; this skill
  guarantees the choice is one drag away.

## 5. Partial poses (upper body, hands, head)

Full-body re-poses mid-shot can pop feet or fight a walk. Build **partial pose assets**
keyed only to a bone subset:
- When creating the asset, select *only* the controls the partial owns — e.g.
  `DILL.upper.guarded.v1` keys spine-mid upward + arms + head, leaving root/legs/feet
  unkeyed, so applying it over a sit or a walk never touches the lower body.
- Standard partials per character: `upper.*` (spine-up), `head.*` (neck+head only, for
  listening reactions), `hands.*` (finger sets: fist, splayed, relaxed, grip).
- Applying a partial to selected bones only: select the subset first — the manual says
  that with bones selected the pose applies only to them (its example applies a fist pose
  to a hand, then an open-hand pose to just the index finger and thumb), so a full-body
  asset can also be used partially by selecting just the arms first. **Select/Deselect
  Pose Bones** in the right-click menu shows which bones a pose stores.
- Layer order in practice: body pose → upper override → hand set → head/eye direction.
  Each layer is a separate cheap asset instead of a combinatorial explosion of
  full-body poses.

## 6. Data-driven apply (the pipeline path)

Shots are data; poses should be too. The shotlist row carries a pose tag per character
per beat, and the renderer applies it headlessly:
```json
{"shot":"ep03_sc04_sh02","chars":{"DILL":{"pose":"stand.guarded","pose_events":[{"frame":96,"pose":"upper.open","blend":0.8}]}}}
```
Renderer side (`shot-renderer`), in `bpy`:
- Resolve `<CHAR>.<tag>.v<latest>` to the asset Action in the character's library
  file; a pose asset **is an Action**, so applying = evaluating that action onto the
  rig's pose bones at the event frame and keying:
  `action` → for each fcurve, write its evaluated value to the matching
  `pose.bones[...]` channel, then `keyframe_insert`. (Equivalent to the UI apply;
  `bpy.ops.poselib.apply_pose_asset(asset_library_type, asset_library_identifier,
  relative_asset_identifier, blend_factor=1.0, flipped=False)` does it with context, and
  `blend_pose_asset` is the interactive blend operator.)
- Blend = lerp from current channel value toward the asset value by `blend` (slerp
  quaternions — lerping rotation channels componentwise is the classic popped-shoulder
  bug).
- Unknown tag = **hard error**, not silent default pose — a silent fallback is how an
  episode ships with everyone in neutral again.
- Hand-animated shots override data: the renderer skips pose application when the shot
  file has a saved action for that character flagged `manual`.

## 7. Primitive-rigged characters (no armature)

Early/background characters built from grouped primitives (empty-parented feature and
limb objects) still get a library — a "pose" is just a stored set of object transforms:
- Structure the character so posing is possible: limbs and features parented to an
  empty hierarchy (`CHAR_root → torso → arm.L → hand.L`...), pivots placed at the
  joints when modeled, not after.
- Store a pose as JSON: `{object_name: {"loc":[...], "rot_quat":[...], "scale":[...]}}`
  for every transform in the hierarchy, saved per named pose beside the asset
  (`poses/<CHAR>/<tag>.json`). A 20-line `bpy` script dumps the current scene state to
  a tag and applies a tag back (with the same blend-lerp as §6).
- The shotlist tag resolves identically, so a primitive character and an armature
  character are the same one line of data to a shot — upgrade the rig later without
  touching any shotlist.
- Same craft rules apply: silhouette, line of action through the stack of objects,
  asymmetry. Primitive characters go mannequin *faster* because nothing idles; give
  them the full core set of §2 even if simplified.

## 8. Versioning with the locked asset

The pose library is part of the character asset and obeys the same lock discipline:
- Pose assets live **in the character's asset .blend** (or a sibling
  `<CHAR>_poses.blend` in the same versioned folder) — never in shot files. A pose
  built in a shot gets promoted by re-creating it in the asset file.
- **Never edit a published pose in place** once shots reference it: create
  `guarded.v2`, keep `v1` so old shots re-render identically. The pipeline resolves
  "latest" only for *new* shots; a rendered shot's record pins the version it used.
- Rig updates (`rig-ui-controls` changes, renamed bones) can break stored actions (practice) — after any rig change, run an apply-all smoke test: script-apply every pose
  asset to the new rig and eyeball the contact sheet (render one thumbnail per pose to
  a grid) before unlocking the asset.
- The contact sheet doubles as the library's review artifact: one image per character
  showing every pose silhouette, reviewed like any other asset.

## Verify

- [ ] Every speaking character has ≥ 15 catalogued pose assets including three distinct
      neutrals, listening, guarded, open, and 2–3 signature poses; each reads correctly
      as a flat-shaded silhouette thumbnail.
- [ ] Pick any shot over 5 seconds: the characters in it hold ≥ 2 distinct library
      poses (or a logged reason), and no two characters in frame hold the same pose.
- [ ] Scrub a full episode at 8× speed: no character visibly sits in the rig default or
      one unchanged pose across consecutive scenes.
- [ ] Partial assets (`upper.*`, `hands.*`, `head.*`) exist and apply over a walk/sit
      without moving feet or root.
- [ ] A shotlist pose tag round-trips headlessly: renderer applies
      `<CHAR>.<tag>.v<N>`, unknown tags fail loudly, rendered shots pin the version.
- [ ] After the last rig change, the apply-all contact sheet was regenerated and
      reviewed with no broken poses.

See also: `pose-planning-thumbnailing.md`, `body-mechanics.md`,
`acting-performance.md`, `animation-blocking-to-polish.md`, `procedural-idle-life.md`,
`rig-ui-controls.md`, `../pipeline/shot-renderer.md`.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and the current Python API docs.
Confirmed: pose asset = action with exactly one frame, marked as asset; Create Pose Asset in the Action Editor and the 3D Viewport Pose menu (stores location, rotation, scale, Bendy Bone values); Current File vs `.asset.blend`; Apply Pose, Apply Pose Flipped, Blend Pose behaviour and keys (`Tab`, `E`, `Ctrl`); Asset Shelf click/drag; partial application to selected bones; Adjust Pose/Replace/Add/Remove; thumbnails use the scene camera and Workbench; operators `poselib.apply_pose_asset`, `blend_pose_asset`, `create_pose_asset` and their parameters. Fixed: "Pose panel → Create Pose Asset" and "Asset Browser header +" paths, thumbnail description, apply_pose_asset call shape. Removed: the `I → Whole Character (Selected)` keying set and the Preferences > File Paths path (no doc coverage), and the "Blender 4.x" gate.
Method: documentation only; no commands were run.
