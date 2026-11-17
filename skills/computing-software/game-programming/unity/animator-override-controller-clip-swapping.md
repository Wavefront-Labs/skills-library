---
id: computing-software.game-programming.unity.animator-override-controller-clip-swapping
name: animator-override-controller-clip-swapping
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, animator-override-controller, clip-swapping, weapon-animsets, game-programming]
level: practitioner
status: docs-checked
description: "Swap clips per character or weapon in Unity with an Animator Override Controller asset, and at runtime with AnimatorOverrideController GetOverrides and ApplyOverrides."
sources: ["https://docs.unity3d.com/Manual/AnimatorOverrideController.html", "https://docs.unity3d.com/ScriptReference/AnimatorOverrideController.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimatorOverrideController clip swapping

**Goal:** one Animator Controller (structure, parameters, logic) reused across characters or weapons,
with only the clips changing.

## Asset workflow
- An Animator Override Controller asset overrides the clips of an Animator Controller while keeping
  the state machine's structure, parameters and logic. Modifying the base controller changes logic
  for all variants; a new character needs only a new override asset.
- Create: Assets > Create > Animation > Animator Override Controller (or the Project window Create
  button). Select it, then set the **Controller** field (drag an Animator Controller in, or use the
  picker).
- The Inspector shows a two-column table: original clips and overriding clips. By default each
  override is the same as the original. Pick an override clip per original clip.
- Assign the override asset as the Animator Controller of the GameObject's Animator component.
- Exit time: use normalized time. In seconds, the exit time might be ignored if an override clip is
  shorter than the exit time; in normalized time the clip exits by the ratio the state machine defines.

## Runtime (three ways, per the reference)
1. Create the override in the Editor.
2. Change one clip per frame: use the indexer (`animatorOverrideController["shot"] = clip`), but each
   call triggers a reallocation of the animator's clip bindings.
3. Change many clips: `ApplyOverrides` reduces reallocation of clip bindings to one per call.
```csharp
// Shape of the reference example (abridged)
animatorOverrideController = new AnimatorOverrideController(animator.runtimeAnimatorController);
animator.runtimeAnimatorController = animatorOverrideController;
clipOverrides = new AnimationClipOverrides(animatorOverrideController.overridesCount);
animatorOverrideController.GetOverrides(clipOverrides);   // List<KeyValuePair<AnimationClip, AnimationClip>>
// ... edit clipOverrides entries, then:
animatorOverrideController.ApplyOverrides(clipOverrides);
```
- Swapping `Animator.runtimeAnimatorController` with an `AnimatorOverrideController` based on the same
  `AnimatorController` at runtime does not reset the state machine's current state.
- API: constructors `AnimatorOverrideController()` and `AnimatorOverrideController(RuntimeAnimatorController)`;
  properties `this[]`, `overridesCount`, `runtimeAnimatorController`; methods `ApplyOverrides`,
  `GetOverrides`.

## Checked
Date: 2026-11-07

Read in full: the "Animator Override Controller" manual page and the `AnimatorOverrideController`
reference (remarks, both code examples, constructor/property/method tables; the inherited-members
list was skimmed).

Removed because neither page confirms it: "unassigned slots use the base clip" wording beyond the
page's "by default each override is the same as the original", the claim that assigning a different
controller resets parameters, `anim.Play(stateHash, ...)` restoration advice, the "placeholder clips
must be unique" gotcha, the claim that events must be copied to replacement clips, and the Verify
list (including the "`Animator.Rebind`-style spike").

Method: documentation only; no commands were run.
