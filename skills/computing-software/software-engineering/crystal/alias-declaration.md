---
id: computing-software.software-engineering.crystal.alias-declaration
name: alias-declaration
category: computing-software
field: software-engineering
product: crystal
tags: [alias-declaration, alias-types, alias, type-alias, recursive-alias, json-any, nickname, crystal]
level: practitioner
status: docs-checked
description: "Name complex types with alias in Crystal, including recursive JSON-like types."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/alias.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# alias declarations

Goal: shorten and recurse types.

```crystal
alias PInt32 = Pointer(Int32)
alias RecArray = Array(Int32) | Array(RecArray)
module Json
  alias Type = Nil | Bool | Int64 | Float64 | String | Array(Type) | Hash(String, Type)
end
```
- Each use of an alias is replaced by the type it refers to by the compiler, so `PInt32.malloc(1)` is a `Pointer(Int32)`.
- Aliases give long type names a short name and let you describe recursive types (`RecArray`, `Json::Type`).
- An alias can be declared inside a module, as `Json::Type` is.

Verify: use the alias in a method signature and compile.

## Checked
Checked 2026-11-02 against the crystal-book `alias` page. Confirmed: replacement by the compiler, the recursive `RecArray` and `Json::Type` examples, alias inside a module. Removed: claims about alias cycles, error-message display, aliasing generics with parameters, the absence of a method alias keyword and the `Foo` handler example.

Method: documentation only; no commands were run.
