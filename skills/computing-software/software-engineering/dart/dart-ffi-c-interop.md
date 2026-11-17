---
id: computing-software.software-engineering.dart.dart-ffi-c-interop
name: dart-ffi-c-interop
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-ffi, ffi-c-interop]
level: advanced
status: docs-checked
description: "Call C from Dart with dart:ffi: typedefs, DynamicLibrary lookup, package:ffigen and build hooks."
sources: ["https://dart.dev/interop/c-interop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart:ffi, ffigen and native memory
- `dart:ffi` is for Dart Native apps (mobile, command-line, server); it can call native C APIs and read, write, allocate and deallocate native memory.
- Steps: `import 'dart:ffi' as ffi;`, declare a typedef with the FFI signature of the C function (for example `typedef hello_world_func = ffi.Void Function();`), open the library with `ffi.DynamicLibrary.open(libraryPath)`, then call `.lookup<ffi.NativeFunction<hello_world_func>>('hello_world')` and convert the pointer with `asFunction`.
- `package:ffigen` generates the Dart bindings from C header files for large API surfaces.
- Dart build hooks (formerly native assets) let a package contain native code that is built, bundled and available at runtime; see the Hooks page.
- Bugs in native memory handling can crash the process; test with known inputs and outputs.
Verify: a unit test with known inputs and outputs.

## Checked
2026-11-03. Confirmed against dart.dev interop/c-interop (dart:ffi scope, hello_world steps, DynamicLibrary.open, lookup, ffigen, hooks). Removed: `lookupFunction`, `package:ffi` (`calloc`, `Utf8`, `Arena`), `jnigen` and Objective-C/Swift ffigen claims, and the sanitiser advice (not on the page read).
Method: documentation only; no commands were run.
