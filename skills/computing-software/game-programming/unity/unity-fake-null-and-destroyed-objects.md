---
id: computing-software.game-programming.unity.unity-fake-null-and-destroyed-objects
name: unity-fake-null-and-destroyed-objects
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, unity-fake-null, destroyed-object, null-conditional, game-programming]
level: practitioner
status: docs-checked
description: "Handle Unity's overloaded == null for destroyed objects: why ?? and ReferenceEquals disagree with == and how to check a destroyed object."
sources: ["https://docs.unity3d.com/ScriptReference/Object-operator_eq.html", "https://unity.com/blog/engine-platform/custom-operator-should-we-keep-it"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity fake-null and destroyed objects

**Goal:** never act on a destroyed object, and never get fooled by a reference that is "null" to
Unity but not to C#.

## What happens
Anything derived from `UnityEngine.Object` (GameObject, components, and so on) is a thin C# wrapper holding a pointer to a
native object. The native object's lifetime is managed explicitly: it is destroyed when a new scene loads or when you call
`Object.Destroy(obj)`. The wrapper's lifetime follows the C# garbage collector, so a wrapper can outlive the native object.

Unity gives `UnityEngine.Object` a custom `==` operator. As well as checking that the managed reference is null, it checks
whether the native pointer is null; if either is true, `== null` evaluates to `true`. The Script Reference notes this
can give different results from `Object.ReferenceEquals` or `==` in standard C#.

Checks that bypass the custom operator see a destroyed wrapper as not null. Unity's own blog post names the `??`
operator, which does a pure C# null check and cannot be redirected to Unity's. Treat any C# null check that does not call
the overloaded `==` the same way (`ReferenceEquals` is documented as differing).

```csharp
if (target == null) return;   // Unity's operator: true for a destroyed object
var t = maybeDestroyed ?? fallback;   // pure C# null check: a destroyed wrapper is NOT replaced
```

## Editor-only "fake null" for unassigned fields
In the Editor only, a MonoBehaviour field that is unset holds a "fake null" object rather than a real null, so Unity can
show a helpful message and highlight the GameObject in the Inspector instead of a bare NullReferenceException. The blog
notes this is why `GetComponent` for a missing component allocates in the Editor but not in built games, and why you
should profile a built player, not the Editor.

## Costs of the custom operator (from the same blog post)
- It is counterintuitive.
- Comparing two Unity objects, or one to null, is slower than a plain reference check.
- It was described as not thread safe, so do not compare Unity objects off the main thread.
- The post is from 2014 and floated removing the operator; the current Script Reference still documents it, so keep
  relying on it.

## Verify
- [ ] Destroyed-object checks use `== null` / `!= null` on the Unity-typed variable, not `??`.
- [ ] No Unity object comparisons run on worker threads.

## Checked
Date: 2026-11-09. Read in full: Script Reference "Object operator ==" and Unity blog "Custom == operator, should we keep
it?" (2014). Removed as not on those pages: the `?.`, `is null`, pattern-matching and interface-variable claims, the
statement that Destroy takes effect after the Update loop, `DestroyImmediate` advice, analyser IDs UNT0007/UNT0008,
`UnassignedReferenceException`/"Missing (Type)" inspector behaviour, and the dictionary and cached-component gotchas.
Method: docs-checked 2026-11-09 against the two pages named above.
