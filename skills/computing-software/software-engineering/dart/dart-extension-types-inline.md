---
id: computing-software.software-engineering.dart.dart-extension-types-inline
name: dart-extension-types-inline
category: computing-software
field: software-engineering
product: dart
tags: [dart, extension-types-inline]
level: advanced
status: docs-checked
description: "Wrap a representation type with zero-cost Dart 3.3 extension types, implement interfaces, and hide members."
sources: ["https://dart.dev/language/extension-types", "https://dart.dev/blog/new-in-dart-3-3-extension-types-javascript-interop-and-more"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension types
- `extension type Id(int value) { Id.parse(String s) : this(int.parse(s)); }` is compiled away: it is a static-only interface over the representation type, so no wrapper object exists at run time (introduced in Dart 3.3).
- Members of the representation type are not members of the extension type unless you redeclare them. `implements int` (the representation type, or a supertype of it) makes its members available and makes the extension type a subtype; omit it to hide them.
- Use `@redeclare` (from `package:meta`) when you deliberately reuse a supertype member name; the lint `annotate_redeclares` warns when you hide one without it.
- Hide the default constructor with a private one: `extension type E._(int i) { E.fromString(String s) : i = int.parse(s); }`.
- Not a safe runtime boundary: `is`, `as` and pattern matches evaluate against the representation object, so `x is Id` tests the representation type, and `List<Id>` is `List<int>` at run time. Writing `Id(i)` is the only way to run constructor validation.
- Good for typed IDs and for static JS interop, for example `extension type Foo(JSObject _)`; prefer a real wrapper class when you need run-time encapsulation.

Verify: assigning an Id to an int variable fails to compile unless the extension type implements int.

## Checked

Checked 2026-11-08 against https://dart.dev/language/extension-types (read in full) and the Dart 3.3 announcement blog post (read for the 3.3 version gate, zero-cost wrapper and JSObject examples). Removed the claim about units as a use case, which neither page states.

Method: documentation only; no commands were run.
