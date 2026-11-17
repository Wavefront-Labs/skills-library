---
id: computing-software.software-engineering.rust.builder-pattern-and-constructors
name: builder-pattern-and-constructors
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-types-data, rust-builder-pattern, builder-pattern, new, default, constructors]
level: practitioner
status: docs-checked
description: "Design Rust builders per the API Guidelines (C-BUILDER): when a builder fits, consuming vs non-consuming builders, required fields and terminal methods."
sources:
  - https://rust-lang.github.io/api-guidelines/type-safety.html
  - https://rust-unofficial.github.io/patterns/patterns/creational/builder.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Builder pattern and constructors

**Goal:** an ergonomic way to create types with many optional parameters.

Rust lacks overloading and default values for function parameters, and you can only have one method with a given name, so multiple constructors are less pleasant than in C++ or Java; the builder is the usual answer. The Design Patterns book gives the motivation: many constructors, or construction with side effects.

```rust
pub struct Foo { bar: String }
impl Foo { pub fn builder() -> FooBuilder { FooBuilder::new() } }   // helps users discover the builder

pub struct FooBuilder { bar: String }
impl FooBuilder {
    pub fn new() -> FooBuilder { FooBuilder { bar: String::from("X") } }  // minimally required fields
    pub fn name(mut self, bar: String) -> FooBuilder { self.bar = bar; self }
    pub fn build(self) -> Foo { Foo { bar: self.bar } }                   // terminal method
}
let foo = FooBuilder::new().name(String::from("Y")).build();
```

## C-BUILDER guidance
- Introduce a separate `TBuilder` type (pick a better name where possible, e.g. `Command` builds a child process). Its constructor takes only the data required to make a `T`.
- Configuration methods return the builder to allow chaining, including incremental setup of compound inputs such as slices.
- Provide one or more "terminal" methods that actually build the `T`. Builders suit cases where building has side effects (spawning a task, launching a process).
- **Non-consuming builders are preferred** by the guidelines when building does not need to consume the builder (as with `std::process::Command::spawn`, which takes `&self`); the methods then take and return `&mut` and one builder can be a template for many values.
- If terminal methods need ownership (they take `self`), the guidelines say all builder methods should take and return an owned `self`, so one-liners work; complex configuration then requires re-assigning the builder at each step.
- Adding fields to the target struct is backwards compatible if the builder is updated.
- Disadvantage: more complex than a plain struct literal or constructor function.

## Checked
2026-11-03. Confirmed against the Rust API Guidelines "Type safety" page (C-BUILDER) and Rust Design Patterns "Builder". Removed: `bon` and `derive_builder` claims, the `ClientBuilder` validation example, the `new()`/`Default` thresholds ("0 to 3 arguments"), `#[non_exhaustive]` and `#[derive(Default)]` advice, `impl Into<String>` advice, `build(&self)` remark and the `cargo doc` tip.
Method: documentation only; no commands were run.
