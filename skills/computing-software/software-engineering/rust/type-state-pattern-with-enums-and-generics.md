---
id: computing-software.software-engineering.rust.type-state-pattern-with-enums-and-generics
name: type-state-pattern-with-enums-and-generics
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-types-data, rust-typestate, typestate, state-machine, phantomdata]
level: advanced
status: docs-checked
description: "Encode states in Rust types so invalid transitions fail to compile, using separate types or generics with PhantomData and consuming self."
sources:
  - https://docs.rust-embedded.org/book/static-guarantees/typestate-programming.html
  - https://doc.rust-lang.org/std/marker/struct.PhantomData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Type-state pattern

**Goal:** make illegal sequences (use before configuration) compile errors.

Typestates encode information about an object's current state in its type. The Embedded Rust Book's example uses two types: `FooBuilder` (configuration in process) and `Foo` (configured, ready); there is no direct way to create a `Foo`, and `into_foo(self)` consumes the builder, so it cannot be reused without creating a new one. States are types and state transitions are methods that exchange one type for another.

With generics, one struct is parameterised by a marker type; `PhantomData<S>` is a zero-sized type used to mark things that "act like" they own an `S`, and is the standard answer for unused type parameters (`size_of::<PhantomData<T>>() == 0`):

```rust
use std::marker::PhantomData;
struct Closed; struct Open;

struct Door<S> { name: String, _s: PhantomData<S> }
impl Door<Closed> {
    fn new(name: &str) -> Self { Door { name: name.into(), _s: PhantomData } }
    fn open(self) -> Door<Open> { Door { name: self.name, _s: PhantomData } } // consumes self
}
impl Door<Open> {
    fn walk_through(&self) { println!("through {}", self.name); }
    fn close(self) -> Door<Closed> { Door { name: self.name, _s: PhantomData } }
}
// Door::new("a").walk_through();   // error: no such method for Door<Closed>
```

Transitions take `self` by value so the old state cannot be used afterwards.

## Checked
2026-11-03. Confirmed against the Embedded Rust Book "Typestate Programming" (definition, builder example, consuming transition, states as types) and the `PhantomData` page (zero-sized marker, unused type parameters, `size_of` is 0). The `Door` example is the skill's own illustration of those rules. Removed: the enum-vs-typestate guidance, sealed state traits, `embedded-hal` `Pin<Output>`, the `Result<_, (Door<Closed>, Error)>` pattern, code-size and `dyn` claims, `compile_fail` doctests (the cliffle.com source returned HTTP 406 and was not read, so it was dropped).
Method: documentation only; no commands were run.
