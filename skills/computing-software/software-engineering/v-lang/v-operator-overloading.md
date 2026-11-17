---
id: computing-software.software-engineering.v-lang.v-operator-overloading
name: v-operator-overloading
category: computing-software
field: software-engineering
product: v-lang
tags: [v-operator-overloading, methods, operator overloading, +, -, str method, vector, comparison, v-lang]
level: advanced
status: docs-checked
description: "Overload arithmetic and comparison operators on structs with fn (a T) + (b T) T and the limits on which operators are allowed."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading

Goal: make user types behave like numbers.

```v
struct Vec {
	x int
	y int
}

fn (a Vec) str() string {
	return '{${a.x}, ${a.y}}'
}

fn (a Vec) + (b Vec) Vec {
	return Vec{a.x + b.x, a.y + b.y}
}

fn (a Vec) - (b Vec) Vec {
	return Vec{a.x - b.x, a.y - b.y}
}
```
- Overloadable binary operators: `+, -, *, **, /, %, <, ==`. Indexing can be overloaded too: `fn (b Buffer) [] (index int) int` and `fn (mut b Buffer) []= (index int, value int)`; custom types can take `SliceIndex` or `[]SliceIndex` for slice and multidimensional syntax.
- Generated automatically: `==` (can be overridden); `!=`, `>`, `<=`, `>=` once `==` and `<` are defined (cannot be overridden); assignment operators such as `+=` when the operator exists and operands have the same type (cannot be overridden). In the example `c += a` works from the `+` overload.
- Restrictions: `<` and `==` must return `bool`; both arguments must have the same type; overloaded operators return the same type as the argument (except `<` and `==`); enums and interfaces cannot overload operators, but an alias of an enum can; `[]` and `[]=` only on structs and type aliases; `[]` takes exactly one parameter and returns a value; `[]=` takes an index and a value, uses a `mut` receiver and returns nothing.
- Arguments cannot be changed inside overloads; calling other functions inside operator functions is not allowed (planned).
- Define `str()` for printing (as in the example).
- Types in different modules can define their own operators even when type names match.

Verify: `assert Vec{2, 3} + Vec{4, 5} == Vec{6, 8}`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Limited operator overloading" and its subsections). Fixed: the earlier text omitted `**` and said return type is arbitrary for arithmetic; the docs require it to match the argument type. Removed as not stated there: the same-module rule for overloads, the mixed-type reverse-order gotcha, the V2/`*` float example.

Method: documentation only; no commands were run.
