---
id: computing-software.game-programming.unreal-engine.blend-spaces-and-aim-offsets
name: blend-spaces-and-aim-offsets
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-animation, aim-offset, blend-space, additive-animation, game-programming]
level: practitioner
status: docs-checked
description: "Build Unreal blend spaces and aim offsets: axis settings, Use Grid vs triangulation, smoothing and Weight Speed, mesh-space additive aim poses and Anim Graph setup."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/blend-spaces-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/aim-offset-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blend spaces and aim offsets

**Goal:** smooth directional locomotion and an upper-body aim that follows the camera.

## Blend Space (Blend Spaces page)
- Create from Content Browser Add (+) > Animation: Aim Offset, Aim Offset 1D, Blend Space, Blend Space 1D. Samples
  are animations plotted on a graph; the result blends between samples by input value per axis. A normal 2D graph can be
  used one-dimensionally by using one axis only.
- Axis Settings in Asset Details: Name, Minimum Axis Value, Maximum Axis Value, Grid Divisions, Snap to Grid, Wrap Input,
  Smoothing Time, Smoothing Type, Damping Ratio, Max Speed. The page suggests ranges such as -90 to 90 or -180 to 180
  for an Aim Offset whose grid should match rotation values.
- **Use Grid** enables the legacy grid mode instead of the default triangulation; Epic says to use it only for
  specific arrangements such as Wrap Input, otherwise leave it disabled for more accurate blends.
- **Wrap Input** lets the input exceed the min/max, treated as circular; ensure animations at either end are similar to
  avoid popping.
- **Smoothing Time** (seconds; 0 means no time blending) with Smoothing Type: Averaged, Linear, Cubic, Ease In/Out,
  Exponential, Spring Damper. Damping Ratio below 1 overshoots. Max Speed applies only to Spring Damper or Exponential
  (0 = unlimited). **Axis to Scale Animation** names the axis (typically speed) for playback scaling when smoothing.
- **Weight Speed** (per sample): 2.0 means a sample's weight can go zero to one in half a second; 0.0 disables it
  (unless Per Bone Overrides are used). Epic says do not combine Weight Speed or its Smoothing with Smoothing Time /
  Smoothing Type.
- Notify Trigger Mode: All Animations, Highest Weighted Animation or None.
- Editor: hold Ctrl to preview at the cursor, Ctrl+Alt for the influence display; thin triangles show in red.
- Use in an AnimGraph by right-click or dragging the asset in, which creates a Blend Space player.

## Aim Offset (Aim Offset page)
- A Blend Space whose samples are additive, applied on a base animation (e.g. a neutral aiming-forward pose). Choose
  the same Skeleton as the Skeletal Mesh. Set **Preview Base Pose** in Asset Details.
- Each sample Animation Sequence: Additive Anim Type = Mesh Space, Base Pose Type = Selected animation frame, Base Pose
  Animation = the same base animation, Ref Frame Index = 0.
- Why Mesh Space: it applies in the Skeletal Mesh Component space, so with a leaning character an upward-aim sample is
  not skewed as it would be with Local Space.
- Yaw extremes can look wrong while running or walking; limit the incoming data so side-to-side extremes are used only
  when stationary, or aim only up and down and let the character rotation handle side-to-side.
- Anim Graph: place the Aim Offset player (Blend Spaces category), connect a Base Pose input (the base animation or a
  state machine with a similar base pose) to it and its output to Output Pose, and drive Yaw and Pitch; the page's
  example uses property access on the pawn's base aim rotation.

## Checked
Date: 2026-11-07. Read in full: Blend Spaces page (all sections) and Aim Offset page (all sections), unversioned en-us
pages that state no engine version.
Removed as not on those pages: the walk/jog/run sample speeds, the `NativeThreadSafeUpdateAnimation` aim-interpolation
code, `FInterpTo` constants, `GetBaseAimRotation()` / `RemoteViewPitch` replication note, `spine_01` Layered Blend Per
Bone advice, ~90 degree turn-in-place rule, retargeting and sync-marker gotchas, and the Verify checklist.
Method: documentation only; no commands were run.
