---
id: computing-software.software-engineering.rust.async-fn-in-traits-and-send-bounds
name: async-fn-in-traits-and-send-bounds
category: computing-software
field: software-engineering
product: rust
tags: [rust, async-fn-in-trait, async-trait, send-bounds, rpitit, trait-variant, dyn-trait, async]
level: advanced
status: verified
description: "Write async functions in Rust traits (stable since 1.75): Send bounds via trait_variant or RPITIT, dyn compatibility limits and when the async-trait crate is still needed."
sources: ["https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits.html", "https://docs.rs/trait-variant/latest/trait_variant/", "https://docs.rs/async-trait/latest/async_trait/", "https://rust-lang.github.io/async-book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async functions in traits and Send bounds

**Goal:** define async interfaces (repositories, clients, handlers) that work with tokio's
multi-threaded spawn and, where needed, with trait objects.

## Native async fn in traits (Rust 1.75+)
```rust
pub trait Store {
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>, Error>;
}
impl Store for PgStore {
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>, Error> { .. }
}
```
Desugars to `fn get(..) -> impl Future<Output = ..>` (return-position impl Trait in traits,
RPITIT). Zero allocation, static dispatch.

## The Send problem
Callers that `tokio::spawn` need the returned future to be `Send`, but a plain `async fn` in a
trait makes no promise, so generic code fails:
```rust
fn spawn_get<S: Store + Send + Sync + 'static>(s: Arc<S>) {
    tokio::spawn(async move { s.get("k").await });   // error: future cannot be sent between threads
}
```
The compiler lints public traits (`async_fn_in_trait` warning) for this reason. Fixes:

1. **Declare the Send bound in the trait** with explicit RPITIT:
```rust
pub trait Store: Send + Sync {
    fn get(&self, key: &str) -> impl Future<Output = Result<Option<Vec<u8>>, Error>> + Send;
}
// implementors may still write `async fn get(..)` as long as the body is Send
```
2. **trait-variant** generates a Send variant from one definition:
```rust
#[trait_variant::make(Store: Send)]
pub trait LocalStore {
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>, Error>;
}
```
Users implement `Store` (Send) or `LocalStore` (single-threaded runtimes).
3. Return-type notation (`S: Store<get(..): Send>`) would let callers demand Send per method, but it is
still experimental: on stable 1.99.1 it fails with E0658 (tracking issue rust-lang/rust#109417). Use fixes 1 or 2.

## dyn compatibility
Traits with `async fn` (or RPITIT) are **not dyn compatible**: no `Box<dyn Store>`. Options:
- Generics everywhere (`struct Service<S: Store>`) - fastest, but infects signatures.
- `async-trait` crate: `#[async_trait] trait Store { async fn get(..) }` boxes each future as
  `Pin<Box<dyn Future + Send>>` and is dyn compatible. One allocation per call, usually negligible
  next to I/O. Use `#[async_trait(?Send)]` for non-Send.
- Hand-written boxing: `fn get<'a>(&'a self, k: &'a str) -> Pin<Box<dyn Future<Output = ..> + Send + 'a>>`.
- `dynosaur` crate generates a dyn-compatible wrapper for native async traits: `#[dynosaur::dynosaur(DynNext = dyn(box) Next)]` on the trait, then `DynNext::new_box(value)` (0.3.1).
Rule: application internals with a few implementations - native + generics; plugin-style or
heterogeneous collections of implementations - async-trait.

## Lifetimes
Native async methods capture all input lifetimes in the returned future automatically (the future
borrows `&self` and `key`). If you need a `'static` future (to spawn it), clone what you need into
an owned value before the async block, or take `self: Arc<Self>`.

## Verify
- [ ] Spawning a call through a generic `S: Store` compiles on the multi-threaded runtime.
- [ ] No `async_fn_in_trait` warnings on public traits (Send intention made explicit).
- [ ] Trait object usage (if needed) compiles with async-trait or a boxed signature.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, trait-variant 0.1.3, async-trait 0.1.92, dynosaur 0.3.1.
- Ran: explicit RPITIT `-> impl Future<...> + Send` with `tokio::spawn` through a generic `S: Store`; `#[trait_variant::make(Store2: Send)]`; `#[async_trait]` with `Box<dyn AStore>`; dynosaur with `DynNext::new_box`.
- The failing cases compile-fail as described: plain `async fn` in a trait + `tokio::spawn` gives "future cannot be sent between threads safely" (the awaited `impl Future` is not Send); `Box<dyn Store>` gives E0038 "method `get` is `async`"; `S: Store<get(..): Send>` gives E0658.
- The `async_fn_in_trait` warning fires on a `pub trait` in a lib crate (`rustc --crate-type lib`) with the text "use of `async fn` in public traits is discouraged as auto trait bounds cannot be specified".
- Async fn / RPITIT in traits stable in 1.75: blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits (fetched; it mentions trait-variant).
