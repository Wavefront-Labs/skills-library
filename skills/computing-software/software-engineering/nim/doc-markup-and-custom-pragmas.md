---
id: computing-software.software-engineering.nim.doc-markup-and-custom-pragmas
name: doc-markup-and-custom-pragmas
category: computing-software
field: software-engineering
product: nim
tags: [doc-markup-and-custom-pragmas, documentation-generation, nodoc, deprecated, since, doc-groups, rst-directives, doc-visibility, docgen-pragma, nim]
level: advanced
status: docs-checked
description: "Control Nim docgen output: doc comments, exported-only visibility, the deprecated pragma and code-block markup."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/doc/docgen.md
  - https://github.com/nim-lang/Nim/blob/devel/doc/manual.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Doc markup tips: deprecation and visibility

Goal: polish the generated docs.

- Commands: `nim doc <file>.nim` (HTML), `nim doc2tex` (LaTeX), `nim jsondoc` (JSON). For a project use `nim doc --project --index:on --outdir:htmldocs <main>.nim`; without `--outdir` the output goes to an `htmldocs` folder beside the source (or `$nimcache/htmldocs` with `--usenimcache`).
- Comments starting with `##` are documentation, parsed as RST with basic Markdown also supported. Put one space after `##`.
- Docs are generated only for exported symbols (name followed by `*`); `--showNonExports` also shows non-exported fields of an exported type.
- Mark a symbol deprecated with `{.deprecated.}` or with a message: `proc thing(x: bool) {.deprecated: "use thong instead".}`. The pragma attaches to procs and variables (`var x {.deprecated.}: char`).
- Highlighted code in RST: `.. code-block:: nim`.
- Inside a doc comment keep indentation consistent after the first line; the baseline is set by the first non-whitespace character.

Gotchas:
- Make sure `x.nim` and `x.md` do not share a base name in the same package when flattening output, or they both write `x.html`.
- Anchors from `nim doc` include a numeric identifier that is not stable when symbols are added or removed; link by the plain name instead.

Verify: an unexported symbol is absent from the output and a deprecated one is flagged at use sites.

## Checked

2026-11-08. Read: doc/docgen.md from nim-lang/Nim in full for the sections up to output directories and the "Other input formats" and anchor sections (partial: index-file and later sections skimmed only for the terms searched), and the deprecated-pragma section of doc/manual.md (manual searched by section, not read in full). Removed: `:nodoc:`, `since` markers, overload grouping, `.. contents::` advice and the unresolved-link hint gotcha (not found in these sources); tut1 and lib.html dropped from sources.
Method: documentation only; no commands were run.
