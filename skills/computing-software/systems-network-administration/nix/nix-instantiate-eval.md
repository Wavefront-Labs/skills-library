---
id: computing-software.systems-network-administration.nix.nix-instantiate-eval
name: nix-instantiate-eval
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-instantiate, eval-strict, drv-path, nix-eval]
level: practitioner
status: docs-checked
description: "Instantiate derivations or evaluate expressions with nix-instantiate: --expr, --eval, --strict, --raw, --json, --xml, --parse and building the resulting .drv."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-instantiate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-instantiate` evaluates expressions (default `./default.nix`; `-` reads stdin) and prints the resulting store derivation paths.

```
nix-instantiate '<nixpkgs>' --attr hello
nix-store --realise $(nix-instantiate '<nixpkgs>' --attr hello)
nix-instantiate --eval --expr '1 + 2'
nix-instantiate --eval --strict --json --expr '{ a = 1; }'
```

Options:
- `--add-root path`: register a GC root.
- `--parse`: print the syntax tree as a Nix expression.
- `--eval`: evaluate and print values; derivations are hashed and discarded, not written to the store. Output may not mean the same as the input; use `nix eval` for readable output or `--xml` for unambiguous output.
- `--strict`: with `--eval`, evaluate lists and attributes recursively (may not terminate on infinite structures).
- `--raw`: print a string verbatim without quotes, escaping or trailing newline.
- `--json`, `--xml`: structured output (XML matches the `toXML` built-in).
- `--find-file`: resolve names on `NIX_PATH` to absolute paths.
- `--read-write-mode`: instantiates every evaluated derivation, which costs time.

Without `--strict`, nested attributes show as `<unevaluated />` in XML.

## Checked

2026-11-04: synopsis, every option listed, the --eval warning and the strict versus non-strict XML example confirmed against the nix-instantiate manual page. Removed nothing.

Method: documentation only; no commands were run.
