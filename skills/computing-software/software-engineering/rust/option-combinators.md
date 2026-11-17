---
id: computing-software.software-engineering.rust.option-combinators
name: option-combinators
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-option, option-combinators, result-combinators, ok-or, and-then, map, unwrap-or, question-mark-operator]
level: practitioner
status: verified
description: "Use Rust Option and Result combinators fluently: map, and_then, ok_or(_else), unwrap_or(_else/default), filter, take, as_ref/as_deref, transpose, zip, and ? on Option."
sources: ["https://doc.rust-lang.org/std/option/enum.Option.html", "https://doc.rust-lang.org/std/result/enum.Result.html", "https://doc.rust-lang.org/std/option/index.html#method-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option combinators

**Goal:** handle absence without nested `match` blocks or panicking `unwrap()`, choosing the
combinator that states intent.

## Cheat sheet
| Want | Use |
|---|---|
| transform the value if present | `opt.map(f)` |
| chain another Option-returning step | `opt.and_then(f)` |
| keep only if predicate holds | `opt.filter(pred)` |
| default value | `unwrap_or(v)` (eager), `unwrap_or_else(f)` (lazy), `unwrap_or_default()` |
| fallback Option | `opt.or(other)`, `or_else(f)`, `xor` |
| convert to Result | `ok_or(err)`, `ok_or_else(|| err)` |
| Result to Option | `res.ok()`, `res.err()` |
| borrow inner value | `as_ref()`, `as_mut()`, `as_deref()` (`Option<String>` -> `Option<&str>`) |
| take and leave None | `opt.take()`; `replace(v)`; `get_or_insert_with(f)` |
| test without consuming | `is_some()`, `is_none()`, `is_some_and(pred)`, `is_none_or(pred)` (1.82) |
| combine two | `a.zip(b)` -> `Option<(A, B)>` |
| flip nesting | `Option<Result<T,E>>::transpose()` -> `Result<Option<T>,E>` |
| flatten | `Option<Option<T>>::flatten()` |
| side effect | `if let Some(x) = &opt { .. }` (or `inspect` on 1.76+) |

## Patterns
```rust
// ? works on Option inside a function returning Option
fn middle_initial(p: &Person) -> Option<char> {
    p.middle_name.as_deref()?.chars().next()
}

// convert absence to an error at the boundary
let port: u16 = env::var("PORT").ok()
    .map(|s| s.parse()).transpose()?        // Option<Result<u16,_>> -> Result<Option<u16>,_>
    .unwrap_or(8080);

let user = users.get(&id).ok_or_else(|| Error::NotFound(id))?;

// lazy defaults: avoid computing an expensive fallback when not needed
let name = cfg.name.clone().unwrap_or_else(|| hostname());
```
- `unwrap_or(expensive())` evaluates `expensive()` even when Some; use `_else` variants for anything
  that allocates or has side effects (clippy `or_fun_call`).
- `ok_or(format!(..))` allocates eagerly; use `ok_or_else`.
- Iterators: `filter_map`, `flat_map`, `.find()`, `.next()`, `.max()` all return Option; collecting
  `Iterator<Item = Option<T>>` into `Option<Vec<T>>` short-circuits on the first None.

## unwrap and expect
Use `expect("reason this cannot fail")` only for true invariants (a regex literal, a value just
inserted). In libraries prefer returning an error. `unwrap()` in tests is fine.

## Result equivalents
`map_err` (convert error type), `and_then`, `or_else`, `unwrap_or_else`, `inspect_err` (log and pass
through), `is_ok_and`. `Result<T, E>::ok()` drops error info - only when you truly do not care.

## Gotchas
- `map` with a function returning Option gives `Option<Option<T>>`: you wanted `and_then`.
- `Option<&T>::cloned()` / `copied()` to get owned values.
- Matching `Some(ref x)` is rarely needed now: `if let Some(x) = &opt` or `opt.as_ref()`.

## Verify
- [ ] Clippy clean: `or_fun_call`, `option_map_unit_fn`, `manual_map`, `unnecessary_lazy_evaluations`.
- [ ] No `unwrap()` in non-test library code without a documented invariant.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran every row of the cheat sheet and every pattern: `map`, `and_then`, `filter`, `unwrap_or`/`_else`/`_default`, `or`, `xor`, `or_else`, `ok_or`, `ok`, `as_deref`, `take`, `replace`, `get_or_insert_with`, `is_some_and`, `is_none_or`, `zip`, `flatten`, `transpose`, `inspect`, `is_ok_and`, `inspect_err`, collect into `Option<Vec<_>>` (short-circuits on None), `cloned`/`copied`; `middle_initial` with `as_deref()?`; the `env::var("PORT").ok().map(|s| s.parse()).transpose()?.unwrap_or(8080)` pattern gave `Ok(8080)` unset, `Ok(9000)` set and an error for `x`; `ok_or_else` gave `Err(NotFound(2))`.
- Stability from the std source: `is_none_or` `#[stable(... since = "1.82.0")]`; Rust 1.76.0 release notes list `Option::inspect` and `Result::inspect`. Clippy lint names `or_fun_call`, `option_map_unit_fn`, `manual_map`, `unnecessary_lazy_evaluations` accepted by clippy-driver.
