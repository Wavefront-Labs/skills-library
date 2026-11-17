---
id: computing-software.software-engineering.ocaml.ocamlformat-configuration
name: ocamlformat-configuration
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocamlformat-config, ocaml-formatting, ocamlformat, dune-fmt, ocamlformat-profile, format-on-save]
level: intro
status: docs-checked
description: "Add a .ocamlformat with version and profile next to dune-project, run dune fmt or dune build @fmt, and check formatting in a dedicated CI job."
sources: ["https://github.com/ocaml-ppx/ocamlformat", "https://dune.readthedocs.io/en/stable/howto/formatting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ocamlformat

```
# .ocamlformat  (same directory as dune-project)
version = 0.29.0
profile = default
```
```bash
dune fmt                               # short for dune build @fmt --auto-promote
dune build @fmt                        # check only; fails when files differ
dune build @fmt --auto-promote         # check and promote in one go
```

## Notes
- The ocamlformat README names three predefined profiles: `default`, `ocamlformat` and `janestreet`.
- Dune's formatting guide says the `version` line is checked by OCamlFormat; pin it and install the matching ocamlformat (the README example uses 0.29.0, check the current release before copying).
- Most formatting configuration lives in `.ocamlformat`; dune-side options are in the formatting stanza.
- The same guide recommends a dedicated CI job for the formatting check.
- The repository itself ships a `.ocamlformat-ignore` file, but the README does not document the format; read the ocamlformat manual before relying on it.

## Self-check
- [ ] `dune build @fmt` is clean on a fresh clone.

## Checked
Checked 2026-11-08 against the ocamlformat README and the dune formatting guide. Removed: profile list entries beyond the three named, the `disable` attribute and `(* ocamlformat-ignore *)` comment, the claim that a missing version stops the formatter, editor and format-on-save details, and the claims about comments and semantics, none of which those pages state. Unchanged: file location, `dune fmt`, `@fmt`, `--auto-promote`, version checking.

Method: documentation only; no commands were run.
