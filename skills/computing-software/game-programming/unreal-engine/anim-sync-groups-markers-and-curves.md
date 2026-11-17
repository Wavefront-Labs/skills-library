---
id: computing-software.game-programming.unreal-engine.anim-sync-groups-markers-and-curves
name: anim-sync-groups-markers-and-curves
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, sync-group, sync-markers, animation-curves, animation-blueprint, game-programming]
level: practitioner
status: docs-checked
description: "Keep blended Unreal animations in phase with sync groups, roles and sync markers, and drive materials, morph targets and Anim Graph values from animation curves."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-sync-groups-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-curves-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sync groups, markers and animation curves

**Goal:** blend walk and run cycles without foot-placement mismatch, and use curves for synchronised values.

## Sync groups (Sync Groups page)
- One animation is the leader, the rest followers. The leader provides the master length and has priority for
  triggering Animation Notifies; followers match its length and have their notifies suppressed. By default the
  animation with the highest blend influence is leader and roles can change during a blend.
- Restrictions from the page: all synced animations need the same general body movement start to end (for walk and run,
  the same feet planted at start and end frames), and no drastic length differences, or playrate "pops" appear when
  leader and follower switch.
- Details panel settings: **Group Name** (same name for animations meant to blend, e.g. sneak, walk, run, sprint),
  **Group Role**, **Method**.
- Group Role values: Can be Leader (default; leader while it has the highest blend weight), Always Follower (if all are
  set so, the first evaluated becomes leader), Always Leader (if several, the last evaluated is leader), Transition
  Leader and Transition Follower (excluded from syncing while blending in, then leader or follower until blended out).
- Method values: Do Not Sync (default), Sync Group, Graph.
- Group-based: select the nodes in the AnimGraph, Sync category, Method = Sync Group, same Group Name. Preview by
  connecting to a Blend node with Alpha 0.5.

## Sync markers
- Add via right-click in an Animation Notify timeline > Add Sync Marker... > New Sync Marker...; saved to the Skeleton and
  reusable through Existing Sync Markers.
- Useful when step counts differ, stride lengths differ, or for non-looping starts and stops (the page says start and
  stop animations should be Always Leader).
- Markers only sync with other markers when animations are in the same Sync Group: group and marker names must match.
- Only markers common to every animation in the group are synced. Marker syncing is used automatically when the
  animations have matching markers; otherwise it falls back to normal length syncing.
- Montages support marker-based syncing while blending out (Sync Group properties in the Montage editor Asset Details).

## Graph-based syncing
Set Method to Graph on child nodes and use the Sync node (right-click > Misc. > Sync) or a Blend Space Graph with a
Group Name to propagate one group. Sequence Players generated in Blend Space Graph samples default to the Graph method.

## Animation curves (Animation Curves page)
- Float values keyed in an Animation Sequence; stored on the Skeleton asset, so creating one requires saving the
  Skeleton. Create from the Curves track dropdown (Add Curve... > Create Curve) or the Anim Curves panel
  (Window > Anim Curves).
- Import from Maya-style custom attributes: float type only, keyframed, with Import Custom Attribute enabled on FBX import.
- Panel columns: Type (Morph Targets or Materials), Weight, Auto, Bones. Details: Connected Bones and Max LOD
  (value 1 evaluates LOD 0 and 1).
- Material: match the curve name to a Scalar Material Parameter and enable the Material type; it affects all Materials
  on the Skeletal Mesh. Morph Target: match the Morph Target name and enable the Morph Target type.
- In Animation Blueprints, curves commonly drive alpha values of Anim Graph nodes such as IK. Functions on the page:
  Get Active Curve Names, Get All Curve Names, Get Curve Value (target an Anim Instance).
- Metadata Curves output a constant 1.0 and are read-only; normal curves with no keys output 0.0.

## Checked
Date: 2026-11-07. Read in full: Sync Groups page (Overview, Sync Settings, Group-, Marker- and Graph-Based Syncing,
Blend Space Graphs) and Animation Curves page (all sections), unversioned en-us pages with no engine version stated.
Removed as not confirmed on the pages: `GetCurveValue` C++ call and the `FootIKAlpha` example, "Montage Sync Group"
overlay advice for upper-body, Animation Modifier / `FootstepAnimEventsModifier` marker auto-placement, "linked anim
layers need the same group name", curve compression quantizing values, "Can Be Leader" labelled as only the default
for sequence player nodes, and the invented Verify step. The third source (Animation Sequences page) was not re-read and
was dropped from `sources`.
Method: documentation only; no commands were run.
