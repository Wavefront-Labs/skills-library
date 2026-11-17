---
id: computing-software.software-engineering.dart.dart-getters-setters-operators-call
name: dart-getters-setters-operators-call
category: computing-software
field: software-engineering
product: dart
tags: [dart, getters-setters-operators-call]
level: practitioner
status: docs-checked
description: "Define getters/setters, override operators (==, hashCode, []), and make objects callable."
sources: ["https://dart.dev/language/methods", "https://dart.dev/language/callable-objects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Members
- `double get area => w * h;` `set w(double v) {...}`.
- Override `==` together with `hashCode` (`Object.hash(a, b)`); `operator +(Vec o)`.
- `call()` makes an instance invokable like a function.
- `static` members; abstract methods only in abstract classes or mixins.
Verify: put two equal objects in a Set and get length 1.

## Checked

Date: 2026-11-02. Confirmed on the Methods page: getters and setters, operators, `==` with `hashCode` and `Object.hash`, abstract methods, `static`; Callable objects page: `call()`. Removed the `[]` operator example and `external` (not stated in the pages read).

Method: documentation only; no commands were run.
