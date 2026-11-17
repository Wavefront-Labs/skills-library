---
id: computing-software.software-engineering.elixir.file-path-io-streams
name: file-path-io-streams
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, file-read, file-write, path-join, file-stream, io-puts, io-gets, file-mkdir, file-rm, tmp-files, file-io, elixir-io-files]
level: intro
status: docs-checked
description: "Read and write files, build paths with Path, stream lines, create directories and handle errors with tagged tuples."
sources: ["https://hexdocs.pm/elixir/File.html", "https://hexdocs.pm/elixir/Path.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File, Path and IO operations

**Goal:** file handling with correct error treatment.

```elixir
{:ok, data} = File.read(Path.join(dir, "a.txt"))     # prefer tagged tuple in app code
File.read!(path) ; File.write!(path, iodata, [:append]) ; File.mkdir_p!(dir) ; File.rm_rf!(dir)
File.stream!(path, :line) |> Stream.map(&String.trim/1) |> Enum.to_list()
File.ls!(dir) ; File.exists?(path) ; File.stat!(path).size ; File.cp_r!(a, b) ; File.rename!(a, b)
Path.expand("~/x") ; Path.basename("/a/b.txt", ".txt") ; Path.extname(p) ; Path.wildcard("lib/**/*.ex") ; Path.split(p)
System.tmp_dir!() ; File.open!(path, [:write, :utf8], fn f -> IO.write(f, "x") end)
IO.puts("out") ; IO.puts(:stderr, "err") ; IO.gets("prompt> ") ; IO.read(:stdio, :eof)
```

## Rules
- Bang functions raise `File.Error`; non-bang return `{:error, reason}` such as `:enoent`.
- `File.stream!/2` returns a stream you consume with `Enum`/`Stream`; `File.read!/2` returns the whole content.
- `Path.safe_relative/2` returns a relative path protected from directory-traversal attacks; use it on user-supplied path segments.
- `File.rm_rf!` is destructive; guard the path you pass.

## Self-check
Write a file under `System.tmp_dir!()`, read it back, and check that a missing path gives `{:error, :enoent}` from `File.read/1`.

## Checked
2026-11-03: confirmed against the Elixir File, Path, IO and System docs (function names and arities, `write!/3` iodata content, `stream!`, `open!/3` with a function, `Path.safe_relative/2`, `System.tmp_dir!/0`, `IO.gets`, `IO.read(:stdio, :eof)`, `File.Error` for bang functions). Removed: the lazy/auto-close claim for `stream!`, the atomic temp-and-rename recipe and `:eacces`/`:eexist` examples (not on the File pages read).
Method: documentation only; no commands were run.
