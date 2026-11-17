---
id: computing-software.software-engineering.ocaml.opam-install-pin-and-files
name: opam-install-pin-and-files
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, opam-packages-pin, opam-pin, opam-file, opam-install, deps-only]
level: practitioner
status: docs-checked
description: "Install packages, pin local or git sources, write an opam file with depends and build, lint it, and lock dependencies."
sources: ["https://opam.ocaml.org/doc/Usage.html", "https://opam.ocaml.org/doc/Manual.html", "https://opam.ocaml.org/doc/man/opam-install.html", "https://opam.ocaml.org/doc/man/opam-pin.html", "https://opam.ocaml.org/doc/man/opam-lint.html", "https://opam.ocaml.org/doc/man/opam-lock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opam packages and pins

```bash
opam install --deps-only -t .         # install the dependencies of the project in cwd, tests on
opam pin add mylib . --no-action      # pin the local dir as package mylib, no install prompt
opam pin add foo git+https://example.org/foo.git#branch
opam list    opam show lwt    opam search yojson
opam lint mylib.opam
```
```
opam-version: "2.0"
depends: [ "ocaml" {>= "4.14"} "dune" {>= "3.0"} "lwt" "alcotest" {with-test} ]
build: [ ["dune" "build" "-p" name "-j" jobs] ["dune" "runtest" "-p" name "-j" jobs] {with-test} ]
```

## Notes
- `--deps-only` installs the dependencies but not the named package. `-t`/`--with-test` builds and runs tests, but only for packages named on the command line.
- `opam pin add PACKAGE TARGET`: target may be a version, a path, an archive or a VCS URL; append `#branch` (or a commit) to pin a VCS ref. `--no-action` just records the pin.
- Unpin with `opam pin remove PACKAGES|TARGET` (restores the repository definition); `--all` removes every pin in the switch.
- `depends:` is a conjunction of filtered package formulas; filters include `build`, `post`, `with-test`, `with-doc`, `with-dev-setup` (opam 2.2). `build:` is a list of commands run in order and can carry filters. `name`, `version` and `jobs` are available as variables; `dev` is true for packages not built from a release archive.
- Version constraints use `=`, `!=`, `<`, `<=`, `>`, `>=` combined with `&`, `|`, `!`; the manual's example is `"foo" {>= "3" & < "4"}`.
- `opam lint` reports warnings/errors (codes like W20, E22) for an opam file or directory; `--check-upstream` also checks archive availability.
- `opam lock` writes opam files with a `.locked` suffix binding all transitive dependencies to installed versions (`--direct-only`, `--lock-suffix` options); `opam install --locked` uses a `.locked` variant of an opam file if it exists.
- With dune, `(generate_opam_files true)` in `dune-project` is the usual way to avoid hand-writing the file; that is not covered by the opam pages above, see the dune-project skill.

## Self-check
- [ ] `opam install . --deps-only --with-test` followed by `dune test` passes on a fresh switch.

## Checked
Checked 2026-11-08 against the opam usage, manual and install, pin, lint and lock man pages. Removed: the `opam list --installed` flag, the exact `<pkg>.opam.locked` filename (the lock page says only a `.locked` suffix) and the pinned-name `unpin` wording. Unchanged: install, pin, depends/build and filter behaviour; the `-p name` dune build line is a convention not verified in these pages.

Method: documentation only; no commands were run.
