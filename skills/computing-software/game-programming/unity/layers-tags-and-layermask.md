---
id: computing-software.game-programming.unity.layers-tags-and-layermask
name: layers-tags-and-layermask
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, unity-layers, layermask, comparetag, physics-layers, culling-mask, rendering-layers, bitmask, game-programming]
level: intro
status: docs-checked
description: "Use Unity layers and tags correctly: LayerMask fields and bit operations for raycasts, CompareTag, camera culling masks, rendering layers, and the 32-layer limit."
sources: ["https://docs.unity3d.com/Manual/Layers.html", "https://docs.unity3d.com/ScriptReference/LayerMask.html", "https://docs.unity3d.com/ScriptReference/Component.CompareTag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layers, tags and LayerMask

**Goal:** filter physics queries, rendering and gameplay by object category without string checks
or name lookups.

## Layers (32, global)
Edit > Settings > Tags and Layers (per the LayerMask reference). The first 8 layers are specified by Unity
(layer 0 is Default, layer 1 TransparentFX); the other 24 are yours. Layers separate GameObjects so they can
be filtered by physics queries, collision and rendering. Plan them: `Player`, `Enemy`, `PlayerProjectile`, `EnemyProjectile`, `Environment`, `Interactable`,
`Ragdoll`, `Trigger`... You have at most 24 custom ones.

## LayerMask in code
```csharp
[SerializeField] LayerMask groundMask;                // pick layers in the Inspector

bool Grounded() => Physics.SphereCast(transform.position, 0.3f, Vector3.down, out _, 0.2f, groundMask);

int enemyLayer = LayerMask.NameToLayer("Enemy");      // layer index (cache it)
int mask = (1 << enemyLayer) | LayerMask.GetMask("Environment");  // bit mask
int allButPlayer = ~LayerMask.GetMask("Player");
bool isEnemy = ((1 << other.gameObject.layer) & enemyMask) != 0;
```
The classic bug: passing a layer **index** where a **mask** is expected (`Physics.Raycast(..., 8)`
means layer 3, not layer 8). Use LayerMask fields or `GetMask`.

## Tags (string)
```csharp
if (other.CompareTag("Player")) ...
// faster overload when the tag is reused: cache a TagHandle
TagHandle playerTag = TagHandle.GetExistingTag("Player");
if (other.CompareTag(playerTag)) ...
```
`CompareTag(TagHandle)` can be faster than the string overload, particularly if the same TagHandle is reused.
Use tags for coarse identity checks; for anything richer, prefer components (`TryGetComponent<Player>`)
or interfaces.

## Checked
2026-11-01. Confirmed against the Unity Manual (Assign GameObjects to layers) and Scripting API (LayerMask,
Component.CompareTag): 32 layers with 8 built in and 24 user-defined, LayerMask is a bitmask, GetMask,
NameToLayer, LayerToName, CompareTag string and TagHandle overloads. Removed: Rendering Layers section, tag
allocation and error claims, FindWithTag note, per-system layer usage list (not on these pages).
Method: documentation only; no commands were run.

## Verify
- [ ] All raycasts use LayerMask fields or GetMask (search for numeric masks).
- [ ] Tag checks use `CompareTag`.
- [ ] Layer list documented; collision matrix matches it.
