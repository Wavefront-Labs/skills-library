---
id: computing-software.software-engineering.objective-c.type-encodings
name: type-encodings
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-types, type-encodings]
level: sme
status: docs-checked
description: "Read Objective-C type encoding strings produced by @encode, including struct, array, pointer codes and the method qualifier codes."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type encodings
**Goal:** decode the strings the compiler stores for method and variable types.

```objc
char *buf1 = @encode(int **);
char *buf2 = @encode(struct key);
char *buf3 = @encode(Rectangle);
```
- The compiler encodes each method's return and argument types in a string associated with the selector; `@encode(type)` returns the encoding for any type usable with `sizeof()`.
- Basic codes: `c` char, `i` int, `s` short, `l` long (32-bit even in 64-bit programs), `q` long long, `C` `I` `S` `L` `Q` the unsigned forms, `f` float, `d` double, `B` C++ `bool` or C99 `_Bool`, `v` void, `*` `char *`, `@` object (static type or `id`), `#` `Class`, `:` `SEL`, `?` unknown (also function pointers).
- Compound codes: `[12^f]` an array of 12 pointers to float (count first, inside square brackets), `{name=type...}` a structure, `(name=type...)` a union, `bnum` a bit field of `num` bits, `^type` a pointer to type.
- Structure example: `struct example { id anObject; char *aString; int anInt; }` encodes as `{example=@*i}`; a pointer to it is `^{example=@*i}`, and another level of indirection drops the fields: `^^{example}`.
- Objects are treated like structures: `@encode` of the `NSObject` class name gives `{NSObject=#}`, since its only ivar is `isa`.
- `@encode(long double)` returns `d`, the same as `double`; `long double` is not supported.
- The runtime also uses qualifier codes for protocol method declarations: `r` const, `n` in, `N` inout, `o` out, `O` bycopy, `R` byref, `V` oneway. `@encode()` does not return them.

## Gotchas
- `B` is `bool` / `_Bool`; the guide's table does not list a separate code for the Objective-C `BOOL` type, so check the type you use.

## Self-check
Print `@encode` of a struct you own and compare with the `{name=...}` rule above.

## Checked
2026-11-03. Confirmed against the Objective-C Runtime Programming Guide, "Type Encodings" (Tables 6-1 and 6-2, array, struct and pointer examples, long double note). Removed: `method_getTypeEncoding` / `property_getAttributes` examples, frame-size and offset layouts such as `v24@0:8@16`, property attribute letters, `BOOL` as `c` on x86 and the 32/64-bit offset remarks (not on the page).
Method: documentation only; no commands were run.
