---
id: computing-software.game-programming.unity.root-motion
name: root-motion
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, unity-root-motion, onanimatormove, apply-root-motion, bake-into-pose, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity root motion correctly: clip root-transform bake settings, Based Upon options, gravityWeight, OnAnimatorMove with Rigidbody, and generic root nodes."
sources: ["https://docs.unity3d.com/Manual/RootMotion.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnAnimatorMove.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root motion

**Goal:** animation-authored displacement (attacks, vaults, starts/stops) without foot sliding or
drifting characters.

## Body Transform and Root Transform
The Body Transform is the character's mass centre. The Root Transform is a projection of it on the Y
plane, computed at runtime; each frame its change is applied to the GameObject to move it.

## Clip import settings (Animation Clip Inspector)
Three channels, each with **Bake Into Pose** and **Based Upon**. "Baked" motion stays in the pose
(the body moves, the GameObject does not).
- *Root Transform Rotation*: Bake Into Pose means the clip never rotates the GameObject. Use it only
  for clips with similar start and stop orientation, such as a straight walk or run; the editor shows
  a green light for good candidates. Based Upon: Body Orientation (default; follows the body's
  forward vector, works for most mocap walks, runs and jumps but fails for strafing, where you can
  use Offset) or Original (keeps the authored offset, typically for keyframed data).
- *Root Transform Position (Y)*: Bake Into Pose keeps Y motion in the pose so the clip does not change
  GameObject height. Most clips enable it; only clips that change height (jump up or down) turn it off.
  Based Upon offers Original, Mass Center (Body) and Feet; Feet matches the lowest foot Y on every
  frame and suits clips with Bake Into Pose off, which helps avoid floating when blending.
- *Root Transform Position (XZ)*: Bake Into Pose is usually used for idles, forcing delta XZ to 0 and
  stopping small deltas from accumulating into drift. It can also force an authored position for a
  keyframed clip using Original.

Bake Into Pose for Position (Y) also sets `Animator.gravityWeight`: 1 when baked, 0 when not. At 1,
physics handles y-axis movement (gravity applies) provided Use Root Motion is enabled on the Animator
and the GameObject has a Character Controller, Rigidbody or Rigidbody 2D; at 0, the clip drives y.
`gravityWeight` is read only.

## Loop pose
Loop Pose is computed relative to the Root Transform: the pose difference between start and stop
frames is distributed over the clip from 0 to 100%.

## Applying and overriding it
`OnAnimatorMove` is invoked each frame after state machines and animations are evaluated, before
OnAnimatorIK. Unity's own example attaches it to a character with an Animator and optionally a
Rigidbody, with Apply Root Motion enabled, and reads `animator.deltaPosition` and
`animator.deltaRotation`:
```csharp
void OnAnimatorMove() {
    if (rb != null) {
        Vector3 velocity = animator.deltaPosition * rootMotionMultiplier / Time.deltaTime;
        velocity.y = rb.velocity.y;                       // preserve vertical velocity (gravity)
        rb.velocity = velocity;
        rb.MoveRotation(rb.rotation * animator.deltaRotation);
    } else {
        transform.position += animator.deltaPosition * rootMotionMultiplier;
        transform.rotation *= animator.deltaRotation;
    }
}
```

## Generic rigs
Generic root motion works like Humanoid, but the Root Transform comes from the transform set as the
Root node rather than the Body Transform; bones below the root-motion bone become relative to it.

## Verify
- [ ] Idle clips show no XZ drift (Bake Into Pose set for Position XZ).
- [ ] Motion that must respect collisions is routed through physics in `OnAnimatorMove`.

## Checked

Method: docs-checked 2026-11-09 against the Unity manual "How Root Motion works" page (read in full) and the MonoBehaviour.OnAnimatorMove script reference (read in full).
Removed as unconfirmed: the CharacterController.Move snippet, Animate Physics Update Mode advice, `anim.velocity`, NavMeshAgent updatePosition handling, MatchTarget usage, per-state SMB toggling, the humanScale scaling note and the "Update Mode Normal jitters" claim.
