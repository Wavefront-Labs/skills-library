---
id: computing-software.software-engineering.rust.clap-derive-api-and-subcommands
name: clap-derive-api-and-subcommands
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-cli-apps, rust-clap, clap, derive, subcommands, argument-parsing]
level: practitioner
status: docs-checked
description: "Define a Rust CLI with clap derive: Parser, Subcommand, ValueEnum, env fallbacks, defaults, completions and testing with assert_cmd."
sources:
  - https://docs.rs/clap
  - https://rust-cli.github.io/book/tutorial/cli-args.html
  - https://docs.rs/assert_cmd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# clap derive API

**Goal:** a CLI with help, completions and validation from a struct.

```rust
use clap::{Parser, Subcommand, ValueEnum, Args};

#[derive(Parser)]
#[command(name = "tool", version, about = "Manage things")]
struct Cli {
    #[arg(long, global = true)]
    verbose: bool,                                 // global: accepted after subcommands too
    #[arg(long, env = "TOOL_CONFIG", value_name = "FILE")]   // env needs clap's `env` feature
    config: Option<std::path::PathBuf>,
    #[command(subcommand)]
    cmd: Cmd,
}
#[derive(Subcommand)]
enum Cmd {
    /// Start the server
    Serve(ServeArgs),
    /// Print things
    List { #[arg(long, value_enum, default_value_t = Format::Table)] format: Format },
}
#[derive(Args)]
struct ServeArgs {
    #[arg(long, default_value = "127.0.0.1:8080")] addr: String,
}
#[derive(Copy, Clone, ValueEnum)] enum Format { Table, Json }

fn main() {
    let cli = Cli::parse();
    match cli.cmd { /* ... */ }
}
```

Doc comments become help text (attributes take priority over doc comments). Field types map to arguments: `bool` is a flag, `Option<T>` an optional argument, plain `T` required unless it has a default, `Vec<T>` zero or more occurrences. `#[arg(value_parser = ...)]` selects a parser and `value_enum` parses straight into a `ValueEnum` enum, erroring on unsupported values. Completions come from the `clap_complete` crate and man pages from `clap_mangen`; `ValueHint` tells the shell how to complete an argument. Test the built binary end to end with `assert_cmd`: `Command::cargo_bin("tool")` then `.assert().success()`.

## Gotchas
- `Vec<T>` is an empty vec when the argument is absent, but `Option<Vec<T>>` is `None`; choose by whether absence matters.
- `global = true` args are accepted after subcommands; otherwise they must precede them.
- Follow the current clap docs for `ArgAction` and `value_parser`; older tutorials use removed v2/v3 APIs.

## Verify
`tool --help` renders; add a unit test calling `Cli::command().debug_assert()` (clap's documented check for definition mistakes) and run `cargo test`.

## Checked
Confirmed from the docs.rs clap derive reference (Parser/Args/Subcommand/ValueEnum, doc comment handling and priority, `env` needing the `env` feature, `value_parser`, `value_enum`, `default_value`/`default_value_t`, `global`, the type-to-action table incl. `Vec<T>` versus `Option<Vec<T>>`, `Command::debug_assert`), the clap crate page (`clap_complete`, `clap_mangen`, `ValueHint`) and the assert_cmd crate page (`Command::cargo_bin`, `.assert().success()`). Removed: `propagate_version`, the Count-based `-vvv` field, `value_parser!(u16).range`, SocketAddr parsing, the `clap_complete::generate` call, `predicates` usage, `Cli::try_parse_from`, the "exits with usage" note and the `tool completion` check. The rust-cli book page was fetched but not relied on beyond the basic derive pattern.

Method: docs-checked 2026-11-09 against docs.rs clap (crate and derive reference), docs.rs assert_cmd and the Rust CLI book args chapter.
