---
id: computing-software.software-engineering.clojure.cljfmt-and-zprint-formatting
name: cljfmt-and-zprint-formatting
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, cljfmt, zprint, formatter, indentation, check, fix, cljfmt-zprint-format]
level: practitioner
status: docs-checked
description: "Format Clojure consistently with cljfmt (check/fix, .cljfmt.edn indents) or zprint (styles, binary/babashka/uberjar), and run the check in CI or pre-commit."
sources: ["https://github.com/weavejester/cljfmt", "https://github.com/kkinnear/zprint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cljfmt and zprint

**Goal:** remove formatting debates; enforce one layout automatically.

## cljfmt
```bash
cljfmt check                      # report formatting errors (binary; --help lists options)
cljfmt fix                        # correct them
clj -Tcljfmt check / fix          # after: clj -Ttools install io.github.weavejester/cljfmt '{:git/tag "<tag>"}' :as cljfmt
lein cljfmt check / fix           # plugin: [dev.weavejester/lein-cljfmt "<version>"] in :plugins
```
- Also installable via a bash install script, Homebrew (`brew install weavejester/brew/cljfmt`, the
  recommended tap), or as a library `dev.weavejester/cljfmt` (also runnable as a Babashka task).
- Config: `.cljfmt.edn` or `cljfmt.edn`, searched in the current and parent directories. Since 0.16.0, `.clj`
  config files are ignored unless `--read-clj-config-files` is passed. In Leiningen put options under the
  `:cljfmt` key (add `:load-config-file? true` to also load the standard file).
- Keys: `:indents` maps symbols to indent rules and replaces the defaults; `:extra-indents` appends to them.
  `:remove-surrounding-whitespace?` (default true), `:split-keypairs-over-multiple-lines?` (default false),
  `:sort-ns-references?` (default false). Others include `:indentation?`, `:remove-trailing-whitespace?`,
  `:insert-missing-whitespace?`, `:file-pattern`, `:parallel?`, `:paths`.

## zprint
- A pretty-printer library and command line tool for Clojure code and Clojure/EDN data (MIT licence).
- Modes: classic (heuristics, ignores whitespace in function definitions), respect blank lines, and indent
  only (lines are only re-indented, nothing moves to another line).
- Run it as a precompiled macOS/Linux binary, via Babashka (`bb.edn` task or `bbin`), as an uberjar (starts in
  seconds), as a library, or via a VS Code extension.
- Configure with an options map; `{:style :community}` or `{:style :respect-bl}` are the simplest changes.
  Other styles include indent-only, respect-nl, hiccup, justified and how-to-ns.

## CI/pre-commit
- Run `check` in CI so unformatted files fail the build; `fix` can be used in a pre-commit hook (a practice,
  not stated on the pages). Choose one formatter per repo.

## Self-check
Run `check` on a deliberately mis-indented file, see it fail, then `fix` and re-check.

## Checked
Method: 2026-11-08 read the cljfmt and zprint GitHub pages. Removed unsupported claims: the `clojure -Tcljfmt` deps.edn alias form, `:remove-consecutive-blank-lines?`, `:inner`/`:block` rules and `^:indent` metadata, zprint's `.zprintrc`/`:width`/`;!zprint {:format :skip}`, cljstyle and standard-clojure-style tags, clojure-lsp format-on-save. The cljfmt page names no ignore mechanism or :cljfmt/indent metadata. Self-check unchanged, not run.
