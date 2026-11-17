---
id: computing-software.game-programming.game-engine-architecture.reflection-system-for-serialization
name: reflection-system-for-serialization
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, serialization, reflection-system, type-info, type-descriptors, cpp-reflection, macros, game-programming]
level: advanced
status: docs-checked
description: "Build a C++ runtime reflection system with type descriptors and macros, then drive serialization, JSON import and rendering parameters from it."
sources: ["https://preshing.com/20180116/a-primitive-reflection-system-in-cpp-part-1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reflection system for serialization

**Goal:** describe each type's fields once, then get serialization and other generic features from
that description instead of hand-written code per type. This follows Jeff Preshing's
"A Primitive Reflection System in C++" (part 1).

## The model (from the article)
- Runtime reflection generates metadata for C++ types as `TypeDescriptor` objects, created at
  runtime, describing the structure of other runtime objects.
- The author's motivation was serialization in a custom game engine. Once it worked he also used
  it for rendering (passing uniform parameters and describing vertex formats to OpenGL ES) and
  importing JSON (a generic routine builds a C++ object from a JSON file plus a type descriptor,
  used for 3D models, level definitions and other assets).
- The system is built on preprocessor macros and templates. The article says C++ was not designed
  to make runtime reflection easy, and that obscure language rules and order-of-initialization
  bugs were the main traps.

## How registration works
- A `REFLECT()` macro inside a struct declares two static members: `Reflection` (the type
  descriptor) and `initReflection` (a function that fills it in).
- A block of `REFLECT_STRUCT_*()` macros in a .cpp file lists the members. Their expansion calls
  `reflect::TypeResolver<T>::get()` for each member, using `decltype` to pass the right type.
- `TypeResolver` is a class template. `TypeResolver<T>::get()` returns the descriptor for T; the
  primary template handles reflected structs and their members.
- Every `TypeDescriptor` has a name, a size and virtual functions (the sample has `dump()`).
  Concrete descriptors derive from it so each kind of type (for example std::string, or a struct)
  holds extra information.

## Using descriptors
- A descriptor describes a type only. For a whole object you need the descriptor plus a pointer
  to the object, and the sample's `dump()` takes `const void*`. The article's rule: objects held
  as `void*` should always travel with their type descriptors as a pair, because an invalid
  pointer or wrong pair will likely crash.
- The sample only dumps objects to the console; serializing to a binary format is the same
  traversal with a different action (the article points this out rather than implementing it).

## Design points to decide (own advice, not from the article)
- Store field names or name hashes in files so readers can skip unknown fields, and add
  explicit version numbers for migrations.
- Serialize pointers between objects as ids and fix them up after load.

## Verify
- [ ] Round-trip test for every reflected type: write, read, compare field by field.
- [ ] Old save files load after adding or removing a field.
- [ ] Every `void*` object is passed with its descriptor.

## Checked
Method: docs-checked 2026-11-09 against Preshing's "A Primitive Reflection System in C++, Part 1" (downloaded HTML, read in full except the code listings). Removed the home-grown TypeInfo/FieldInfo sketch, offsetof gotchas, Unreal UHT, libclang and C++26 claims, and the gameenginebook.com and Unreal documentation sources (landing page or not read).
