---
id: computing-software.software-engineering.ocaml.ci-with-setup-ocaml
name: ci-with-setup-ocaml
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ci-github-actions, github-actions, setup-ocaml, ocaml-ci]
level: practitioner
status: docs-checked
description: "Set up OCaml in CI with ocaml/setup-ocaml: compiler matrix, opam cache behaviour, build and test steps, lint extensions."
sources: ["https://github.com/ocaml/setup-ocaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI with setup-ocaml

```yaml
jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
        ocaml-compiler: ["4.14", "5.2"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: ocaml/setup-ocaml@v3
        with:
          ocaml-compiler: ${{ matrix.ocaml-compiler }}
      - run: opam install . --deps-only --with-test
      - run: opam exec -- dune build
      - run: opam exec -- dune runtest
```

## Notes
- The README binds to a major version (`@v3` is the latest 3.*) and warns against `@master`.
- `ocaml-compiler` is required; quote dotted versions (`"5.5"`); ranges like `5` or `5.5.x` resolve to the highest match.
- The action caches the opam root and local switch (`cache: true` default); on a hit it skips compiler installation and only runs `opam update`. Project dependencies from `opam install . --deps-only` are intentionally not cached; the README suggests `--locked` if you cache a switch after installing them.
- The README's own example matrix includes `windows-latest`; `windows-compiler` (`mingw` default or `msvc`) and `windows-environment` (`cygwin` default or `msys2`) are inputs. Compiler/OS support varies (for example no MSVC for 5.0 to 5.2), so check the README table.
- Lint extensions `ocaml/setup-ocaml/lint-doc@v3`, `lint-fmt@v3`, `lint-opam@v3` should run in separate jobs on `ubuntu-latest`.
- `opam-pin` (default true) pins local `*.opam` packages (`opam-local-packages`).

## Self-check
- [ ] The matrix covers the lowest OCaml version in your opam `depends`.

## Checked
Checked 2026-11-08 against the setup-ocaml README. Removed: the OCaml-CI remark and the "changing dependencies busts the cache" claim (the README says dependencies are not cached), the generic `dune build @fmt`/`@doc` job advice (replaced with the README's lint extensions), and the unsourced Windows C-library remark. Unchanged: the YAML structure, which follows the README example; the matrix versions are illustrative.

Method: documentation only; no commands were run.
