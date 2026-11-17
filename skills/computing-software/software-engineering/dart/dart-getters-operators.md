---
id: computing-software.software-engineering.dart.dart-getters-operators
name: dart-getters-operators
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-classes, getters-operators]
level: practitioner
status: docs-checked
description: "Define properties, override operators, == and hashCode together and implement toString."
sources: ["https://dart.dev/language/methods", "https://dart.dev/language/callable-objects", "https://dart.dev/language/libraries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getters, setters, operators and toString
- `int get area => w * h;` `set size(int v) {...}`; private members start with `_` and are library-private, not class-private.
- Override `==` and `hashCode` together; use `Object.hash(a, b)`; records get structural equality without writing `==`.
- `operator +(Vec o) => Vec(x + o.x)`.
- `call()` makes an object callable.
Verify: put instances into a `Set` and check duplicates collapse.

## Checked

Date: 2026-11-02. Confirmed on the Methods page: getters, setters, `operator` declarations, `==` overridden with `hashCode` via `Object.hash`; Libraries page: leading underscore means library privacy; Callable objects page: `call()`; Records page: equality. Removed `package:equatable` and code generation advice (not stated).

Method: documentation only; no commands were run.
