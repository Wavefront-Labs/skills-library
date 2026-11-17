---
id: computing-software.game-programming.unity.il2cpp-vs-mono-scripting-backend
name: il2cpp-vs-mono-scripting-backend
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, il2cpp, mono, scripting-backend, aot, generic-sharing, game-programming]
level: advanced
status: docs-checked
description: "Choose between IL2CPP and Mono in Unity: how IL2CPP builds, how to cut its build time, and its AOT limits (reflection, generics, exception filters, native callbacks)."
sources: ["https://docs.unity3d.com/Manual/il2cpp-introduction.html", "https://docs.unity3d.com/Manual/scripting-restrictions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IL2CPP vs Mono scripting backend

**Goal:** know what IL2CPP changes about builds and code, and what breaks under AOT compilation.

## What IL2CPP is
IL2CPP is Unity's ahead-of-time (AOT) scripting back end, originally developed for platforms that do not support Mono
and just-in-time (JIT) compilation, such as iOS. It converts IL to C++ and compiles that to native code. It is supported
on all platforms and can improve performance and startup time over Mono, but including machine code generally increases
build time and built application size. Managed-code debugging works as with Mono.

Build steps: Roslyn compiles C# to managed assemblies; managed code stripping runs; IL2CPP converts the assemblies to C++;
a native platform C++ compiler builds it; Unity produces an executable or DLL.

## Selecting and building
- IL2CPP must be installed as a module with your Unity install (Unity Hub).
- Cross-compilation is generally not supported: build the Player on the same platform (macOS Player on macOS). Linux
  Players can be built from other desktop platforms (Linux IL2CPP cross-compiler).
- Choose it in Edit > Project Settings > Player > Other Settings > Configuration > **Scripting Backend**, or open Player
  Settings from File > Build Profiles. Scripts can use `PlayerSettings.SetScriptingBackend`.

## Reducing IL2CPP build time
- Exclude the project and build folders from anti-malware scans.
- Keep them on your fastest drive (many read/write operations).
- **IL2CPP Code Generation** (Player Settings): default **Optimize for runtime speed**; **Optimize for code size and
  build time** emits less machine code, cutting build time and binary size at some runtime cost. It also compiles only
  the single fully-sharable version of generic code.
- On Linux and QNX, set **IL2CPP LTO Mode** to Thin (Other Settings > Configuration) for strong optimisation with less
  build time than Full.
- Burst can compile suitable code to optimised machine code alongside IL2CPP.

## AOT limitations (IL2CPP limitations page)
- **Threads:** managed threads are not supported on the Web platform; most `System.Threading` APIs have no effect or
  do not work, and `System.Timers.Timer` depends on threads.
- **Reflection:** supported, but code the compiler cannot see being used via reflection might not exist at runtime
  (managed code stripping). `System.Reflection.Emit` methods cannot be implemented on an AOT platform.
- **Exception filters:** supported, but ordering of filter statements versus `catch` blocks differs because IL2CPP uses
  C++ exceptions; a filter that writes a field can behave differently from Mono. Avoid side effects in filters.
- **Serialization:** types used only via reflection during serialization may not get code generated.
- **Generics:** IL2CPP must know which generic instances exist; `List<int>` and `List<double>` need different code, but
  reference types share code (`List<object>` and `List<string>`). Instances created only at runtime (for example with
  `Activator.CreateInstance(typeof(SomeGenericType<>).MakeGenericType(...))`, invoking static methods of such
  instances, `MakeGenericMethod`, some generic virtual calls, deeply nested generic value types) get slower fallback
  code. To keep it fast: `where : class` when the argument is always a reference type; `where : struct` enables some
  optimisations but is still slower; or add a never-called method named `UsedOnlyForAOTCodeGeneration` that references the
  needed instances (the page shows the pattern).
- **Native callbacks:** a managed method marshaled to a C function pointer must be static with the `[MonoPInvokeCallback]`
  attribute; generic ones may need `[MonoPInvokeCallback(typeof(...))]` overloads.
- **Unsupported:** reflection of `MarshalAs` and `FieldOffset` attributes (supported at compile time), the C# `dynamic`
  keyword, `Marshal.Prelink`/`PrelinkAll`, `System.Diagnostics.Process`. Where needed on desktop platforms, use the Mono
  scripting back end.

## Checked
Date: 2026-11-07.
Read in full: "Introduction to IL2CPP" and "IL2CPP limitations" (6000.6 docs, including the AOT generics and
`MonoPInvokeCallback` code blocks as stripped text).
Corrected: the draft said IL2CPP was "required" for iOS, consoles, WebGL and Android 64-bit and that Mono on Android was
32-bit only; the page says IL2CPP is supported on all platforms and was developed for platforms without JIT. It named the
code generation options "Faster runtime" and "Faster (smaller) builds"; the page names them "Optimize for runtime speed"
and "Optimize for code size and build time".
Removed as unconfirmed: the build-time/runtime comparison table figures, "full generic sharing (2022.1+)", the C++
Compiler Configuration (Debug/Release/Master) advice, `Il2CppSetOption` null/bounds checks, Script Debugging attach steps,
the symbols and crash-stack section, the Gotchas and the invented Verify checklist.
Method: documentation only; no commands were run.
