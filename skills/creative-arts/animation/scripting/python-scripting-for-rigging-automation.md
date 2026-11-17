---
id: creative-arts.animation.scripting.python-scripting-for-rigging-automation
name: python-scripting-for-rigging-automation
category: creative-arts
field: animation
product: scripting
tags: [rigging, maya, maya.cmds, pymel, autorig, python, constraints, naming-convention, batch, characters, controls, skinning, build-script, mgear, rigging-automation]
level: practitioner
status: draft
description: "Python automation for rig building in Maya/Blender: batch-building control rigs, constraints, and naming from data instead of hand-rigging each character."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Python scripting for rigging automation

**What it is:** scripting the *rig-building step itself* — joints, controls,
constraints, naming, and skin weight setup — so a new character rig is a
script run against that character's data (guide positions, a skeleton
template, a sides/parts list), not hours of manual rigging repeated per
character. This is distinct from `scripting-basics` (headless scene/shot
building for render) and from `custom-tool-scripting-for-pipelines` (GUI
tools artists click) — this skill is specifically about the rig graph:
joints, constraints, control shapes, and the naming contract animators
depend on.

Maya (`maya.cmds` / PyMEL) is the primary environment this is verified
against; Blender's rig-construction API (`bpy.ops.armature`, bone
constraints) follows the same shape and is noted inline where it differs.

## 1. Drive the build from data, not from clicking
A rig build script takes a plain data structure — not UI state — as input:
```python
GUIDES = {
    "arm_L": {"side": "L", "joints": ["shoulder", "elbow", "wrist"],
               "positions": [(5,15,0), (8,12,0), (11,9,0)]},
}
```
Guides can be locators placed by hand in a guide scene, or just a JSON/YAML
file. Either way, the build script reads positions out of data and emits
joints/controls — never hardcodes a character's specific coordinates in the
script body. That's what makes one script rebuild 40 characters.

## 2. Naming convention is the contract — enforce it in code
Animators, the anim rig, and any later script (deformers, export) all key off
names. Pick one scheme and build a helper that is the ONLY place names are
assembled:
```python
def name(side, part, suffix):      # L_arm_elbow_JNT, R_leg_ankle_CTL
    return f"{side}_{part}_{suffix}"
```
- `side` in `{L, R, C}`, `suffix` in a fixed vocabulary (`JNT`, `CTL`, `GRP`,
  `CON` for constraint nodes). Never let a one-off script spell a suffix
  differently — a `_ctrl` next to forty `_CTL`s breaks any later script that
  globs by suffix.
- Mirror by string substitution on `side`, not by re-deriving positions:
  `mirror_name = name.replace("L_", "R_", 1)` plus a mirrored transform
  (negate the mirror axis) — cheaper and less error-prone than rebuilding the
  right side from scratch.

## 3. Joints: orient explicitly, don't trust creation order
```python
cmds.joint(p=(5,15,0))                       # creates AND parents under selection
cmds.joint('shoulder_JNT', e=True, zso=True, oj='xyz', sao='yup')  # orient after the fact
```
- `cmds.joint()` parents the new joint under whatever is selected — chain
  order depends on selection state, which is exactly the "ops act on context"
  trap also covered in `scripting-basics`. Explicitly `cmds.select(d=True)`
  (deselect) before starting a fresh chain.
- Orient joints AFTER the whole chain exists (`zso=True` zeroes the end
  joint's rotation) — orienting mid-build compounds errors down the chain.
- In Blender, `bpy.ops.armature.extrude_move` has the equivalent
  selection-dependence; prefer building the `EditBone` data directly
  (`armature.edit_bones.new()`) when scripting, same reasoning as preferring
  the data API over ops in `scripting-basics`.

## 4. Controls are curves, built once, parented through an offset group
Never parent a control curve straight onto a joint — insert a zero/offset
group so animators' keyed channels stay at identity when nothing is happening:
```python
ctl = cmds.circle(nr=(1,0,0), r=3, n=name(side,"elbow","CTL"))[0]
zero = cmds.group(ctl, n=name(side,"elbow","ZERO"))
cmds.matchTransform(zero, "elbow_JNT")
cmds.parentConstraint(ctl, "elbow_JNT", mo=False)
```
- `mo=False` (maintain offset off) is correct when control and joint are
  already coincident from `matchTransform`; use `mo=True` only when you
  constrain across a deliberate offset.
- Freeze transforms on the control curve's shape, not the offset group, so
  the animator's channel box shows clean zeros.

## 5. HARD-WON GOTCHAS
- **`cmds.joint()` reuses the LAST created joint as parent even across
  unrelated chains** if you forget to deselect — the most common cause of a
  batch rig build silently producing one tangled skeleton instead of N clean
  limbs. Always bracket each chain with explicit select/deselect.
- **Freezing transforms on a constrained node breaks the constraint.**
  Freeze BEFORE constraining, never after.
- **Skin weights don't survive a joint rename done after binding** — Maya's
  skin cluster stores influence by node, so renaming is safe, but a
  *rebuild* (delete + recreate joint) orphans the weights. If a build script
  might re-run on an already-skinned character, make it idempotent by
  checking `cmds.objExists()` and skipping/rebuilding the skin cluster
  explicitly, not just the joints.
- **Mirrored controls need mirrored rotation axes, not just mirrored
  position**, or the animator's "rotate X" moves the limb the wrong way on
  one side. Mirror via `cmds.setAttr(ctl + ".scaleX", -1)` on the control
  shape's parent only if your rig convention expects negative scale there —
  otherwise mirror the joint orient's `secondaryAxisOrient` instead. *This
  detail is pipeline-convention-dependent — confirm against your rig's
  existing mirrored limb before trusting either approach blind (unverified
  which is "correct" in general; verify per rig).*

## 6. Batch-building N characters from a template
```python
for char in characters:
    cmds.file(new=True, force=True)
    build_skeleton(char["guides"])
    build_controls(char["sides"])
    cmds.file(rename=f"rigs/{char['name']}_rig.ma")
    cmds.file(save=True, type="mayaAscii")
```
Run via `mayapy build_rig.py` (headless, no UI) for CI/batch use — same
batch-build motivation as `scripting-basics`'s `blender -b --python`.

## Verify
- [ ] Build script run twice on the same character produces byte-identical
      (or functionally identical) output — idempotent, no accumulating nodes.
- [ ] Every joint/control name matches the one naming helper's output; no
      hand-typed names elsewhere in the script.
- [ ] A mirrored limb rotates the same *perceived* direction as its source
      when the animator rotates the same channel.
- [ ] Skin weights (if any) survive a re-run without manual re-painting.
- [ ] Script runs headless via `mayapy` (or `blender -b --python`) and exits
      non-zero on a build failure.

See also: `scripting-basics` (the headless/data-driven pattern this borrows),
`custom-tool-scripting-for-pipelines` (wrapping this build script in a GUI
button for riggers who don't want to touch Python).
