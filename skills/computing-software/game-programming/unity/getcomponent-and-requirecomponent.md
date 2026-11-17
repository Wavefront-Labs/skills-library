---
id: computing-software.game-programming.unity.getcomponent-and-requirecomponent
name: getcomponent-and-requirecomponent
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, unity-components, trygetcomponent, requirecomponent, getcomponentinchildren, component-caching, game-programming]
level: intro
status: docs-checked
description: "Find and depend on components in Unity: TryGetComponent vs GetComponent, GetComponentInChildren search rules, RequireComponent behaviour, and caching references."
sources: ["https://docs.unity3d.com/ScriptReference/Component.TryGetComponent.html", "https://docs.unity3d.com/ScriptReference/RequireComponent.html", "https://docs.unity3d.com/ScriptReference/Component.GetComponentInChildren.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GetComponent, TryGetComponent and RequireComponent

**Goal:** components that find their collaborators reliably and do not repeat lookups needlessly.

## Declaring dependencies
```csharp
[RequireComponent(typeof(Rigidbody))]
public class PlayerScript : MonoBehaviour
{
    Rigidbody rb;
    void Start() { rb = GetComponent<Rigidbody>(); }
}
```
- When a script with `RequireComponent` is added to a GameObject, the required component is added automatically.
- It checks for missing dependencies only when `GameObject.AddComponent` is called (in the Editor or at runtime). Unity
  does not add missing dependencies to components that already exist on GameObjects without them, so existing objects
  need fixing by hand (for example re-adding the script).
- Constructors take one, two or three `System.Type` arguments. The attribute is `AllowMultiple = true`, class targets
  only.

## Lookup variants
| Call | Behaviour (per the script reference) |
|---|---|
| `TryGetComponent<T>(out T c)` | Searches only the GameObject the calling component is on, active or inactive; returns bool. Differs from `GetComponent` in that it does not allocate in the Editor when the component is missing. |
| `TryGetComponent(Type, out Component)` | Non-generic; less efficient than the generic version, use only if necessary. |
| `GetComponentInChildren<T>(bool includeInactive)` | Checks the GameObject it is called on first, then recurses down the children depth-first until a match; returns the first match or null. Inactive children are skipped unless `includeInactive` is true; the starting GameObject is always searched. |

- `GetComponentInChildren` returns only the first match and the check order on one GameObject is not defined; use
  `GetComponentsInChildren` when you need a specific one among several.
- The non-generic `GetComponentInChildren(Type)` is likewise less efficient than the generic version.
- If the requested type is a MonoBehaviour-derived type whose script cannot be loaded, `GetComponentInChildren` returns
  null for it.
- You can call it on another component reference to search that component's GameObject and its children.

```csharp
void Start()
{
    if (TryGetComponent<HingeJoint>(out HingeJoint hinge)) hinge.useSpring = false;
}
```

## Caching
Repeating a lookup you can do once is wasted work: fetch a reference in `Awake` or `Start` and reuse it, or assign it as
a serialized field in the Inspector. (Design guidance; the script reference pages do not give a cost figure.)

## Checked
Date: 2026-11-07.
Read in full: Component.TryGetComponent, RequireComponent (including constructor table) and
Component.GetComponentInChildren script reference pages (6000.6 docs), including their code samples.
Removed as unconfirmed by those pages: `[DisallowMultipleComponent]`, "RequireComponent prevents removing" the
component, `GetComponentInParent`, `GetComponents<T>(List<T>)`, the interface-lookup claim, the Editor "fake null" detail
for `GetComponent`, `Reset()` auto-fill, the FindObject advice, the Unity null / `?.` section, and the invented Verify
checklist.
Method: documentation only; no commands were run.
