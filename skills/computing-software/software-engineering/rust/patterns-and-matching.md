---
id: computing-software.software-engineering.rust.patterns-and-matching
name: patterns-and-matching
category: computing-software
field: software-engineering
product: rust
tags: [rust, let-else, rust-patterns, match, if-let, match-ergonomics, destructuring, binding-modes, exhaustiveness, rust-pattern-matching, rust-let-else]
level: practitioner
status: verified
description: "Write idiomatic Rust pattern matching: exhaustive match, let-else early returns, if-let chains, match ergonomics and binding modes, guards, @ bindings and slice patterns."
sources: ["https://doc.rust-lang.org/book/ch19-00-patterns.html", "https://doc.rust-lang.org/reference/patterns.html", "https://doc.rust-lang.org/rust-by-example/flow_control/let_else.html", "https://doc.rust-lang.org/reference/expressions/if-expr.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Patterns and matching

**Goal:** flat, exhaustive control flow over enums and data shapes, with no needless clones or
nested `if let` pyramids.

## match: exhaustive by design
```rust
match cmd {
    Cmd::Get { key } => get(key),
    Cmd::Set { key, value } if value.len() <= MAX => set(key, value),
    Cmd::Set { .. } => Err(TooLarge),
    Cmd::Ping | Cmd::Echo(_) => Ok(Pong),
}
```
- Prefer listing variants over a trailing `_` so adding a variant forces you to handle it.
- Guards (`if ...`) do not count toward exhaustiveness.
- `x @ 1..=9` binds while testing a range; `Some(n @ (1 | 2))` with or-patterns.

## let-else: early return with a binding
```rust
let Some(user) = repo.find(id) else {
    return Err(Error::NotFound(id));
};
let [first, .., last] = parts.as_slice() else { bail!("need at least 2 parts") };
```
The else block must diverge (`return`, `break`, `continue`, `panic!`). It keeps the happy path
unindented, replacing `match x { Some(v) => v, None => return .. }`.

## if let and let chains
```rust
if let Some(v) = map.get(k) { use_it(v) }
// Edition 2024 (Rust 1.88+): let chains
if let Some(u) = user && u.is_admin() && let Some(t) = u.token() { .. }
```
On older editions use `match` or `matches!(x, Pat if cond)` for boolean checks. `while let Some(x)
= stack.pop()` for loops.

## Match ergonomics and binding modes
Matching a reference against a non-reference pattern auto-dereferences and binds by reference:
```rust
let opt: &Option<String> = &Some("a".into());
if let Some(s) = opt { /* s: &String, nothing moved */ }
```
- Matching an owned value moves non-Copy fields out: `match opt { Some(s) => .. }` consumes `opt`.
  Match on `&opt` or `opt.as_ref()` / `as_mut()` / `as_deref()` to borrow.
- `ref` / `ref mut` explicitly bind by reference inside by-value patterns.
- Edition 2024 tightened rules: writing `&` or `mut`/`ref` explicitly inside a pattern that is
  already in by-reference mode is an error; let the default binding mode work.

## Destructuring
```rust
let Point { x, y: py, .. } = p;                  // rename and ignore rest
for (i, (k, v)) in map.iter().enumerate() {}
match slice { [] => .., [one] => .., [head, tail @ ..] => .. }
match (a, b) { (Some(x), Some(y)) => .., (None, _) | (_, None) => .. }
```
Struct literal shorthand in patterns mirrors construction. Use `_` to ignore one value, `..` for the
rest; `_x` still binds (and moves), `_` does not.

## Gotchas
- A lowercase identifier in a pattern is a new binding, not a comparison with a variable: `match x
  { limit => .. }` always matches. Compare with a guard or use a `const` (uppercase).
- Matching on strings: `match s.as_str()`.
- Clippy helps: `single_match`, `manual_let_else` (pedantic), `match_like_matches_macro`,
  `wildcard_enum_match_arm` (restriction).

## Verify
- [ ] No `_ =>` arms on enums you own unless genuinely open-ended.
- [ ] Clippy pedantic `manual_let_else` clean.
- [ ] No clones introduced just to match on owned data.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, edition 2024. Ran: exhaustive `match` with a guard arm and or-pattern (too large -> `Err`, ok -> `Ok("set")`), `let ... else` with an early return and the `let [first, .., last] = parts else` slice form, a let chain `if let Some(u) = user && u.is_admin() && let Some(t) = u.token()`, `x @ 1..=9`, `Some(n @ (1 | 2))`, `if let Some(s) = &Option<String>` (s is `&String`), struct destructuring with rename and `..`, slice patterns `[]`, `[one]`, `[head, tail @ ..]`, `matches!` with a guard, `while let Some(x) = stack.pop()`.
- Let chains: Rust 1.88.0 release (blog.rust-lang.org/2025/06/26/Rust-1.88.0, fetched) "Let chains are only available in the Rust 2024 edition".
- Edition 2024 binding rule: `if let Some(ref s) = &opt` fails with "cannot explicitly borrow within an implicitly-borrowing pattern", while `&Some(ref s)` compiles. A lowercase identifier in a pattern shadows (`match 10 { limit => ... }` printed `limit=10`). `let (_x, _) = t` moves `t.0` (later use gives E0382) while `let (_, k) = t` does not. Clippy lint names `single_match`, `manual_let_else` (pedantic per clippy source), `match_like_matches_macro`, `wildcard_enum_match_arm` (restriction per clippy source) accepted.
