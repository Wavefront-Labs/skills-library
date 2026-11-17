---
id: computing-software.web-development.dioxus.dioxus-streams-and-sse
name: dioxus-streams-and-sse
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, textstream, bytestream, streaming, filestream, jsonencoding, sse]
level: practitioner
status: docs-checked
description: "Stream text, bytes, typed JSON and files between a Dioxus server function and client with TextStream, ByteStream, Streaming<T, E> and FileStream."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/streams.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream data with TextStream, ByteStream and FileStream

Goal: send chunked data (LLM output, downloads, server-sent events) over a server function.

Streams are unidirectional. Unlike websockets, browsers usually cannot have a streaming input and output at once, so use streams for text/byte responses or file sending.

## Text

`TextStream` can be the input or output of a server function. `TextStream::spawn` gives you an `UnboundedSender`:

```rust
#[get("/api/test_stream?start")]
async fn text_stream(start: Option<i32>) -> Result<TextStream> {
    let mut count = start.unwrap_or(0);
    Ok(TextStream::spawn(move |tx| async move {
        while tx.unbounded_send(format!("Hello, world! {}", count)).is_ok() {
            count += 1;
            tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
        }
    }))
}
```

You can also build one from any existing type implementing `Stream` (e.g. the receiver from `futures::channel::mpsc::unbounded()`) with `new()`.

## Bytes

`ByteStream` works like `TextStream` but with `Bytes`. Consume it with `.next()`; streams implement the standard `Stream` trait:

```rust
#[post("/api/upload_as_bytestream")]
async fn upload_as_bytestream(mut stream: ByteStream) -> Result<()> {
    while let Some(chunk) = stream.next().await { /* handle chunk */ }
    Ok(())
}
```

## Streaming<T, E>

`TextStream` and `ByteStream` are variations of the generic `Streaming<T, E>` (streams of `Vec<u8>` underneath; `TextStream` ensures valid utf-8). Pick an encoding implementing `Encoding`; built in: `JsonEncoding`, `CborEncoding`, `PostcardEncoding`, `MsgPackEncoding`.

```rust
#[get("/api/json_stream")]
async fn json_stream() -> Result<Streaming<Dog, JsonEncoding>> {
    Ok(Streaming::spawn(|tx| async move {
        for count in 0..10 {
            let dog = Dog { name: format!("Dog {}", count), age: (count % 10) as u8 };
            if tx.unbounded_send(dog).is_err() { break; }
            tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
        }
    }))
}
```

## FileStream

`FileStream` is not built on `Streaming<T, E>`; it uses platform-native optimizations to stream files without buffering them in memory. Download with `FileStream::from_path(path).await?`. For uploads, create it from `FileData` with `file.into()` and accept `FileStream` on the server. It sets extra headers such as `Content-Disposition` and `X-Content-Size`.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 streams page (read in full): unidirectional streams, TextStream spawn and new, ByteStream with next(), the generic Streaming<T, E>, the built-in encodings, FileStream from_path and from FileData, and the extra headers.

Method: documentation only; no commands were run.
