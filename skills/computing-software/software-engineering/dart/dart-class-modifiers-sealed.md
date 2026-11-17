---
id: computing-software.software-engineering.dart.dart-class-modifiers-sealed
name: dart-class-modifiers-sealed
category: computing-software
field: software-engineering
product: dart
tags: [dart, class-modifiers-sealed]
level: advanced
status: docs-checked
description: "Apply Dart 3 class modifiers sealed, base, final, interface and mixin class to control subtyping."
sources: ["https://dart.dev/language/class-modifiers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class modifiers (Dart 3)
- `sealed class Shape {}` allows only same-library subtypes and gives exhaustive `switch`.
- `base` requires subtypes to be base/final/sealed; `interface` can be implemented but not extended outside the library; `final` blocks both outside its library.
- `mixin class` can be used both as mixin and class; `abstract` for non-instantiable.
Verify: a switch over a sealed hierarchy with a missing case fails analysis.

## Checked

Date: 2026-11-02. Confirmed on the Class modifiers page: `sealed` blocks extension or implementation outside the library and enables exhaustive switch, `base`, `interface`, `final`, `mixin class`, `abstract`, language version 3.0.

Method: documentation only; no commands were run.
