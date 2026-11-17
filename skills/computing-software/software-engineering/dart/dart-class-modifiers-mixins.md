---
id: computing-software.software-engineering.dart.dart-class-modifiers-mixins
name: dart-class-modifiers-mixins
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-inheritance, class-modifiers-mixins]
level: advanced
status: docs-checked
description: "Apply Dart 3 class modifiers and mixins to control extension and implementation."
sources: ["https://dart.dev/language/class-modifiers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sealed, base, final, interface classes and mixins
- Dart 3 modifiers: `abstract`, `base`, `final`, `interface`, `sealed`, `mixin` (and `mixin class`, combinable with `abstract` or `base` only); they control how a class can be used inside and outside its library.
- `sealed class Shape {}` lets the compiler check a switch covers all direct subtypes; it cannot be instantiated, and it cannot be extended or implemented outside its library.
- `mixin Logger { void log(String m) => print(m); }`, `class A with Logger`.
- Unmodified and `interface` classes can be implemented from other libraries; `base`, `final` and `sealed` restrict implementation outside the library.
Verify: compile code that violates a modifier in another library.

## Checked

Date: 2026-11-02. Confirmed on Dart Class modifiers page (modifier list, sealed, mixin class combinations, implements restrictions). Fixed: 'implements works unless base/final' omitted sealed and misdescribed interface. Removed as not confirmed: the `on` clause remark.

Method: documentation only; no commands were run.
