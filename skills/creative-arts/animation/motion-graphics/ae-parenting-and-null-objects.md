---
id: creative-arts.animation.motion-graphics.ae-parenting-and-null-objects
name: ae-parenting-and-null-objects
category: creative-arts
field: animation
product: motion-graphics
tags: [null-objects, null-object, parenting, after-effects, hierarchy, rigging, controller]
level: practitioner
status: draft
description: "Build hierarchies in After Effects with parenting and nulls: pick whip, what is inherited, controller nulls, rig order, 3D and camera nulls, common traps."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Parenting and null objects (After Effects)

**Parenting** links a layer's transformation to another layer: a child follows the parent's position, scale and rotation. A **null object** (Layer > New > Null Object) is an invisible layer that renders nothing, so it is a clean controller.

## Parenting
- Use the **Parent & Link** column (enable via Columns) and drag the pick whip from the child to the parent, or choose from the dropdown.
- The child inherits the parent's **Position, Scale, Rotation** (and the 3D equivalents), but **not opacity** or time or effects.
- A child's own values are **relative** to the parent: a child at position 0,0 sits at the parent's anchor point. Set the parent's anchor point where you want the pivot (the shoulder, the hinge).
- Parenting a layer to a layer that is already moving can make the child jump; set the parent link at a frame where the relationship is as intended, or zero the child's transform first.

## Null objects as controllers
1. Create a null named for what it does (`CTRL_head`, `CTRL_all`), and parent layers to it.
2. Animate the null, not the many children. Change timing by editing one layer.
3. Add **slider and checkbox controls** on the null (`ae-expression-controls.md`) to drive expressions across layers.
4. Put a master null above everything for position and scale of the whole rig.
5. For cameras, parent the camera to a null to move or orbit the camera with simple keyframes. Make the null a **3D layer** if the camera is 3D.

## Rigging order
Build from the root: hips, then spine, then arms and head; parent each part to the one above it. Set anchor points first (`Pan Behind` tool, Y), then parent, then animate.

## Traps
- Scale on a parent also scales the children's position offsets and stroke widths; put scale on a separate null if needed.
- A null shows a dotted outline in the comp: it is not in the render, but "Show Layer Controls" may need toggling to see it.
- Do not parent a 2D layer to a 3D layer expecting 3D movement; make children 3D too.

## Verify
- [ ] Moving the master null moves the whole rig; rotating a joint null rotates only its chain.
- [ ] Parent links are visible in the Parent column and are not accidentally circular.
