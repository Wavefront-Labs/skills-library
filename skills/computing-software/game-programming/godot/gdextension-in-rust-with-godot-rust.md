---
id: computing-software.game-programming.godot.gdextension-in-rust-with-godot-rust
name: gdextension-in-rust-with-godot-rust
category: computing-software
field: game-programming
product: godot
tags: [godot, gdextension, godot-rust, gdext-crate, native-extension, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot 4 GDExtensions in Rust with the gdext crate: project setup, .gdextension file, GodotClass derive, exported properties, signals, hot reload and export paths."
sources: ["https://godot-rust.github.io/book/", "https://docs.rs/godot/latest/godot/", "https://github.com/godot-rust/book/blob/master/src/intro/hello-world.md", "https://github.com/godot-rust/book/blob/master/src/register/functions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDExtension in Rust with godot-rust

**Goal:** performance-critical or library-backed systems written in Rust, usable from GDScript as
normal nodes.

## Setup
```toml
# Cargo.toml (crate in e.g. rust/)
[lib]
crate-type = ["cdylib"]
```
Add the dependency with `cargo add godot`; pick a godot-rust release that matches your Godot version
(see the book's versioning page).
```ini
; res://rust.gdextension
[configuration]
entry_symbol = "gdext_rust_init"
compatibility_minimum = 4.1
reloadable = true
[libraries]
linux.debug.x86_64 = "res://../rust/target/debug/librust.so"
windows.debug.x86_64 = "res://../rust/target/debug/rust.dll"
macos.debug = "res://../rust/target/debug/librust.dylib"
windows.release.x86_64 = "res://../rust/target/release/rust.dll"
```
- `entry_symbol` must be `gdext_rust_init`; no other symbol works.
- `compatibility_minimum` is the lowest Godot version that may run the extension.
- Library paths are relative to the directory holding `project.godot`; at least your own OS in
  `debug` is needed.
- Export paths must be inside `res://`; `..` paths are not supported in exports.

## Code
```rust
use godot::prelude::*;
struct MyExt;
#[gdextension] unsafe impl ExtensionLibrary for MyExt {}

#[derive(GodotClass)]
#[class(base = Node2D)]
struct Spinner { #[export] speed: f64, base: Base<Node2D> }

#[godot_api]
impl INode2D for Spinner {
    fn init(base: Base<Node2D>) -> Self { Self { speed: 1.0, base } }
    fn process(&mut self, delta: f64) {
        let s = self.speed;
        self.base_mut().rotate((s * delta) as f32);
    }
}
#[godot_api]
impl Spinner {
    #[signal] fn spun(turns: i64);
    #[func] fn reset(&mut self) { self.base_mut().set_rotation(0.0); }
}
```
`cargo build`, then add a node of type `Spinner` (not its base `Node2D`, or the Rust logic will not run).

## Rules
- `Gd<T>` smart pointers for engine objects; `bind()`/`bind_mut()` return guards that access the Rust
  data of your class. The library checks borrow rules at runtime and panics on a violation.
- Keep guard scope short, especially `bind_mut()`; inside the class, a `to_gd()` pointer is an
  independent handle, so `bind_mut()` on it during a method gives a double-borrow panic.
- A signal needs a `Base<T>` field on the class.

## Hot reload and export
- `reloadable = true` makes the editor reload the extension when its window regains focus; if Godot
  crashes, try removing it.
- Export: list a library per target in `.gdextension`; for a custom cargo `--target`, the output path
  includes the target triple and the paths must match.

## Gotchas
- Version mismatch between godot-rust and Godot gives load errors.
- If Godot fails to load a Rust class it may silently replace it with its base class.
- Missing library or `gdext_rust_init` errors: check `cargo build` ran, `cdylib`, and the paths.

## Verify
- [ ] Class instantiable from GDScript in an exported build on each target OS.
- [ ] Rebuilding while the editor is open reloads the extension.

## Checked

2026-11-01. Confirmed against the godot-rust book (hello-world and register/functions chapters): cdylib, entry
symbol, compatibility_minimum and reloadable meanings, library path rules, export path rule, custom target path,
GodotClass/Base/base_mut, `#[signal]` syntax, bind/bind_mut guards and double-borrow panic, silent base-class fallback.
Removed: pinned crate version, "Godot 4.2+" for reloadable, thread-usage advice, panic-recovery claim,
cross-compile and CI advice.

Method: documentation only; no commands were run.
