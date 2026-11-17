---
id: computing-software.game-programming.unity.scriptableobject-event-driven-architecture
name: scriptableobject-event-driven-architecture
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, event-channel, decoupling, observer-pattern, singleton-alternative, unityevent, architecture, game-programming]
level: practitioner
status: docs-checked
description: "Decouple Unity gameplay systems with ScriptableObject variables, GameEvent assets with listeners, and ScriptableObject systems instead of singletons."
sources: ["https://unity.com/how-to/architect-game-code-scriptable-objects", "https://docs.unity3d.com/Manual/class-ScriptableObject.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScriptableObject event-driven architecture in Unity

**Goal:** stop systems depending directly on each other by routing communication through ScriptableObject assets, which
exist in the project independent of GameObjects and can be dragged into Inspector fields.

Unity's guide (from Ryan Hipple of Schell Games) frames this around modular design (no hard references between systems,
scenes as clean slates, self-contained prefabs, single-purpose components), data-driven and editable parts, and being easy to
debug (visible state in the Inspector).

## Asset-based variables
A `FloatVariable : ScriptableObject` with a `Value` field lets any MonoBehaviour or ScriptableObject reference the shared
value. When one MonoBehaviour changes `Value`, others see the change, which forms a messaging layer between systems with no
references to each other. Example: a health bar reads `PlayerHP` that the player writes, so the bar can point at a different
variable (for example `PlayerMP`) without code changes.

To avoid changing the value stored on disk, the guide copies the data into a runtime value: an `InitialValue` field plus a
`[NonSerialized] RuntimeValue`, reset in `OnAfterDeserialize` (via `ISerializationCallbackReceiver`). MonoBehaviours then
access `RuntimeValue`.

## Event assets and listeners
Two parts: a `GameEvent : ScriptableObject` and a `GameEventListener : MonoBehaviour`.

```csharp
[CreateAssetMenu]
public class GameEvent : ScriptableObject {
    private List<GameEventListener> listeners = new List<GameEventListener>();
    public void Raise() { for (int i = listeners.Count - 1; i >= 0; i--) listeners[i].OnEventRaised(); }
    public void RegisterListener(GameEventListener l) { listeners.Add(l); }
    public void UnregisterListener(GameEventListener l) { listeners.Remove(l); }
}

public class GameEventListener : MonoBehaviour {
    public GameEvent Event;
    public UnityEvent Response;
    private void OnEnable() { Event.RegisterListener(this); }
    private void OnDisable() { Event.UnregisterListener(this); }
    public void OnEventRaised() { Response.Invoke(); }
}
```
- Designers create any number of `GameEvent` assets. A listener registers in `OnEnable`, unregisters in `OnDisable`, and
  invokes a `UnityEvent` (a serialized function call rather than a true event).
- Raising iterates the listener list backwards.
- Example: the Player script calls `Raise` on an `OnPlayerDied` asset; Game Over UI, camera fade, music and every enemy
  listen without the Player knowing them. Test a response by calling `Raise` from test code or an Inspector button.
- The guide says Schell Games' production version grew to pass data and auto-generate types; the sample is the starting point.

## Systems as ScriptableObjects
A system implemented in a MonoBehaviour can often move into a ScriptableObject. The guide's example puts an inventory in a
ScriptableObject instead of a `DontDestroyOnLoad` MonoBehaviour: it has no Transform and no `Update`, keeps state between
scene loads without special initialisation, and scripts take a public reference instead of using a singleton, which makes it
easy to swap in a test or tutorial inventory.

## Persistence of changes
Per the manual: in the Editor you can save data to ScriptableObjects in Edit and Play mode; in a standalone Player you can only
read saved data. Changes made through the Inspector or Editor authoring tools are written to disk automatically. Changes made
by script in Edit mode are not saved automatically: call `EditorUtility.SetDirty` on the object, or they may not persist
between Editor sessions.

## Verify
- [ ] Systems reference a channel or variable asset, not each other's concrete type.
- [ ] Every listener registers in `OnEnable` and unregisters in `OnDisable`.
- [ ] Runtime-mutated values use a `NonSerialized` runtime copy, not the serialized asset field.

## Checked
Date: 2026-11-09. Read in full: Unity "Three ways to architect your game with ScriptableObjects" (January 2020) and the
manual page "ScriptableObject data assets". Removed as not on those pages: the typed `UnityAction` channels with C# events,
runtime sets, the claim that Play Mode mutations persist in the Editor and the Enter Play Mode Settings advice, the
"when not to use" list (return values, per-frame events, over-fragmentation), and the missing-unsubscribe
`MissingReferenceException` claim.
Method: docs-checked 2026-11-09 against the two Unity pages named above.
