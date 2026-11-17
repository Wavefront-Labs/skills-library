---
id: computing-software.software-engineering.rust.returning-errors-from-main-and-exitcode
name: returning-errors-from-main-and-exitcode
category: computing-software
field: software-engineering
product: rust
tags: [rust, exitcode, main-result, termination, cli, process-exit, error-reporting, anyhow, rust-cli-apps]
level: practitioner
status: verified
description: "Return errors from Rust main cleanly: Result<(), E> and Debug output, ExitCode for custom statuses, the Termination trait, and why process::exit skips destructors."
sources: ["https://doc.rust-lang.org/std/process/struct.ExitCode.html", "https://doc.rust-lang.org/std/process/trait.Termination.html", "https://doc.rust-lang.org/std/process/fn.exit.html", "https://rust-cli.github.io/book/in-depth/exit-code.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Returning errors from main and ExitCode

**Goal:** CLI and service binaries that print a human-readable error, exit with a meaningful
status code, and still run destructors (flush files, remove temp dirs).

## main returning Result
```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cfg = load_config()?;
    run(cfg)?;
    Ok(())
}
```
On `Err(e)` the runtime prints `Error: {e:?}` (the **Debug** form) to stderr and exits with code 1.
Debug of a custom enum is ugly; with anyhow, `anyhow::Error`'s Debug prints the message, the
`Caused by:` chain and a backtrace if enabled, which is why `fn main() -> anyhow::Result<()>` reads
well.

## ExitCode for specific statuses
```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(Error::Usage(msg)) => { eprintln!("usage: {msg}"); ExitCode::from(2) }
        Err(e) => {
            eprintln!("error: {e}");
            let mut src = std::error::Error::source(&e);
            while let Some(s) = src { eprintln!("  caused by: {s}"); src = s.source(); }
            ExitCode::FAILURE
        }
    }
}
```
- `ExitCode::from(u8)`; conventions: 0 success, 1 general failure, 2 usage error (clap uses 2),
  sysexits-style 64-78 for some tools, 130 for SIGINT.
- Values from `main` run all destructors in main's scope before exiting.

## Termination trait
`main` may return any `T: Termination`: `()`, `ExitCode`, `Result<T: Termination, E: Debug>`, `!`.
Implement it for your own type to centralise reporting:
```rust
struct App(Result<(), MyError>);
impl std::process::Termination for App {
    fn report(self) -> ExitCode { match self.0 { Ok(()) => ExitCode::SUCCESS, Err(e) => { eprintln!("{e}"); e.code() } } }
}
```

## process::exit pitfalls
`std::process::exit(code)` terminates immediately: **destructors on the current stack do not run**,
so `BufWriter` contents are lost and temp files remain. Return from main instead; if you must exit
deep in the stack, flush explicitly first. `std::process::abort` additionally skips everything and
produces SIGABRT.

## Panics
A panic in main prints the panic message and exits with code 101. Do not rely on panics for user
errors. Set `RUST_BACKTRACE=1` for traces. Install a custom hook (`std::panic::set_hook`, or
`human-panic` for end-user CLIs) to print a friendly message.

## Async main
`#[tokio::main] async fn main() -> anyhow::Result<()>` works the same; the runtime shuts down
(dropping tasks) when main returns.

## Verify
- [ ] `myapp --bad-flag; echo $?` prints 2; a runtime failure prints 1 and a readable message.
- [ ] Error output goes to stderr, data to stdout.
- [ ] No `process::exit` before buffered output is flushed.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Built one binary and checked exit codes: `ExitCode::SUCCESS` gave 0, `ExitCode::from(2)` gave 2, `ExitCode::FAILURE` gave 1, a custom `Termination::report` returning `ExitCode::from(7)` gave 7, `main` returning `Err(E)` printed `Error: E { code: 4 }` (Debug form) with exit code 1, and a panic in main exited with 101.
- Destructors: values returned from `main` ran `Drop` (`D dropped`); `std::process::exit(3)` printed no `Drop` output, and a `BufWriter` holding `data` followed by `process::exit(0)` left a 0-byte file.
- `Termination`: `fn main() -> !` compiles; `Result<(), String>::report()` equals `ExitCode::FAILURE` and prints `Error: "x"`. Calling `.report()` by hand needs `use std::process::Termination`.
- The skill's claims about clap (exit 2), sysexits 64-78 and 130 for SIGINT are conventions, not checked against those projects here.
