---
id: computing-software.software-engineering.ocaml.flambda-and-optimisation-flags
name: flambda-and-optimisation-flags
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, flambda-options, flambda, ocamlopt-o3, inlining, config-flambda]
level: advanced
status: docs-checked
description: "Check for flambda with ocamlopt -config, use -O3, -inline and -unsafe correctly, and measure before keeping any optimisation flag."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flambda and optimisation flags

```bash
ocamlopt -config | grep flambda        # flambda: true|false
ocamlopt -O3 -inline 200 -unsafe file.ml     # see notes
```

## Notes
- Without flambda, `-O2`/`-O3` flags are accepted and silently ignored.
- With flambda, `-O3` enables more aggressive inlining; `-inline N` sets the threshold. `-unsafe` removes bounds checks (undefined behaviour on bugs).
- Flambda is selected when the compiler is configured; code compiled with Flambda cannot be linked into the same program as code compiled without it. Always benchmark before and after.
- Attributes direct the inliner: `[@@inline always]` or `[@@inline never]` on a function declaration, `[@inlined]` on a call, and `[@unrolled n]` on a recursive call.

## Self-check
- [ ] `ocamlopt -config` shows `flambda: true` before expecting `-O3` to do anything.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Flambda chapter (the flambda: true line of -config, -O3, -inline, flags accepted silently without Flambda, no mixing of Flambda and non-Flambda code, inliner attributes) and the ocamlopt page (-unsafe).

Removed or corrected: the opam switch command, all dune advice and the claim that Flambda improves allocation-heavy code.

Method: documentation only; no commands were run.
