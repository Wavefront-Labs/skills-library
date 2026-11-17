---
id: computing-software.software-engineering.rust.tracing-spans-subscribers-and-structured-logs
name: tracing-spans-subscribers-and-structured-logs
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-web-services, rust-tracing, tracing, tracing-subscriber, spans, instrument, structured-logging]
level: practitioner
status: docs-checked
description: "Instrument Rust services with tracing: events, spans, #[instrument], tracing-subscriber layers, EnvFilter, JSON output and async-safe spans."
sources:
  - https://docs.rs/tracing/latest/tracing/
  - https://docs.rs/tracing-subscriber/latest/tracing_subscriber/
  - https://tokio.rs/tokio/topics/tracing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tracing spans, subscribers and structured logs

**Goal:** logs with context (request ID, user) that follow async tasks.

```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```
```rust
use tracing::{info, instrument, Instrument};
use tracing_subscriber::{fmt, EnvFilter, prelude::*};

fn init() {
    tracing_subscriber::registry()
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| "info".into()))
        .with(fmt::layer().json())                    // JSON output needs the json feature
        .init();
}

#[instrument(skip(db), fields(user_id = %user.id))]
async fn charge(db: &Db, user: &User, cents: u64) -> Result<(), Error> {
    info!(cents, "charging");
    Ok(())
}

tokio::spawn(work().instrument(tracing::info_span!("job", id = 7)));   // span follows the future
```

- A `Span` has a start and end and is entered and exited; an `Event` is a point in time that may occur inside a span, comparable to a log record. Subscribers (via `tracing-subscriber` layers) record them.
- `#[tracing::instrument]` is the easiest way to emit spans for functions; `skip(...)` stops arguments being recorded in the span (use it for large or secret values), and `fields(...)` adds fields.
- In async code `Span::enter` can produce incorrect traces if the guard is held across an await point; attach the span to the future with `.instrument(span)` instead.
- `tracing-subscriber` composes `Layer`s on a `registry`; `Filter`s decide what each layer sees. Feature flags: `env-filter` enables `EnvFilter` (filtering similar to the `env_logger` crate), `json` enables JSON output for `fmt`, `fmt` and `ansi` are on by default.
- Events from the `log` crate are formatted better in the `fmt` subscriber via the default `tracing-log` optional dependency; the `log` and `log-always` features of `tracing` make spans and events emit `log` records.

## Gotchas
- Do not log secrets; skip them in `#[instrument]`.
- Libraries should generally not enable the `log-always` feature.

## Verify
Run the service, hit an endpoint and confirm JSON lines with span fields.

## Checked
Method: docs-checked 2026-11-09 against the tracing and tracing-subscriber crate pages and the Tokio tracing topic (instrument macro, skip and async-guard warning read). Dropped unconfirmed claims about err, release_max_level features, OpenTelemetry export, tracing-appender, tracing-error, tracing-test and the example filter directives.
