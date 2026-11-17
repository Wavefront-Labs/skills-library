---
id: computing-software.game-programming.unity.managed-code-stripping-and-link-xml
name: managed-code-stripping-and-link-xml
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, managed-code-stripping, link-xml, preserve-attribute, unitylinker, il2cpp, game-programming]
level: advanced
status: docs-checked
description: "Control Unity's managed code stripping: what the Unity linker removes, preserving reflection-only types via link.xml and [Preserve], AlwaysLinkAssembly, RequiredMember."
sources: ["https://docs.unity.com/en-us/engine/current/manual/programming-environment/script-compilation/managed-code-stripping", "https://docs.unity.com/en-us/engine/current/manual/programming-environment/script-compilation/managed-code-stripping/preserving"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed code stripping and link.xml

**Goal:** small builds without "type not found" / MissingMethodException crashes from reflection-only code.

## What gets removed
Stripping runs at build time and removes unused or unreachable code from managed assemblies (your
scripts, packages and plugins, .NET Framework). The Unity linker uses static analysis, so it sees only
code that exists at build time: code generated at runtime is not analysed, and the linker cannot
always detect reflection use. Code reached only by reflection or runtime code generation should be
preserved explicitly. The stripping level is set in the Unity Editor; the level names and defaults
are on the manual's "Configure managed code stripping" page, so read them there for your version.

## Preserving
```csharp
using UnityEngine.Scripting;
class Foo { [Preserve] public void PreservedMethod() { } }
[assembly: AlwaysLinkAssembly]   // see below
```
- `[Preserve]` on a type preserves the class and its default constructor; on a method it preserves the
  method, its declaring type, return type and argument types. It also covers properties, fields,
  events and delegates.
- `AlwaysLinkAssembly` forces the linker to process an assembly even if no other assembly in the build
  references it. It applies root marking rules but does not directly preserve code; it is intended for
  precompiled or package assemblies with `[RuntimeInitializeOnLoadMethod]` methods, and has no effect
  if another included assembly already references the assembly.
- `RequiredMemberAttribute` marks all members of a type as dependencies; the page also lists
  `RequiredImplementors`, `RequireDerived`, `RequiredInterface` and `RequireAttributeUsages`.
- `link.xml`: the file must be named `link.xml`, sit in `Assets` or a subdirectory, and contain the
  `<linker>` tag. Any number of `link.xml` files may be used. It cannot go inside a package, but a
  non-package `link.xml` can reference package assemblies. For the XML syntax (the attribute values
  for what to preserve) follow the manual's link.xml formatting reference.

## Verify
- [ ] Save/load, JSON configs and any reflection-driven system pass on a build with your intended
  stripping level.

## Checked

2026-11-01. Confirmed on the Unity manual pages for managed code stripping and for preserving code: build-time
static analysis, Unity linker, [Preserve] semantics, AlwaysLinkAssembly, RequiredMember family, link.xml rules
(name, location, `<linker>` tag, not in packages). Removed: stripping level names and defaults, Mono/IL2CPP
availability, link.xml preserve values and example, Addressables behaviour, diagnosis paths and symptoms (not on
those pages). Corrected: link.xml cannot ship in a package.

Method: documentation only; no commands were run.
