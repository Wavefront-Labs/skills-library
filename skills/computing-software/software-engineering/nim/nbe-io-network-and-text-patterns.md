---
id: computing-software.software-engineering.nim.nbe-io-network-and-text-patterns
name: nbe-io-network-and-text-patterns
category: computing-software
field: software-engineering
product: nim
tags: [nbe-io-network-and-text-patterns, learning-resources-nim-by-example, nim-by-example, file-io, json, httpclient, parseopt, osproc, regex, examples, io, nim]
level: practitioner
status: draft
description: "Practise the I/O-centred examples: reading files, parsing args, JSON, HTTP requests, running processes and regex."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim by Example: file I/O, parsing, JSON, HTTP and processes

Goal: build small real-world tools.

- Examples to build: word-count (readFile + split + CountTable), CSV summariser (parsecsv), JSON pretty-printer (parseJson + pretty), file watcher via `getLastModificationTime`, HTTP fetcher (httpclient with `-d:ssl`), CLI with parseopt, directory walker (walkDirRec), subprocess wrapper (execCmdEx), simple TCP echo (net).
- Structure each as `proc main()` with `when isMainModule: main()`.
- Handle errors explicitly: `try` around IO, exit with `quit(1)` and message on stderr.
- Package the best one with nimble (`bin = @["tool"]`) and install via `nimble install`.
- Pair each with a small test using temp dirs from `getTempDir()`.

Gotchas:
- Network examples need `-d:ssl` and OpenSSL for HTTPS.
- Windows path separators: use `/` and `joinPath`.

Verify: the tool runs on sample input and its test passes.
