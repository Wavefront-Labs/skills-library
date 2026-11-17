---
id: computing-software.software-engineering.rust.cli-exit-codes-signals-and-machine-output
name: cli-exit-codes-signals-and-machine-output
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-cli-apps, rust-cli-output, exit-codes, sigpipe, ctrlc, json-output, stdout-stderr]
level: practitioner
status: docs-checked
description: "Make Rust CLIs script-friendly: stdout vs stderr, exit codes, broken pipes, Ctrl-C handling and NO_COLOR-aware colour."
sources:
  - https://rust-cli.github.io/book/in-depth/exit-code.html
  - https://rust-cli.github.io/book/in-depth/signals.html
  - https://no-color.org/
  - https://doc.rust-lang.org/std/process/fn.exit.html
  - https://doc.rust-lang.org/std/process/struct.ExitCode.html
  - https://doc.rust-lang.org/std/macro.println.html
  - https://doc.rust-lang.org/std/io/trait.IsTerminal.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exit codes, signals and machine-readable output

**Goal:** a CLI that composes in pipelines.

Rules: primary results go to **stdout** (`println!`), error and progress messages to **stderr** (`eprintln!`); exit `0` on success; many tools exit `1` on a common failure; Rust itself exits with `101` when the process panics. Keep any further codes for domain outcomes documented. The BSD ecosystem has a common exit-code vocabulary, available in Rust through the `exitcode` crate.

```rust
use std::process::ExitCode;
fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => { eprintln!("error: {e:#}"); ExitCode::from(3) }   // any u8; FAILURE is the canonical failure code
    }
}

use std::io::{IsTerminal, Write};
// NO_COLOR convention: disable colour when the variable is present and not an empty string
let no_color = std::env::var_os("NO_COLOR").is_some_and(|v| !v.is_empty());
let color = std::io::stdout().is_terminal() && !no_color;

// writing to a closed pipe (for example `| head`) must not panic: avoid println! there
let mut out = std::io::stdout().lock();
if let Err(e) = writeln!(out, "{line}") { if e.kind() != std::io::ErrorKind::BrokenPipe { return Err(e.into()) } }
```

`println!` panics if writing to stdout fails, so for output that may go to a closed pipe use `writeln!` on a locked stdout and handle the error. Locking stdout once also avoids the per-call lock in hot loops.

Ctrl-C: the `ctrlc` crate reacts to Ctrl-C (SIGINT) in a cross-platform way. In a real program, set an `Arc<AtomicBool>` (or send on a channel) in the handler and check it in loops or when waiting for a thread, then clean up. For other Unix signals use `signal-hook` (its `tokio-support` feature gives a `futures::Stream`). Windows has no signals; it has console handlers. If the user presses Ctrl-C again while you are shutting down, the typical behaviour is to quit immediately. If the app does not need graceful shutdown, the default handling is fine.

## Gotchas
- Never print colour codes or progress to stdout when it is piped; `IsTerminal::is_terminal` (Rust 1.70+) tells you whether a handle is a tty and returns false if detection fails.
- `std::process::exit()` runs no destructors on any stack; return an `ExitCode` or `Result` from `main` instead. On Unix usually only the low 8 bits of an exit code reach the parent.

## Verify
`NO_COLOR=1 tool | cat -v` shows no escapes; piping a large output into `head -1` does not print a panic message.

## Checked
Method: docs-checked 2026-11-09 against the Rust CLI book exit-code and signals chapters, no-color.org, and the std docs for process::exit, ExitCode, println! and IsTerminal. Dropped unconfirmed claims: clap exit code 2, grep exit codes, the SIGPIPE-ignored explanation, tokio signal usage, exit code 130, indicatif and the --json and ISO 8601 advice.
