---
id: computing-software.software-engineering.objective-c.block-syntax
name: block-syntax
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-blocks, block-syntax]
level: intro
status: docs-checked
description: "Declare, define, typedef and call blocks including the ^ syntax and as method parameters."
sources:
  - https://clang.llvm.org/docs/BlockLanguageSpec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Block syntax
**Goal:** write block types and literals without lookup.

```c
int (^add)(int, int) = ^(int a, int b) { return a + b; };
int r = add(2, 3);
void (^later)(void) = ^{ printf("hello world\n"); };
void (^arrayOfTen[10])(int);
```
- A block variable is declared like a function pointer with `^` in place of `*`: `int (^)(char, float)` is a block taking a `char` and a `float` and returning `int`.
- A block with no arguments must specify `void` in the declaration; an empty list does not mean unspecified in the specification (gcc and clang accept K&R style as a convenience). Variadic `...` is supported.
- A block literal is `^ block_decl compound_statement_body`. The return type is optional and inferred from the return statements; if several return a value, all must have the same type; no value means `void`.
- If the return type is omitted and the argument list is `(void)`, the list may be omitted: `^(void){...}` and `^{...}` are equivalent.
- A block is invoked with function call syntax: `x('a')`, `(*y)('a')`.
- A block reference may be cast to a pointer of any type and back, but may not be dereferenced with `*`.

## Gotchas
- Return statements in one block that return different types are an error.

## Self-check
Compile one block of each form above.

## Checked
2026-11-02. Confirmed against the Clang "Language Specification for Blocks": block type syntax, declarations, literal grammar, return type inference, omitted `(void)`, invoke operator, cast and dereference rules. Removed: `NSStackBlock`/`NSMallocBlock`/`NSGlobalBlock` and nil-block-call claims, Foundation `enumerateObjectsUsingBlock:` and typedef examples, `-Wstrict-prototypes` advice.
Method: documentation only; no commands were run.
