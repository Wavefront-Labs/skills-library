---
id: computing-software.game-programming.unity.sendmessage-vs-interfaces
name: sendmessage-vs-interfaces
category: computing-software
field: game-programming
product: unity
tags: [unity, sendmessage, interfaces, getcomponent, decoupling, game-programming]
level: practitioner
status: draft
description: "Replace Unity SendMessage/BroadcastMessage string dispatch with interfaces found via GetComponents and TryGetComponent, keeping messages typed, fast and refactor-safe."
sources: ["https://docs.unity3d.com/ScriptReference/GameObject.SendMessage.html", "https://docs.unity3d.com/ScriptReference/Component.GetComponents.html", "https://docs.unity3d.com/ScriptReference/Component.TryGetComponent.html", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/MessagingSystem.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SendMessage vs interfaces

**Goal:** one object tells another "you were hit" without string method names.

## Why not SendMessage
`SendMessage("TakeDamage", 10)` looks up methods by name via reflection on every component of the
object, boxes the argument, silently does nothing on a typo (unless `SendMessageOptions.RequireReceiver`)
and breaks when a method is renamed. IL2CPP managed stripping can remove the target method because no
code references it. `BroadcastMessage` walks all children too.

## Interface dispatch
```csharp
public interface IDamageable { void TakeDamage(int amount, GameObject source); }

void OnCollisionEnter(Collision c) {
    if (c.collider.TryGetComponent(out IDamageable d)) d.TakeDamage(10, gameObject);
}
```
- `GetComponent<T>`/`TryGetComponent<T>` accept interface types. `TryGetComponent` does not allocate
  in the editor when nothing is found (GetComponent creates a fake-null object there).
- Several receivers on one object: reuse a list to avoid allocations.
```csharp
static readonly List<IDamageable> buf = new();
target.GetComponents(buf);
foreach (var r in buf) r.TakeDamage(10, gameObject);
```
- Hit a child collider but the logic is on the root: `GetComponentInParent<IDamageable>()`, or cache
  the receiver on the collider with a small forwarding component.

## Hierarchy-wide messages
`ExecuteEvents.Execute<T>(go, null, (h, _) => h.Method())` (uGUI messaging system) gives a typed
version of SendMessage for custom `IEventSystemHandler` interfaces, and `ExecuteHierarchy` bubbles up
to the first handler, like UI events.

## When SendMessage is acceptable
Editor prototyping, or Unity callbacks that already use it internally. Never in hot paths.

## Verify
- [ ] Search the project for `SendMessage(` and `BroadcastMessage(`; each remaining call is justified.
- [ ] Renaming the interface method is a compile error, not a silent runtime no-op.
