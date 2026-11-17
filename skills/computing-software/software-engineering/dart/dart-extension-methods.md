---
id: computing-software.software-engineering.dart.dart-extension-methods
name: dart-extension-methods
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-extension-methods, extension-methods]
level: practitioner
status: docs-checked
description: "Add methods to existing types with extensions and zero-cost wrappers with extension types."
sources: ["https://dart.dev/language/extension-methods", "https://dart.dev/language/extension-types", "https://dart.dev/blog/new-in-dart-3-3-extension-types-javascript-interop-and-more"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extensions and extension types
- `extension StringX on String { bool get isBlank => trim().isEmpty; }` resolved statically; they do not work on `dynamic`.
- Name conflicts between extensions are resolved by explicit application: `StringX(s).isBlank`.
- Extension types (Dart 3.3 or newer) `extension type Id(int v) {}` wrap a representation type without runtime cost, giving a distinct static type.
Verify: the extension is not visible unless its library is imported.

## Checked

Date: 2026-11-02. Confirmed on the Extension methods page: static resolution, no calls on `dynamic`, named extensions to resolve API conflicts, import of the declaring library; Extension types page: wrapping a representation type; Dart 3.3 launch on the Dart 3.3 blog. Removed the instance-fields claim (not stated).

Method: documentation only; no commands were run.
