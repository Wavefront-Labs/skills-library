---
id: computing-software.software-engineering.rust.string-vs-str-and-slices
name: string-vs-str-and-slices
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-strings, string-slices, str, utf-8, osstr, pathbuf, asref, slices, rust-collections-strings]
level: practitioner
status: verified
description: "Choose between String, &str, and other string types in Rust APIs, slice UTF-8 safely, iterate chars vs bytes, and handle OsStr/Path and Box<str>."
sources: ["https://doc.rust-lang.org/book/ch08-02-strings.html", "https://doc.rust-lang.org/std/string/struct.String.html", "https://doc.rust-lang.org/std/primitive.str.html", "https://doc.rust-lang.org/std/ffi/struct.OsStr.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# String vs &str and slices

**Goal:** APIs that accept strings cheaply, own them only when needed, and never panic on a UTF-8
boundary.

## The types
| Type | Owns? | Use |
|---|---|---|
| `&str` | borrow | function parameters, read-only views, literals (`&'static str`) |
| `String` | owned, growable | building text, storing in structs that outlive the input |
| `Box<str>` / `Arc<str>` | owned, immutable | many stored strings (no capacity field), cheap clones with Arc |
| `Cow<'a, str>` | either | return borrowed when unchanged, owned when modified |
| `&[u8]` / `Vec<u8>` | bytes | non-UTF-8 data, protocols |
| `OsStr` / `OsString` | platform strings | env vars, OS APIs |
| `Path` / `PathBuf` | paths | file system paths (wrap OsStr) |
| `CStr` / `CString` | NUL-terminated | FFI |

## API design
```rust
fn greet(name: &str) {}                       // accepts &String via deref coercion, and literals
fn set_name(&mut self, name: impl Into<String>) { self.name = name.into(); } // caller decides to move or copy
fn open(p: impl AsRef<Path>) {}               // accepts &str, String, PathBuf, &Path
```
Take `&str` when you only read; take `String` (or `impl Into<String>`) when you will store it, so
callers with an owned String can move it in without a copy. Return `String` (or `&str` tied to
`&self`).

## Slicing is by byte index
```rust
let s = "héllo";
&s[0..1];        // "h"
&s[0..2];        // PANIC: byte index 2 is not a char boundary ('é' is 2 bytes)
s.get(0..2);     // None instead of panic
s.chars().take(2).collect::<String>();   // "hé"
s.char_indices();                         // (byte_offset, char) to slice safely
```
- `len()` is bytes, not characters. `s.chars().count()` is Unicode scalar values, still not what a
  user sees as characters (graphemes); use the `unicode-segmentation` crate for that.
- `s.as_bytes()` for byte-level parsing of ASCII protocols; `str::from_utf8(bytes)?` to validate,
  `String::from_utf8_lossy` to replace invalid sequences.

## Building strings efficiently
```rust
let mut out = String::with_capacity(n * 8);
for x in items { use std::fmt::Write; write!(out, "{x},").unwrap(); }
let joined = parts.join(", ");
let s = format!("{a}-{b}");          // allocates; fine outside hot loops
```
`push_str` for &str, `push` for char. Avoid `s = s + &t` in loops (it works but reads poorly);
`+` consumes the left String and borrows the right `&str`.

## OsStr and paths
`std::env::args()` panics on non-UTF-8 arguments; `args_os()` does not. `path.to_str()` returns
`Option`; `path.display()` for printing; `to_string_lossy()` when lossy is acceptable. Never round-trip
paths through String in tools that must handle arbitrary filenames.

## Gotchas
- Comparing `String` to `&str` works (`s == "x"`), but `match s.as_str() { "a" => .. }` is needed
  to match literals.
- `to_string()` vs `to_owned()` vs `String::from` are equivalent for &str; prefer one style.
- Holding `&str` slices of a `String` borrows it; you cannot mutate the String while they live.

## Verify
- [ ] Non-ASCII test input (emoji, combining marks) does not panic any slicing code.
- [ ] Public functions take `&str`/`impl AsRef<Path>` unless they store the value.
- [ ] Clippy clean (`needless_pass_by_value`, `manual_str_repeat`, `inefficient_to_string`).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran: `&s[0..1]` on "héllo" gives "h"; `&s[0..2]` panics ("end byte index 2 is not a char boundary; it is inside 'é' (bytes 1..3 of string)"); `get(0..2)` is `None`, `get(0..3)` is `Some("hé")`; `char_indices` offsets 0,1,3,4,5; `len()` 6 vs `chars().count()` 5; "e" + U+0301 has 3 bytes and 2 chars; `impl Into<String>` accepted `&str` and `String`; `impl AsRef<Path>` accepted `&str`, `String`, `PathBuf`; `write!` into a String; `join`; `String + &String`; a `Cow` normaliser returned borrowed/owned correctly; `match st.as_str()`; `from_utf8_lossy` gave a replacement character; `Box<str>` is smaller than `String`.
- std docs (doc.rust-lang.org/std/env/fn.args.html, fetched) have a "Panics" section for non-Unicode arguments. `unicode-segmentation` exists on crates.io. Clippy lint names `needless_pass_by_value`, `manual_str_repeat`, `inefficient_to_string` accepted by clippy-driver.
