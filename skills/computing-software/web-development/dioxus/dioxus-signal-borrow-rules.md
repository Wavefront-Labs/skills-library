---
id: computing-software.web-development.dioxus.dioxus-signal-borrow-rules
name: dioxus-signal-borrow-rules
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, signal, read, write, read-unchecked, await, clippy, generational-box, dispose]
level: practitioner
status: docs-checked
description: "Avoid Dioxus signal runtime borrow panics: do not hold read or write guards across await, clone or scope the guard, use read_unchecked, and know signals are disposed on unmount."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/signals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus signal borrow rules and lifetime

Goal: read and write the same signal safely, since signals are borrow-checked at runtime rather than compile time.

Combining a `.read()` and a `.write()` in one scope can cause a runtime borrow failure (panic). It is most often hit when a guard is held across an await point:

```rust
// Clicking quickly causes multiple `.write()` calls to be active
onclick: move |_| async move {
    let mut writer = state.write();
    sleep(Duration::from_millis(1000)).await;
    *writer = 10;
}
```

The page says this fails `cargo clippy` because the guard should not be held across an await (the `await_holding_refcell_ref` lint).

## Read then write in the same scope

The trivial case does not compile because `.write()` takes `&mut Signal` (error E0502). Stage operations so guards do not overlap:

```rust
let cur = state.read().clone(); // clone releases the read guard immediately
```

Or shorten the guard's scope:

```rust
let next = {
    let cur = state.read();
    println!("{cur}");
    cur.clone() + 1
};
*state.write() = next;
```

Or call `drop(cur1);` on the guard before calling `.write()`.

## read_unchecked

In very advanced cases you can copy the signal or use `read_unchecked` to relax the rules, for example `match result.read_unchecked().as_ref() { Ok(resp) => ..., Err(err) => ... }`. Rust 2024 fixes the `.read()`-in-`match` issue, so `read_unchecked` is not needed there.

## Disposal

`use_signal` calls `Signal::new()` and registers `signal.dispose()` on the component's `on_drop`. Reading a signal after its component unmounted causes a runtime panic (in debug mode you get a log warning that it is read after disposal). Calling `Signal::new()` directly, for example `users.write().push(Signal::new("bob".to_string()))`, keeps the data until the owning component unmounts or you call `.dispose()`, which can mean unbounded memory usage. The page advises preferring built-in methods and reactive collections when mapping or creating signals on the fly.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Dioxus 0.7 "Reactive Signals" docsite page (Signals are Borrowed at Runtime, Signals are Disposed). Nothing removed.
