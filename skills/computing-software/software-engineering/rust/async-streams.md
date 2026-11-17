---
id: computing-software.software-engineering.rust.async-streams
name: async-streams
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-streams, futures-stream, tokio-stream, async-stream, streamext, buffer-unordered, async]
level: advanced
status: verified
description: "Produce and consume async streams in Rust: futures::Stream and StreamExt, tokio-stream wrappers, async-stream generators, buffer_unordered concurrency and backpressure."
sources: ["https://docs.rs/futures/latest/futures/stream/trait.StreamExt.html", "https://docs.rs/tokio-stream/latest/tokio_stream/", "https://docs.rs/async-stream/latest/async_stream/", "https://tokio.rs/tokio/tutorial/streams"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async streams

**Goal:** process sequences of async values (paginated APIs, message consumers, file lines) with
bounded concurrency and backpressure, the async analogue of Iterator.

## The trait
`futures::Stream` (`futures-core`): `poll_next(self: Pin<&mut Self>, cx) -> Poll<Option<Item>>`.
Not yet in std as a stable trait; the ecosystem standard is `futures::Stream`, and tokio re-exports
it through `tokio-stream`. Combinators come from an extension trait:
`use futures::StreamExt;` (or `tokio_stream::StreamExt` - do not import both, method names clash:
calling `.map` or `.collect` then fails with E0034 "multiple applicable items in scope"; import one in
the module, or alias it `as _` and call the other with full paths).
tokio-stream gates its wrappers and combinators behind features (`time` is default; `sync` for
`BroadcastStream`, `net` for `TcpListenerStream`, `io-util` for `LinesStream`; `full` enables all).

## Consuming
```rust
use futures::{StreamExt, TryStreamExt};
use std::pin::pin;
let mut s = pin!(make_stream());          // many streams are !Unpin; pin before .next()
while let Some(item) = s.next().await { handle(item?); }

// concurrency: up to 8 requests in flight, results in completion order
let results: Vec<_> = futures::stream::iter(urls)
    .map(|u| client.get(u).send())
    .buffer_unordered(8)                  // `buffered(8)` keeps input order
    .collect().await;

// fallible streams
let rows: Vec<Row> = stream.try_filter(|r| future::ready(r.active)).try_collect().await?;
```
Useful adaptors: `map`, `then` (async map), `filter_map`, `take`, `take_while`, `chunks(n)`,
`ready_chunks`, `fold`, `for_each_concurrent(limit, f)`, `throttle` (tokio-stream), `timeout`,
`merge`/`select` (combine streams), `fuse`.

## Producing
**async-stream** macro (easiest):
```rust
use async_stream::try_stream;
fn pages(client: Client) -> impl Stream<Item = Result<Page, Error>> {
    try_stream! {
        let mut cursor = None;
        loop {
            let page = client.list(cursor.take()).await?;
            cursor = page.next.clone();
            yield page;
            if cursor.is_none() { break; }
        }
    }
}
```
**unfold** without macros:
```rust
futures::stream::unfold(Some(start), |state| async move {
    let cur = state?;
    let page = fetch(cur).await.ok()?;
    let next = page.next.clone();
    Some((page, next))
})
```
**From a channel**: `tokio_stream::wrappers::ReceiverStream::new(rx)` (also `IntervalStream`,
`BroadcastStream`, `TcpListenerStream`, `LinesStream`). A spawned producer feeding a bounded channel
gives natural backpressure and lets producer and consumer run on different threads.

Returning streams: `impl Stream<Item = T>` for static dispatch, or
`Pin<Box<dyn Stream<Item = T> + Send>>` (`futures::stream::BoxStream<'a, T>`) for trait objects and
heterogeneous branches (`.boxed()`).

## Backpressure and cancellation
- Streams are lazy: nothing happens until polled. A consumer that stops polling stops the producer
  (except producers spawned as separate tasks; those block on the bounded channel).
- Dropping a stream cancels it; the same cancellation-safety concerns as `select!` apply to
  partially consumed items.
- `for_each_concurrent` / `buffer_unordered` bound in-flight work; never `collect` an unbounded
  stream into memory.

## Async iteration in the language
`async gen` blocks and `AsyncIterator` are nightly-only; use the crates above on stable.

## Verify
- [ ] Concurrency limit visible and tested (count in-flight futures).
- [ ] Memory flat on a long stream (no unbounded collect or buffer).
- [ ] Only one StreamExt trait imported per module.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, tokio-stream 0.1.19, async-stream 0.3.6.
- Ran: `try_stream!` pager (3 pages) consumed through `pin!` + `.next()`; `buffer_unordered(8)` over 20 tasks measured a peak of 8 in flight and out-of-order results, `buffered(8)` kept order; `try_filter`/`try_collect`; `unfold`; `ReceiverStream`; `chunks(2)` and `ready_chunks(2)`; `for_each_concurrent`; `futures::stream::select`; `.boxed()`; tokio-stream `throttle` (3 items at 50 ms took at least 100 ms), `merge` and `timeout`.
- `pin!` is needed: `tokio_stream` `Timeout` (a `!Unpin` stream) fails `.next()` with "`PhantomPinned` cannot be unpinned" until pinned. Importing both StreamExt traits gives E0034 (confirmed). `BroadcastStream`/`TcpListenerStream` missing without the features (compile error says gated behind `sync`/`net`).
- `async gen` blocks fail on stable with E0658 "gen blocks are experimental" and "yield syntax is experimental".
