---
id: computing-software.software-engineering.ocaml.runtime-environment-variables
name: runtime-environment-variables
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, runtime-variables, ocamlrunparam, ocamllib, caml-ld-library-path, ocamlparam]
level: practitioner
status: docs-checked
description: "Know OCAMLRUNPARAM, OCAMLLIB, CAML_LD_LIBRARY_PATH, OCAMLFIND_CONF and OCAMLPARAM and which affect compile versus run time."
sources: ["https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime and tool environment variables

| Variable | Effect |
|---|---|
| `OCAMLRUNPARAM` | runtime params, comma-separated: `b` backtrace, `s` minor heap size (words), `o` space overhead, `v` GC verbosity (sum of flags), `l` stack limit (words), `d` max domains, `R` randomised hash tables, `W` runtime warnings |
| `CAMLRUNPARAM` | fallback when `OCAMLRUNPARAM` is unset |
| `OCAMLLIB` | directory of the standard library (`CAMLLIB` is the fallback) |
| `CAML_LD_LIBRARY_PATH` | directories searched for shared C libraries by the bytecode runtime |
| `OPAMROOT`, `OPAMSWITCH` | opam root and active switch (set by `opam env --root` / `--switch` with `--set-root` / `--set-switch`) |

## Notes
- Size values accept the multipliers `k`, `M` and `G`; an unrecognised option letter makes the whole parameter ignored. Example from the manual: `export OCAMLRUNPARAM='b,s=256k,v=0x015'`.
- `b` can take a value: `b=0` turns backtrace printing off.
- Check the manual's runtime chapter for the full parameter list of your version.

## Self-check
- [ ] `env | grep -i caml` shows no surprising leftovers when debugging a build.

## Checked

2026-11-02. Checked against the OCaml 5.5 manual runtime chapter (ocaml.org/manual/5.5/runtime.html): OCAMLRUNPARAM option letters b, s, o, v, l, d, R, W and their meanings, CAMLRUNPARAM fallback, OCAMLLIB with CAMLLIB fallback, CAML_LD_LIBRARY_PATH, size multipliers, the example value; and the opam man page for OPAMROOT / OPAMSWITCH. Removed (not in those pages): OCAMLPARAM, OCAMLFIND_CONF, OCAMLPATH, DUNE_PROFILE, DUNE_CACHE and the remarks about OCAMLPARAM and which tools read OCAMLRUNPARAM.

Method: documentation only; no commands were run.
