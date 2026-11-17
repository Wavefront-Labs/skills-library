---
id: computing-software.software-engineering.objective-c.isa-metaclass
name: isa-metaclass
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runtime, isa-metaclass]
level: sme
status: docs-checked
description: "Explain how instances point to classes via isa, what class objects and metaclasses are, and why [obj class] can differ from object_getClass."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocObjectsClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# isa and metaclasses
**Goal:** model how instances, class objects and metaclasses relate.

- `id` is defined as a pointer to `struct objc_object { Class isa; }`, and `Class` as a pointer to `struct objc_class`. Every object therefore has an `isa` variable saying which class it is an instance of; it is often called the isa pointer.
- The runtime can find an object's exact class just by asking the object, which supports dynamic typing, dynamic binding and introspection.
- The compiler creates one class object per class. It is not an instance, has no instance variables of its own, and can perform class methods, which are inherited down the hierarchy like instance methods.
- The compiler also builds a metaclass object per class. It describes the class object as the class object describes instances, but you cannot send messages to it directly; it is used only internally by the runtime.
- A class object that cannot answer with a class method can perform instance methods defined in the root class.
- Dynamically created subclasses (key-value observing and Core Data do this) typically override `class` so they masquerade as the class they replace. For such objects `[object class] != object_getClass(object) != *((Class*)object)`.

## Gotchas
- Compare two classes as `[objectA class] == [objectB class]`, using the `class` method rather than lower-level functions.

## Self-check
Print `object_getClass(obj)` and `[obj class]` for an object under key-value observing and compare them.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on objects, classes and messaging: `id` and `Class` definitions, `isa`, class objects, metaclass note, root-class instance methods, class equality for dynamic subclasses. Removed: non-pointer isa, `class_isMetaClass`, metaclass chain and lookup description, the `NSKVONotifying_` class name, tagged pointers, `obj->isa` advice (not on the page); the Runtime Guide source was not used. The page is a retired document.
Method: documentation only; no commands were run.
