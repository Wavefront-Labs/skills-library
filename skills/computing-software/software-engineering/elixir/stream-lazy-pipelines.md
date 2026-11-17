---
id: computing-software.software-engineering.elixir.stream-lazy-pipelines
name: stream-lazy-pipelines
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, stream, lazy, stream-resource, stream-unfold, file-stream, cycle, stream-lazy]
level: advanced
status: docs-checked
description: "Build lazy pipelines with Stream, generate sequences with unfold/iterate/resource and process big files with File.stream!, forcing evaluation with Enum."
sources: ["https://hexdocs.pm/elixir/Stream.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream and lazy evaluation

**Goal:** process large or infinite sequences without materialising intermediate lists, following the `Stream` docs.

```elixir
stream =
  1..3
  |> Stream.map(&IO.inspect(&1))
  |> Stream.map(&(&1 * 2))
  |> Stream.map(&IO.inspect(&1))

Enum.to_list(stream)             # nothing ran before this call; each element flows through once

Stream.iterate(1, &(&1 * 2)) |> Enum.take(5)      #=> [1, 2, 4, 8, 16]
Stream.unfold(0, fn n -> {n, n + 1} end) |> Enum.take(10)   # infinite unless next_fun returns nil

File.stream!("/path/to/file")
|> Stream.map(&String.replace(&1, "#", "%"))
|> Stream.into(File.stream!("/path/to/other/file"))
|> Stream.run()                  # run for side effects only, result ignored

Stream.resource(
  fn -> File.open!("sample") end,                  # start
  fn file ->                                       # next: {[elements], acc} or {:halt, acc}
    case IO.read(file, :line) do
      data when is_binary(data) -> {[data], file}
      _ -> {:halt, file}
    end
  end,
  fn file -> File.close(file) end                  # after
)
```

## Rules
- `Stream` functions are lazy and `Enum` functions are eager. A stream is a recipe of computations executed later, usually when consumed by an `Enum` function (or `Stream.run/1`).
- `Enum` chains create an intermediate list per step; a stream pipeline enumerates the source once. That makes streams useful for large or infinite collections.
- `Stream` functions work in linear time, like `Enum`.
- Functions that return streams: `IO.stream/2` (input lines), `URI.query_decoder/1`, `Stream.cycle/1`, `Stream.unfold/2`, `Stream.resource/3` (acquire, emit, release a resource), `Stream.iterate/2`.
- `Stream.run/1` enumerates the stream without caring about the result.
- Do not check whether a value is a `Stream` struct (see the `Stream` docs); rely on the `Enumerable` protocol.

## Self-check
Rewrite an `Enum.map |> Enum.filter` pipeline with `Stream.map |> Stream.filter |> Enum.to_list` and compare the order in which side effects print.

## Checked
Date: 2026-11-02. Confirmed against the Stream module docs (lazy vs eager, recipe, linear time, creation functions, iterate/unfold/resource/run examples, do not check for Stream structs). Removed: small-collection speed claim, Stream.chunk_every batch example, to_list infinite warning, Enum vs Stream timing self-check.
Method: documentation only; no commands were run.
