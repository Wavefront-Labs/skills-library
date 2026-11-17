---
id: computing-software.software-engineering.ocaml.deprecations-and-stdlib-evolution
name: deprecations-and-stdlib-evolution
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, deprecations-and-compat, deprecated-alert, pervasives, stdlib-prefix, compatibility]
level: practitioner
status: docs-checked
description: "Handle deprecation alerts with [@@deprecated] and use the Since notes of the Stdlib API to set a compatible OCaml version floor."
sources: ["https://ocaml.org/releases", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecations and compatibility

```ocaml
let f x = g x [@@deprecated "use g"]
```

## Notes
- The `deprecated` attribute is an alias for the `deprecated` alert (OCaml manual, attributes chapter).
- Check the lowest OCaml version you support and add CI for it; the Since notes in the Stdlib API docs give the floor of newer functions (`In_channel` since 4.14, `String.starts_with` since 4.13, `Mutex.protect` since 5.1).

## Self-check
- [ ] The build is warning-free on the oldest and newest supported compilers.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the attributes chapter ([@@deprecated] and the deprecated alert) and the In_channel, String and Mutex API pages (Since 4.14, 4.13 and 5.1).

Removed or corrected: the Pervasives removal timeline and String.lowercase rename, the -alert command-line syntax, the opam depends line, ocaml-compiler-libs and stdcompat, dune lang advice, and the code line using [@alert].

Method: documentation only; no commands were run.
