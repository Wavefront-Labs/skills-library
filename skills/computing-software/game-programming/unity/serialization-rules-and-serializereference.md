---
id: computing-software.game-programming.unity.serialization-rules-and-serializereference
name: serialization-rules-and-serializereference
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, unity-serialization, serializereference, serializefield, formerlyserializedas, iserializationcallbackreceiver, polymorphism, inspector, game-programming]
level: practitioner
status: docs-checked
description: "Know what Unity serializes: field rules, [Serializable] classes, SerializeReference for polymorphism, FormerlySerializedAs renames, callbacks."
sources: ["https://docs.unity3d.com/Manual/script-Serialization.html", "https://docs.unity3d.com/Manual/script-serialization-rules.html", "https://docs.unity3d.com/ScriptReference/SerializeReference.html", "https://docs.unity3d.com/ScriptReference/Serialization.FormerlySerializedAsAttribute.html", "https://docs.unity3d.com/ScriptReference/ISerializationCallbackReceiver.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serialization rules and SerializeReference

**Goal:** data you set in the Inspector is actually saved, survives refactors, and supports
polymorphic lists (for example a list of different ability effects).

## What gets serialized
Unity serializes fields, not properties. A field is serialized when it:
- is `public` or has `[SerializeField]`; and is not `static`, `const` or `readonly`; and
- has a serializable type: primitives, enums (32 bits or smaller), fixed-size buffers, Unity built-in
  types (Vector2, Vector3, Rect, Matrix4x4, Color, AnimationCurve), custom structs and classes marked
  `[Serializable]`, references to `UnityEngine.Object`-derived types, and arrays or `List<T>` of
  those; `Dictionary<TKey,TValue>` is also supported with `[SerializeField]`.

Not supported: multidimensional arrays, jagged arrays, and collections nested directly in another
collection (for example `List<Dictionary<string,int>>`). Wrap the nested type in a class or struct, or
use `ISerializationCallbackReceiver`.

`[NonSerialized]` excludes a field from serialization and the Inspector; use `[HideInInspector]` to
hide a field but still serialize it. `[Serializable]` is not inherited: put it on every class in an
inheritance hierarchy. Without it on a custom class, the field is silently not serialized.

Properties are not serialized, but their backing field can be. For an auto-property, use the `field:`
prefix: `[field: SerializeField] public int MyInt { get; set; }`.

## Plain [Serializable] classes are values
By default custom classes are serialized inline by value. The same instance stored in several fields
becomes separate objects after deserialization. Direct self-reference is ignored (the field is always
null after loading); indirect cycles stop after 10 levels of recursion and log a warning.

## SerializeReference: polymorphism, null, sharing, cycles
`[SerializeReference]` stores the field as a managed reference. It supports null, shared references,
cyclical graphs and polymorphism (without it, only the declared base type's fields are saved and the
base type is instantiated on load). Per the SerializeReference reference page:
- It works on fields whose type is a regular class, abstract class, interface or `System.Object`.
- The value must be an instance of a `[Serializable]` custom class, must not derive from
  `UnityEngine.Object`, must not be a value type, a `Dictionary`, or an unsupported type like `Stack<T>`.
- On an array or `List<T>` field the attribute applies to the elements, and you cannot assign a list
  to a `System.Object` field.
- Managed references are shared only within their host object; cloning the host or assigning the same
  object on two hosts produces separate copies. Use a ScriptableObject to share data across hosts.
- By-value serialization is more efficient, so use `SerializeReference` only where needed.
- If a referenced type no longer exists when deserializing, Unity replaces the instance with null but
  preserves the serialized information.
```csharp
public interface IEffect { }
[System.Serializable] public class DamageEffect : IEffect { public int amount; }
[SerializeReference] public List<IEffect> effects;
```

## Renaming fields safely
`[FormerlySerializedAs("hitpoints")] public int health;` keeps the old serialized value. The
attribute is Editor-only and can be applied multiple times.

## Custom formats
`ISerializationCallbackReceiver` provides `OnBeforeSerialize` and `OnAfterDeserialize` for types
Unity cannot serialize. The serializer runs on a different thread from most of the Unity API, so
process only fields the object directly owns. For managed references, `OnBeforeSerialize` runs on
the host before its managed references, and `OnAfterDeserialize` runs on the host after them.

## Verify
- [ ] Inspector shows and saves every field you expect (reopen the scene and check values).
- [ ] Polymorphic lists reload with the correct concrete types.

## Checked

Method: docs-checked 2026-11-09 against the Unity manual pages Script serialization and Serialization rules, and the script reference pages SerializeReference, FormerlySerializedAsAttribute and ISerializationCallbackReceiver (all read in full).
Removed as unconfirmed: the claim that dictionaries are unsupported (the current manual supports them with SerializeField), the `TypeCache` type-dropdown editor advice, the `MovedFrom` attribute advice, "keep the attribute until all assets are re-saved", and the "OnBeforeSerialize is called often" remark.
