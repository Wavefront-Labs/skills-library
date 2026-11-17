---
id: computing-software.software-engineering.dart.dart-dart-compile-targets
name: dart-dart-compile-targets
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-compilation, dart-compile-targets]
level: advanced
status: docs-checked
description: "Choose between dart run, AOT exe, kernel snapshot, JavaScript and WebAssembly outputs."
sources: ["https://dart.dev/tools/dart-compile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JIT, AOT, kernel, JS and Wasm
- `dart run` uses the Dart VM's JIT compiler; `dart compile` has subcommands `exe`, `aot-snapshot` (run with `dartaotruntime`), `jit-snapshot`, `kernel`, `js` and `wasm`.
- `dart compile js -O2 -o out/main.js web/main.dart`; `-O0` to `-O4` set optimisation and `-o` the output.
- `exe` and `aot-snapshot` have no support for `dart:mirrors` and `dart:developer`; use code generation for reflection-like needs.
- For `js` and `wasm`, `-D<key>=<value>` sets a compile-time declaration, read via `String.fromEnvironment('key')`.
Verify: run the compiled artefact and compare output with `dart run`.

## Checked

Date: 2026-11-02. Confirmed on Dart 'dart compile' page (subcommands, dartaotruntime, -O and -o, -D, AOT limitations, dart run JIT). Fixed: the runtime is dartaotruntime, not dartaot. Removed as not confirmed: hot reload under `dart run`, Wasm minimum version.

Method: documentation only; no commands were run.
