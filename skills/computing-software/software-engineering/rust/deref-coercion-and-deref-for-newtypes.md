---
id: computing-software.software-engineering.rust.deref-coercion-and-deref-for-newtypes
name: deref-coercion-and-deref-for-newtypes
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-smart-pointers, rust-deref-coercion, deref, deref-coercion, newtype]
level: practitioner
status: docs-checked
description: "Know how Deref coercion makes &String act as &str, the three coercion cases, and why Deref for inheritance-style wrappers is an anti-pattern."
sources:
  - https://doc.rust-lang.org/book/ch15-02-deref.html
  - https://rust-unofficial.github.io/patterns/anti_patterns/deref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deref coercion and Deref for newtypes

**Goal:** understand implicit `&` conversions and avoid abusing `Deref` for inheritance.

Deref coercion converts a reference to a type implementing `Deref` into a reference to another type, for example `&String` to `&str`. It is a convenience Rust performs on arguments to functions and methods, and it is applied as many times as needed to match the parameter's type; the count is resolved at compile time, so there is no runtime penalty.

The three cases (The Rust Book):
- `&T` to `&U` when `T: Deref<Target=U>`
- `&mut T` to `&mut U` when `T: DerefMut<Target=U>`
- `&mut T` to `&U` when `T: Deref<Target=U>`

Immutable references never coerce to mutable ones, because a mutable reference must be the only reference to its data.

```rust
use std::ops::Deref;
fn hello(name: &str) { println!("Hello, {name}!"); }

struct MyBox<T>(T);
impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target { &self.0 }
}

let m = MyBox(String::from("Rust"));
hello(&m);        // &MyBox<String> -> &String -> &str
```

Without coercion the call would have to be written `hello(&(*m)[..])`.

## The anti-pattern
Rust Design Patterns calls "Deref polymorphism" a misuse: implementing `Deref` on a wrapper (`Bar` with `Target = Foo`) just to reuse the inner type's methods and emulate inheritance. Disadvantages it lists: it is a surprising idiom that is completely implicit, it introduces no subtyping, and traits implemented by `Foo` are not automatically implemented for `Bar`, so it interacts badly with bounds checking and generic programming. The saving is a little boilerplate; explicit delegation (`impl Bar { fn m(&self) { self.f.m() } }`) is the alternative.

## Checked
2026-11-03. Confirmed against The Rust Book "Treating Smart Pointers Like Regular References with Deref" (coercion definition, three cases, compile-time resolution, `MyBox` example) and the Rust Design Patterns "Deref polymorphism" page. Removed: the `Box`/`Rc`/`Vec` transitive coercion list, the `Meters` example, the `AsRef` generic-bound gotcha, `.inner()` suggestion, claims about which std types should implement `Deref`, and the `cargo doc` advice.
Method: documentation only; no commands were run.
