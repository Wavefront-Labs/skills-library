---
id: computing-software.software-engineering.d.d-inout-and-qualifier-templates
name: d-inout-and-qualifier-templates
category: computing-software
field: software-engineering
product: d
tags: [d-inout-and-qualifier-templates, const-immutable, inout, wild-qualifier, qualifier-generic, auto-ref, const-overload, d]
level: advanced
status: draft
description: "Write one function for mutable, const and immutable arguments with inout, plus inout return, and the template alternative (auto ref / T param)."
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

# inout parameters and qualifier-generic code

Goal: avoid writing three overloads.

```d
inout(char)[] firstWord(inout(char)[] s) {
    foreach (i, c; s) if (c == ' ') return s[0 .. i];
    return s;
}
```
- `inout` is a placeholder that becomes the actual qualifier of the argument (mutable, const, immutable); the return carries the same one.
- All `inout` occurrences in a signature resolve to the same qualifier, and are usable on member functions: `inout(T) front() inout`.
- Passing `inout` data to a function requires it to be const-or-inout for modification safety.
- `ref` plus `inout` forwards references; `auto ref` binds both lvalues and rvalues in templates.
- Related: `Unqual!T`, `CopyConstness!(From, To)`, `std.traits.isMutable`.

Gotchas:
- You cannot write to `inout` data; it is const inside.
- Mixed qualifiers across inout params can decay to const.

Verify: call with `char[]`, `const(char)[]`, `string` and assert return typeof matches via `typeof`.
