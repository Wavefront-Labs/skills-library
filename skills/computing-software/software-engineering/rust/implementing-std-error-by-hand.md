---
id: computing-software.software-engineering.rust.implementing-std-error-by-hand
name: implementing-std-error-by-hand
category: computing-software
field: software-engineering
product: rust
tags: [rust, std-error-trait, error-source, display, error-chain, custom-error-types, error-handling, no-dependencies]
level: practitioner
status: verified
description: "Implement std::error::Error manually in Rust: Display messages, source() chains, From impls for ?, Send + Sync + 'static bounds, and printing the full cause chain."
sources: ["https://doc.rust-lang.org/std/error/trait.Error.html", "https://doc.rust-lang.org/std/fmt/trait.Display.html", "https://rust-lang.github.io/api-guidelines/interoperability.html#error-types-are-meaningful-and-well-behaved-c-good-err"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing std::error::Error by hand

**Goal:** a well-behaved error type without dependencies (or to understand what `thiserror`
generates): good messages, an inspectable cause chain, and `?` conversions.

## Full example
```rust
use std::{error::Error, fmt, io, num::ParseIntError};

#[derive(Debug)]
pub enum ConfigError {
    Io { path: String, source: io::Error },
    Parse { line: usize, source: ParseIntError },
    Missing(&'static str),
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io { path, .. } => write!(f, "cannot read config file {path}"),
            Self::Parse { line, .. } => write!(f, "invalid number on line {line}"),
            Self::Missing(key) => write!(f, "missing required key `{key}`"),
        }
    }
}

impl Error for ConfigError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io { source, .. } => Some(source),
            Self::Parse { source, .. } => Some(source),
            Self::Missing(_) => None,
        }
    }
}

// Context-carrying variants are built with map_err rather than a blanket From:
// let n: u32 = s.parse().map_err(|e| ConfigError::Parse { line, source: e })?;
```

## Rules for good errors
- **Display**: lowercase, no trailing punctuation, describes this layer only. Do **not** include the
  source's message in Display when you also return it from `source()`: reporters print the chain and
  you get duplicated text ("cannot read file: No such file: No such file").
- **source()**: return the underlying error so callers and reporters can walk the chain. `cause()`
  and `description()` are deprecated; do not implement them.
- **Debug**: derive it; `fn main() -> Result<(), E>` prints Debug, which is why apps convert to
  anyhow/eyre for nicer output.
- Make errors `Send + Sync + 'static` (avoid `Rc` or borrowed data inside) so they work with
  `Box<dyn Error + Send + Sync>`, anyhow, and across threads/tasks.
- Add context fields (path, line, id) rather than relying on generic `From` conversions, which lose
  where the error happened. Provide `From` only when the conversion needs no context.

## Printing the chain
```rust
fn report(e: &dyn Error) -> String {
    let mut s = e.to_string();
    let mut cur = e.source();
    while let Some(c) = cur { s.push_str(": "); s.push_str(&c.to_string()); cur = c.source(); }
    s
}
```
anyhow's `{:#}` and eyre reports do this for you.

## Downcasting
`err.downcast_ref::<io::Error>()` on `dyn Error + 'static` lets callers inspect causes; walk
`source()` to find a specific kind deep in the chain.

## When to stop hand-writing
Once there are more than a few variants, `thiserror` generates exactly this code
(`#[error("...")]`, `#[source]`, `#[from]`) with no runtime cost and no public API exposure.

## Verify
- [ ] Each Display message reads well alone and the chain has no duplicated text.
- [ ] `fn assert_err<T: Error + Send + Sync + 'static>() {}` compiles for your type.
- [ ] `source()` returns the wrapped error for every wrapping variant.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Compiled the full `ConfigError` example (Display, `source()`, `Error`), the `parse(...).map_err(|e| ConfigError::Parse { line, source: e })?` constructor, `fn assert_err<T: Error + Send + Sync + 'static>()`, and `report(&dyn Error)`: it printed `invalid number on line 3: invalid digit found in string` and `cannot read config file a.toml: No such file`. `Box<dyn Error + Send + Sync>` plus `source().downcast_ref::<io::Error>()` found `NotFound`; `Missing` returned `None` from `source()`.
- The duplicated-chain warning was reproduced in a thiserror run (see error-handling-with-result): putting the source text in Display repeats it in anyhow's chain.
