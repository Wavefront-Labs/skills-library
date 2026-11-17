---
id: computing-software.software-engineering.clojure.slurp-spit-reader-writer-with-open
name: slurp-spit-reader-writer-with-open
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, io, slurp, spit, clojure.java.io, reader, writer, with-open, file, resource, line-seq, copy, java-io-slurp-spit, clojure-io]
level: intro
status: docs-checked
description: "Read and write files with slurp/spit, clojure.java.io (file, reader, writer, resource, copy), with-open, line-seq and charset options; stream big files lazily and safely."
sources: ["https://clojure.github.io/clojure/clojure.java.io-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slurp, spit and clojure.java.io

**Goal:** file and stream I/O without leaks.

```clojure
(require '[clojure.java.io :as io])
(slurp "data.txt")  (slurp (io/resource "config.edn"))  (slurp url :encoding "UTF-8")
(spit "out.txt" "text")  (spit "out.txt" "more" :append true)
(with-open [r (io/reader "big.txt")]
  (doall (take 10 (line-seq r))))            ; realise inside with-open!
(io/copy (io/input-stream "a") (io/output-stream "b"))
(io/file "dir" "sub" "f.txt")  (file-seq dir)
(io/make-parents "out/sub/f.txt")           ; creates the parent directories only
```
- `io/resource` returns the URL for a named resource, using the context class loader when no loader is given.
- `slurp` opens a reader on its argument and returns a string; `spit` opens a writer, writes, and closes. Both pass their options to `io/reader` / `io/writer`: `:encoding` names the charset (e.g. "UTF-8") and `:append true` appends. Pass `:encoding` explicitly.
- `with-open` evaluates the body in a `try` and calls `.close` on each binding in reverse order in a `finally`.
- `line-seq` takes a `java.io.BufferedReader` and returns a lazy seq, so realise it inside `with-open`; never return it from there.
- `io/file` with several args treats the first as the parent and the rest as children, so prefer it to string concatenation for paths.

## Failure modes
- A lazy `line-seq` consumed after `with-open` has closed the reader reads from a closed reader: `doall` or reduce inside the block.
- `io/resource` yields a URL, not a path: read it with `slurp` or `io/input-stream` rather than converting it to a file.

## Self-check
Write 3 lines with `spit`, read them back with `line-seq` inside `with-open`, and count them.

## Checked
2026-11-03. Confirmed against the clojure.java.io API page and the clojure.core API page: slurp, spit, with-open, line-seq, file-seq, io/reader and writer options (:append, :encoding), io/copy, io/input-stream, io/output-stream, io/file argument rule, io/make-parents, io/resource. Removed: the UTF-8 default claim, the nil-when-absent claim, java.io.File and java.nio.file.Files method calls, the FileNotFoundException/user.dir note and the jar-file remark (Java behaviour, not in the pages read).
Method: documentation only; no commands were run.
