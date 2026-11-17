---
id: computing-software.game-programming.godot.physicalbone3d-ragdolls
name: physicalbone3d-ragdolls
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, physicalbone3d, ragdoll, physicalbonesimulator3d, skeleton3d, game-programming]
level: practitioner
status: docs-checked
description: "Make ragdolls in Godot 4 with PhysicalBone3D: Create Physical Skeleton, PhysicalBoneSimulator3D, joint limits, collision layers, partial ragdolls and death transitions."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/ragdoll_system.html", "https://docs.godotengine.org/en/stable/classes/class_physicalbone3d.html", "https://docs.godotengine.org/en/stable/classes/class_physicalbonesimulator3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PhysicalBone3D ragdolls

## Create
1. Select the `Skeleton3D` in the imported character and choose **Create Physical Skeleton** from its
   toolbar menu. Godot generates `PhysicalBone3D` nodes and collision shapes for each bone and joints
   connecting them.
2. Delete bones you don't need (fingers, twist bones, face) to keep the ragdoll small.
3. Adjust the collision shapes to fit the mesh before tuning joints.

## Joints
Each PhysicalBone3D has a `joint_type` (`JOINT_TYPE_NONE` = 0, `JOINT_TYPE_PIN`, `JOINT_TYPE_CONE`,
`JOINT_TYPE_HINGE`, `JOINT_TYPE_SLIDER`, `JOINT_TYPE_6DOF`) with limits in the Joint section of the
inspector. The tutorial says generated bones get an unconstrained pin joint by default, while the
class page lists a `joint_type` default of 0 (none); check the value on your bones. Per the tutorial:
- ConeJoint (ball-and-socket): shoulders, hips, neck. Limit Swing Span between 20 and 90 degrees and
  Twist Span between 20 and 45 degrees.
- HingeJoint: elbows and knees. Enable Angular Limit in Joint Constraints, rotate the PhysicalBone3D to
  set the axis, then adjust the angles.
- 6DOFJoint: linear and angular constraints, most complex. If in doubt, start with Hinge and Cone.

## Start and stop
```gdscript
@onready var sim: PhysicalBoneSimulator3D = $Skeleton3D/PhysicalBoneSimulator3D

func die(impulse: Vector3, hit_bone: StringName) -> void:
    $AnimationTree.active = false
    $CollisionShape3D.disabled = true        # the CharacterBody capsule
    sim.physical_bones_start_simulation()     # all bones; pass a bone name list for a partial ragdoll
    var b := sim.find_child(hit_bone) as PhysicalBone3D   # find by node name
    if b:
        b.apply_central_impulse(impulse)

func revive() -> void:
    sim.physical_bones_stop_simulation()
```
The tutorial calls `physical_bones_start_simulation(["l-arm", "r-arm"])` for a partial ragdoll and
`physical_bones_stop_simulation()` to stop; it is a method of PhysicalBoneSimulator3D.

## Collision setup
- Set the collision layer and mask so the CharacterBody3D's capsule does not get in the way of the
  simulation (the tutorial also notes adjusting layers on pickups so the player can still collect them).
- PhysicalBone3D has `mass` (default 1.0), `can_sleep` (default true) and `body_offset`.

## Verify
- [ ] Death from different directions looks plausible with no exploding limbs on spawn.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Ragdoll system tutorial and the PhysicalBone3D class page: Create Physical Skeleton, joint types and enum names, cone/hinge/6DOF guidance and span limits, PhysicalBoneSimulator3D start/stop with a partial bone list, apply_central_impulse, mass and can_sleep defaults, collision layer/mask note. Flagged: tutorial (pin joint default) versus class page (joint_type default 0, none). Removed (not confirmed): 4.3+ gate and pre-4.3 Skeleton3D API note, 11-15 body count, simulator `influence` blending, ticks-per-second and Jolt jitter advice, CCD advice, root-motion gotcha, sleep-time check.
Method: documentation only; no commands were run.
