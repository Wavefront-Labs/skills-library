---
id: computing-software.software-engineering.d.d-class-struct-tupleof-properties
name: d-class-struct-tupleof-properties
category: computing-software
field: software-engineering
product: d
tags: [d-class-struct-tupleof-properties, properties, tupleof, classinfo, typeid, typeinfo, reflection, d]
level: advanced
status: draft
description: "Reflect over fields using .tupleof, aggregate init order, typeid(), classinfo and TypeInfo for runtime type identity; compare with __traits and std.traits."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Class and struct .tupleof, .classinfo, typeid

Goal: iterate struct/class fields and identify runtime types.

- `obj.tupleof` is the tuple of all fields (including private ones inside the module); `foreach (i, v; obj.tupleof) writeln(__traits(identifier, obj.tupleof[i]), "=", v);`
- `typeof(obj.tupleof)` gives types; `FieldNameTuple!S` (std.traits) gives names, `Fields!S` gives types.
- `typeid(expr)` returns `TypeInfo`; for a class reference it returns the dynamic `TypeInfo_Class`; `typeid(obj).name` gives the mangled-qualified name.
- `obj.classinfo` / `typeid(obj)` supports `.base`, `.interfaces`, `.create()` and `Object.factory("pkg.Class")` creates by name if the class has a default ctor.
- Compare dynamic types with `typeid(a) == typeid(b)`, not `is`.

Gotchas:
- Nested (inner) classes carry a hidden context pointer not shown in `.tupleof`.
- `.tupleof` on a class instance requires access rights to private members; across modules use `__traits(getMember...)` with `allMembers` and check protection.

Verify: a unittest comparing `FieldNameTuple!S` to the expected names with `static assert`.
