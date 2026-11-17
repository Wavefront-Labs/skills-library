---
id: computing-software.software-engineering.d.d-user-defined-attributes
name: d-user-defined-attributes
category: computing-software
field: software-engineering
product: d
tags: [d-user-defined-attributes, attributes, uda, user-defined-attributes, getattributes, hasuda, getudas, d]
level: advanced
status: docs-checked
description: "Attach metadata with @(...) UDAs and read them with __traits(getAttributes) and std.traits hasUDA / getUDAs for serialisation and DSL style reflection."
sources:
  - https://dlang.org/spec/attribute.html
  - https://dlang.org/phobos/std_traits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-defined attributes (UDAs)

Goal: tag declarations and act on tags at compile time.

```d
struct Column { string name; }
enum Skip;
struct Row { @Column("id") int id; @Skip string tmp; }
static foreach (m; __traits(allMembers, Row)) {
    static if (hasUDA!(__traits(getMember, Row, m), Skip)) {}
    else pragma(msg, getUDAs!(__traits(getMember, Row, m), Column));
}
```
- Syntax: `@Column("id")`, `@(1, "a")`, or an enum/struct type name used as `@Skip`.
- Read: `__traits(getAttributes, sym)`; `std.traits.hasUDA!(sym, T)`, `getUDAs!(sym, T)`.
- UDAs are compile-time annotations on declarations (including function parameters); several in scope are concatenated, and `__traits(getAttributes, s)` returns an empty sequence when there are none.
- A type-as-UDA (`@Skip`) is retrieved as the type; a value-UDA as the value (use a struct for typed lookups).

Gotchas:
- The attribute of a type name is not the attribute of a variable of that type: `getAttributes` on `typeof(a)` and on `a` differ.

Verify: `static assert(hasUDA!(Row.id, Column));`

## Checked

Date 2026-11-02. Confirmed UDA syntax, __traits(getAttributes), hasUDA, getUDAs and parameter UDAs (Attributes spec, std.traits). Removed the claims about compiler-known attributes and getMember.

Method: documentation only; no commands were run.
