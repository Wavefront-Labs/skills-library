---
id: computing-software.software-engineering.dart.dart-closures-tearoffs-typedefs
name: dart-closures-tearoffs-typedefs
category: computing-software
field: software-engineering
product: dart
tags: [dart, closures-tearoffs-typedefs]
level: practitioner
status: docs-checked
description: "Pass Dart functions as values: closures capture variables, method tear-offs, and function type aliases."
sources: ["https://dart.dev/language/functions", "https://dart.dev/language/typedefs", "https://dart.dev/language/constructors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures and tear-offs
- `var f = (int x) => x + 1;` closures capture variables from their lexical scope.
- Tear-off: `list.forEach(print)`, `items.map(Item.fromJson)`; constructor tear-offs `Foo.new`.
- `typedef Cb = void Function(String)`; generic `typedef Json<T> = T Function(Map<String, dynamic>)`.
- Optional positional `[x]`, named `{x}`, `required`; defaults must be const.
Verify: `charCodes.map(StringBuffer.new)` style constructor tear-offs compile.

## Checked

Date: 2026-11-02. Confirmed on the Functions page: closures capture variables in their lexical scope, optional positional and named parameters, `required`, default values must be compile-time constants; Typedefs page; constructor tear-off `StringBuffer.new` on the Constructors page. Removed the 'by reference' wording and the `int.parse` check (not stated).

Method: documentation only; no commands were run.
