---
id: computing-software.software-engineering.dart.dart-params-closures
name: dart-params-closures
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-functions, params-closures]
level: practitioner
status: docs-checked
description: "Declare positional optional, named and required parameters and use closures and tear-offs."
sources: ["https://dart.dev/language/functions", "https://dart.dev/language/loops"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional, named and required parameters and closures
- `void f(int a, [int b = 0])` optional positional; `void g({required int a, int b = 0})` named.
- Arrow `=>` bodies; function types `int Function(int)`; tear-off `list.forEach(print)`; closures capture variables from their lexical scope (a closure inside a `for` loop captures the value of the index).
- `typedef Cb = void Function(String);`.
- A function body without a `return` statement implicitly returns `null`.
Verify: call with missing required named arguments and read the error.

## Checked

Date: 2026-11-02. Confirmed on the Functions page: optional positional and named parameters, `required`, lexical scope closures, implicit `return null`; Loops page: closures in `for` capture the value of the index. Removed the claim that required named parameters cannot have defaults (not stated).

Method: documentation only; no commands were run.
