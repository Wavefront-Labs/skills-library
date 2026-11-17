---
id: computing-software.game-programming.unreal-engine.linked-anim-layers
name: linked-anim-layers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-animation, linked-anim-layers, animation-layer-interface, linkanimclasslayers, weapon-anim-sets, lyra-animation, game-programming]
level: advanced
status: docs-checked
description: "Structure Unreal character animation with Linked Anim Layers: Animation Layer Interface, Linked Anim Layer nodes, Link Anim Class Layers, and the per-weapon pattern used in Lyra."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-animation-blueprint-linking-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-in-lyra-sample-game-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linked anim layers

**Goal:** keep shared locomotion logic in one main Anim Blueprint and swap sub-sections of the graph (for example per
weapon) through linked Animation Blueprints.

## What the system is
Animation Blueprint Linking extends Sub Anim Instances: it switches sub-sections of an Animation Graph dynamically,
supporting multi-user collaboration and memory savings because the Animation Blueprint no longer loads animation assets
that are not in use.

## Pieces (Using Animation Blueprint Linking)
1. **Animation Layer Interface**: Content Browser > Animation > Animation Layer Interface. Analogous to Blueprint
   Interfaces; defines the layers, their names, groups they belong to, and inputs (layers can expose input poses and
   parameters). Compile after adding inputs.
2. **Linked Anim BP**: a normal Anim Blueprint on the same skeleton; add the interface in Class Settings > Interfaces and
   fill each layer graph (the page's example plays a hit-react animation into the Output Pose).
3. **Main Anim BP**: also adds the interface in Class Settings and calls the layer with a **Linked Anim Layer** node
   in the Anim Graph. The node's **Instance Class** property sets a default layer override, handy for splitting logic
   (the page's example: frequently changing IK logic in its own Anim BP).
4. **Switching at runtime (Blueprint)**: on the Mesh component use **Link Anim Class Layers** and **Unlink Anim Class
   Layers**, giving the linked Anim BP class. Linking sets up and runs the instance; unlinking resets the layer to its default.

## Pattern from the page (Fortnite use case)
- Two interfaces, one for weapons and one for vehicles, can be active together; one Anim BP implementing an interface
  can override several points (for example WeaponUpperBody and WeaponAdditive).
- A shared locomotion state machine lives in the main graph; each weapon Anim BP has a layer it can override per state,
  and leaves the output unconnected for states it does not need to override.
- Anim BPs with layers have their own Event Graphs, which keeps per-vehicle or per-weapon data processing contained.

## Lyra implementation (Animation in Lyra page)
- `ALI_ItemAnimLayers` is the Anim Layer Interface (layers for locomotion states, aiming and skeletal controls, such
  as `FullBody_Aiming`). `ABP_ItemAnimLayersBase` is the base linked-layer Anim BP; every weapon has a child Anim BP
  inheriting it, where animators slot in animations and edit per-weapon variables (`ABP_PistolAnimLayers` is the example).
- Linked layers reach the main Anim BP (`AnimBP_Mannequin_Base`) through a custom function `Get Main Anim BPThreadSafe`
  and Property Access, avoiding recalculating values such as Acceleration or Velocity.
- Linked layers use Property Access with Anim Node Functions (`On Update`, `On Become Relevant`), for example
  choosing a directional start animation each time the animation becomes relevant.
- Lyra computes animation values with Multi Threaded Animation rather than the Event Graph: Project Settings > Engine
  > General Settings > Anim Blueprints > Allow Multi Threaded Animation Update. Thread-safe functions cannot read data
  directly from game objects.

## Verify
- [ ] The main Anim BP and each linked Anim BP implement the same interface layers.
- [ ] Calling Link Anim Class Layers changes the output of the Linked Anim Layer node, and Unlink resets it.

## Checked
Date: 2026-11-07.
Read in full: Using Animation Blueprint Linking (Steps, End Result, Additional Use Case) and Animation in Lyra
(all sections; the Linked Layer, Anim Node Functions and Blueprint ThreadSafe sections used above). dev.epicgames.com;
the Lyra page mentions Unreal Engine 5.0 for montages.
Removed as unconfirmed: the C++ `LinkAnimClassLayers` / `UnlinkAnimClassLayers` snippet and `TSubclassOf<UAnimInstance>`
type (the page shows only the Blueprint nodes), example layer function names (`FullBody_IdleState` etc.), "per group"
Linked Anim Graph claim, soft-reference loading advice, inertialization advice on weapon swap, and the memory-report Verify step.
Method: documentation only; no commands were run.
