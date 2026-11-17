---
id: computing-software.software-engineering.rust.drop-and-raii-guards
name: drop-and-raii-guards
category: computing-software
field: software-engineering
product: rust
tags: [rust, drop-trait, raii, guards, scope-guard, mutexguard, destructors, drop-order]
level: practitioner
status: verified
description: "Implement Drop for cleanup and RAII guards in Rust: drop order, scope guards, explicit drop, mem::forget, panics in drop, and why async cleanup cannot live in Drop."
sources: ["https://doc.rust-lang.org/std/ops/trait.Drop.html", "https://doc.rust-lang.org/reference/destructors.html", "https://doc.rust-lang.org/std/mem/fn.forget.html", "https://doc.rust-lang.org/nomicon/leaking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drop and RAII guards

**Goal:** tie cleanup (unlock, close, restore, rollback) to scope so it runs on every exit path,
including `?` and panics.

## Implementing Drop
```rust
struct TempDir { path: PathBuf }
impl Drop for TempDir {
    fn drop(&mut self) {
        if let Err(e) = std::fs::remove_dir_all(&self.path) {
            eprintln!("tempdir cleanup failed: {e}");   // cannot return errors from drop
        }
    }
}
```
- `drop` cannot fail or return a value. If cleanup can fail meaningfully, offer an explicit
  `close(self) -> Result<()>` and let Drop be the best-effort fallback (the `File`/`BufWriter` pattern:
  `BufWriter` flushes in drop but ignores errors, so call `flush()` yourself).
- You cannot call `x.drop()` directly; use `drop(x)` (std::mem::drop) to end a value early, for
  example to release a MutexGuard before an expensive call.

## Drop order
- Locals drop in **reverse declaration order**.
- Struct fields drop in **declaration order**, after the struct's own `Drop::drop`.
- Temporaries in an expression statement drop at the end of the statement; in `match x.lock().unwrap().get()`
  the guard temporary lives until the end of the match (a classic deadlock source). Since edition 2024,
  temporaries in `if let` scrutinees drop before the `else` block, and tail-expression temporaries drop
  before locals.
- `let _ = guard();` drops immediately; `let _g = guard();` keeps it to scope end. This bites with
  locks and tracing spans.

## Guard pattern
```rust
struct Restore<'a> { cfg: &'a mut Config, old: Level }
impl Drop for Restore<'_> { fn drop(&mut self) { self.cfg.level = self.old; } }
fn with_debug(cfg: &mut Config) -> Restore<'_> {
    let old = std::mem::replace(&mut cfg.level, Level::Debug);
    Restore { cfg, old }
}
```
The `scopeguard` crate provides `defer! { ... }` and `guard(value, |v| ...)` for ad-hoc cases;
`ScopeGuard::into_inner` cancels the cleanup (commit pattern). An sqlx `Transaction` rolls back on drop
unless committed (sqlx docs: "rollback is called on drop if the transaction is still in-progress").

## Leaks and forget
- `std::mem::forget(x)` skips Drop and is safe: Rust does not guarantee destructors run (Rc cycles
  also leak). Unsafe code must never rely on Drop running for soundness (the "leakpocalypse" rule).
- `ManuallyDrop<T>` suppresses automatic drop for a field you drop yourself (FFI, unions).
- `Box::leak` for intentional `'static` data.

## Panics and Drop
Drop runs during unwinding. A panic inside `drop` while already unwinding aborts the process. Keep
drop simple and non-panicking; check `std::thread::panicking()` to skip work like poisoning reports.
With `panic = "abort"` no destructors run on panic.

## Async
Drop is synchronous: you cannot `.await` in it. For async cleanup provide `async fn close(self)`,
spawn a cleanup task from drop (needs a runtime handle, best effort), or use a structured scope that
awaits cleanup.

## Verify
- [ ] Cleanup runs on early return, `?` and panic (test each with a counter).
- [ ] No `let _ = lock()` where a held guard was intended (clippy `let_underscore_lock`).
- [ ] Fallible cleanup has an explicit method whose result is checked.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran: reverse local drop order and field order after the struct's own Drop (`drop Pair`, `f.a`, `f.b`, `second`, `first`); `let _ = guard()` released immediately while `let _g` lived to `drop(_g)`; the `Restore`/`with_debug` guard restored `Info` after the scope; `early()` with `?` still ran Drop; `mem::forget` printed nothing; a `match m.lock().unwrap().first()` kept the guard alive inside the match (`try_lock` failed); `thread::panicking()` was true inside Drop during unwinding; `scopeguard::guard` + `ScopeGuard::into_inner` cancelled the cleanup and `defer!` ran at scope end.
- A panic inside `drop` while already unwinding aborted the process (exit code 127 on Windows here, with a stack backtrace); with `-C panic=abort` the destructor did not run.
- Edition 2024 temporaries: a function returning `D("temp").v()` with a local `D("local")` printed `drop local, drop temp` on edition 2021 and `drop temp, drop local` on 2024. An `if let` scrutinee guard in the `else` branch was already released (`try_lock` ok) on 2024.
- The clippy lint `let_underscore_lock` exists (accepted by clippy-driver; unknown names warn).
- sqlx `Transaction` docs (docs.rs, fetched): "If neither are called before the transaction goes out-of-scope, rollback is called." The earlier claim that diesel does the same was removed (not checked).
