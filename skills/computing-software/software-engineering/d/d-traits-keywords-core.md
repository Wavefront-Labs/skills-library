---
id: computing-software.software-engineering.d.d-traits-keywords-core
name: d-traits-keywords-core
category: computing-software
field: software-engineering
product: d
tags: [d-traits-keywords-core, traits, __traits, allmembers, getmember, identifier, hasmember, getoverloads, reflection, compile-time-reflection, d]
level: advanced
status: draft
description: "Reflect over types and symbols with __traits (allMembers, derivedMembers, getMember, identifier, hasMember, parent, isSame, getOverloads, getVirtualMethods)."
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

# __traits: allMembers, getMember, identifier, hasMember, isSame

Goal: write code that adapts to a type's shape.

```d
foreach (name; __traits(allMembers, S)) {
    alias M = __traits(getMember, S, name);
    static if (is(typeof(M) == int)) pragma(msg, name);
}
```
- Discovery: `allMembers`, `derivedMembers` (no inherited), `getMember(T, "name")`, `hasMember(T, "name")`, `getOverloads(T, "name")`, `getVirtualMethods`, `parent`, `getAliasThis`.
- Info: `identifier`, `isStaticFunction`, `isVirtualFunction`, `isAbstractClass`, `isFinalFunction`, `isPOD`, `isCopyable` , `isSame(a, b)`, `isTemplate`, `getProtection` (visibility: "public", "private" ...), `getLinkage`, `getFunctionAttributes`, `getParameterStorageClasses`, `classInstanceSize`, `getAttributes`.
- Validity: `compiles`, `isArithmetic`, `isIntegral`, `isFloating`, `isScalar`, `isStaticArray`, `isAssociativeArray`.
- `allMembers` includes `this`, `__ctor`, `Object` members for classes; filter them out (`name != "this"`, skip names starting `__`).
- Combine with `static foreach` to generate serialisers, bindings, command-line parsers.

Gotchas:
- `getMember` on a private symbol from another module fails; check `getProtection` first.
- Traits give declaration data, not instance values: use `mixin("obj." ~ name)` or `__traits(getMember, obj, name)`.

Verify: unittest asserting `__traits(allMembers, S)` equals the expected list.
