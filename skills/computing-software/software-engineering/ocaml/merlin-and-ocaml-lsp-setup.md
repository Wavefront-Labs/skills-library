---
id: computing-software.software-engineering.ocaml.merlin-and-ocaml-lsp-setup
name: merlin-and-ocaml-lsp-setup
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, merlin-lsp-setup, ocaml-editor-tooling, merlin, ocaml-lsp-server, vscode-ocaml-platform, dune-ocaml-merlin]
level: practitioner
status: docs-checked
description: "Install ocaml-lsp-server per switch, keep dune in watch mode, add formatters, and know how it relates to Merlin."
sources: ["https://raw.githubusercontent.com/ocaml/ocaml-lsp/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merlin and ocaml-lsp

```bash
opam install ocaml-lsp-server ocamlformat      # ocaml-lsp-server installs the ocamllsp binary
dune build --watch                              # keeps the server's build information fresh
```

## Notes
- The package is `ocaml-lsp-server`; the binary is `ocamllsp`. Install it in every opam switch where you want to use it. With Dune 3.24 or later (or the nightly), `dune tools install ocamllsp` builds it with the project's own compiler, and `eval $(dune tools env)` before launching the editor makes the editor see it.
- Usually the editor or its plugin launches `ocamllsp`. For VS Code use the OCaml Platform extension; for Emacs the README points to the `ocaml-eglot` package for Dune package management.
- The server works from information from your last build, so run Dune in watch mode. When watch mode is running, the server talks to Dune's RPC (since OCaml-LSP 1.11.0) for extra diagnostics and a `Promote` code action; save files to refresh diagnostics.
- Formatting: install `ocamlformat`, `ocp-indent` or Topiary. `ocamlformat` wins when several configs exist in one directory. `ocamlformat-rpc` (shipped with ocamlformat above 0.21.0) formats hover output; `ocp-indent-rpc` enables indentation as you type.
- The server uses Merlin internally (vendored), so Merlin need not be installed. To respect `.merlin` files pass `--fallback-read-dot-merlin` and install `dot-merlin-reader`.
- Features include completion, hover, definition, references, rename, formatting, switch implementation/interface, infer interface, typed holes, destruct and construct code actions.
- To debug in editors other than VS Code, set the LSP server trace to `verbose` in your client.

## Self-check
- [ ] Hovering an expression shows its inferred type.

## Checked
Date: 2026-11-08. Confirmed against the ocaml-lsp README on GitHub (read in full). Removed: Vim/Neovim and tuareg setup, `dune ocaml-merlin`, the "No configuration" and `.cmt` troubleshooting, `which ocamllsp` and OCaml version-matching advice, the `--log-file` flag and the ocaml.org/docs and Merlin site sources (not read).
Method: documentation only; no commands were run.
