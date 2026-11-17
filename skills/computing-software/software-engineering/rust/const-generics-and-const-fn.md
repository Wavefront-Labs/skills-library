---
id: computing-software.software-engineering.rust.const-generics-and-const-fn
name: const-generics-and-const-fn
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-traits-generics, rust-const-generics, const-generics, const-fn, arrays]
level: advanced
status: docs-checked
description: "Parameterise Rust types by values with const generics, the allowed parameter types and standalone-use rule, and compile-time evaluation in const contexts."
sources:
  - https://doc.rust-lang.org/reference/items/generics.html
  - https://doc.rust-lang.org/reference/const_eval.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Const generics and const fn

**Goal:** fixed-size, stack-allocated, compile-time checked structures.

```rust
struct Matrix<const R: usize, const C: usize> { data: [[f32; C]; R] }
impl<const R: usize, const C: usize> Matrix<R, C> {
    fn transpose(&self) -> Matrix<C, R> {
        let mut out = [[0.0; R]; C];
        for i in 0..R { for j in 0..C { out[j][i] = self.data[i][j]; } }
        Matrix { data: out }
    }
}
```

Rules from the Rust Reference:
- Const generic parameters make items generic over constant values. The only allowed parameter types are `u8`, `u16`, `u32`, `u64`, `u128`, `usize`, `i8`..`i128`, `isize`, `char` and `bool`.
- Parameters may be declared in any order among type and const parameters, but lifetimes come first.
- In a type or array repeat expression a const parameter must be **standalone**: a single path segment such as `N` or `{N}`, not combined with other expressions (so `[T; N * 2]` is rejected).
- A const argument must be a block expression (`f::<{ 1 + 2 }>()`) unless it is a single identifier or a literal (`f::<1>()`, `f::<-1>()`); `_` is an inferred const, accepted where a const argument is expected but not in item signatures.
- If an argument could be a type or a const, it is resolved as a type; wrap it in braces to force a const.

## Constant evaluation
Expressions in a const context (const items, statics, const generic arguments, `const { }` blocks) must be constant expressions and are always evaluated at compile time. Outside const contexts a constant expression may, but is not guaranteed to, be evaluated at compile time. Out-of-bounds indexing or overflow is a compile error when the value must be evaluated at compile time, otherwise a warning that will likely panic at run time. Writes to statics are not allowed in any constant evaluation context.

## Checked
2026-11-03. Confirmed against the Rust Reference "Generics" (const generics) and "Constant evaluation" pages. Removed: nightly feature names (`adt_const_params`, `generic_const_exprs`), version numbers (1.51, 1.79), `first_n`, `copy_from_slice`, `static_assertions`, `const _: () = assert!`, `Default` for arrays, monomorphisation/stack-size remarks, the `compile_fail` doctest advice, and the claim about what `const fn` bodies may contain.
Method: documentation only; no commands were run.
