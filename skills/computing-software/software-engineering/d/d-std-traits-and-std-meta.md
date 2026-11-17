---
id: computing-software.software-engineering.d.d-std-traits-and-std-meta
name: d-std-traits-and-std-meta
category: computing-software
field: software-engineering
product: d
tags: [d-std-traits-and-std-meta, traits, std-traits, std-meta, returntype, parameters, fieldnametuple, iscallable, aliasseq, hasuda, fullyqualifiedname, d]
level: practitioner
status: docs-checked
description: "Use std.traits (ReturnType, Parameters, FieldNameTuple, isCallable, Unqual, hasUDA) and std.meta (AliasSeq, staticMap, Filter, Replace) instead of hand-rolled traits."
sources:
  - https://dlang.org/phobos/std_traits.html
  - https://dlang.org/phobos/std_meta.html
  - https://dlang.org/spec/traits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.traits and std.meta utilities

Goal: reuse library templates for reflection.

- Function info: `ReturnType!f`, `Parameters!f`, `ParameterIdentifierTuple!f`, `ParameterDefaults!f`, `arity!f`, `functionAttributes!f`, `SetFunctionAttributes`, `isCallable!x`, `isSafe!f`.
- Type info: `isIntegral`, `isFloatingPoint`, `isNumeric`, `isSomeString`, `isSomeChar`, `isPointer`, `isArray`, `isAssociativeArray`, `isAggregateType`, `isSigned`, `isUnsigned`, `isInstanceOf!(Template, T)`.
- Qualifiers: `Unqual`, `CopyConstness`, `isMutable` (true for `string`, which is `immutable(char)[]`), `Largest`, `CommonType`, `Select!(cond, A, B)`.
- Fields/enum: `FieldNameTuple!S`, `Fields!S`, `hasIndirections`, `EnumMembers!E`, `OriginalType!E`, `BaseClassesTuple`, `InterfacesTuple`, `TransitiveBaseTypeTuple`.
- Naming: `fullyQualifiedName!T`, `moduleName!sym`, `packageName!sym`.
- Sequences in `std.meta`: `AliasSeq`, `staticMap`, `Filter`, `Alias`, `staticSort`, `Stride`, `Repeat`, `aliasSeqOf`.

Gotchas:
- `ReturnType` of an overloaded name needs a specific overload; list them with `__traits(getOverloads, ...)`.

Verify: `static assert(is(ReturnType!(typeof(&f)) == int));`

## Checked

2026-11-03. Confirmed against: std.traits, std.meta and the traits spec page (`__traits(getOverloads)`).

Removed because the pages read did not confirm it: `isImmutable` (not in std.traits; use `isMutable`), the `isSomeString` const-qualifier claim.

Method: documentation only; no commands were run.
