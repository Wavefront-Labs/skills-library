---
id: computing-software.software-engineering.ocaml.static-linking-and-release-builds
name: static-linking-and-release-builds
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, static-binaries, ocaml-deployment, static-linking, musl, release-build, ccopt-static]
level: advanced
status: docs-checked
description: "Build OCaml release binaries with the dune release profile and pass linker flags such as -ccopt via link_flags."
sources: ["https://dune.readthedocs.io/", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-workspace/profile.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/executable.rst", "https://ocaml.org/manual/5.5/native.html", "https://ocaml.org/manual/5.5/flambda.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release and static builds

```bash
dune build --profile release ./bin/main.exe
```
```lisp
(executable (name main) (link_flags (-ccopt -static)))
```

## Notes
- The `release` profile is what opam releases and `dune build -p <package>` use; it drops development-only defaults such as warnings-as-errors and `-opaque`. Select it with `--profile release` or a `(profile release)` stanza in `dune-workspace` (the command-line option wins).
- `(link_flags <flags>)` on `executable` passes additional flags to the linker.
- `-ccopt <option>` passes the option to the C compiler and linker (`ocamlopt` manual). Whether `-ccopt -static` produces a fully static executable depends on your C toolchain and on static versions of the C libraries being installed; test it on the target platform and inspect the result with your platform's linker inspection tool (for example `ldd` on Linux).
- `-O3` (and `-O2`, `-Oclassic`, `-inline`) are Flambda options, available only with a compiler configured with `-flambda`. Dune adds no `-O2` or `-O3` by default in any profile, so set it explicitly via `ocamlopt_flags (:standard -O3)` if your switch is Flambda.
- Code compiled with Flambda cannot be linked into the same program as code compiled without it.
- The ocamlopt `-nodynlink` flag produces code that cannot be linked into a shared library or PIE; many systems produce PIEs by default, so use `-ccopt -no-pie` at link time if needed.

## Self-check
- [ ] The release binary was built with `--profile release` and its dynamic dependencies were inspected on the target OS.

## Checked
Date: 2026-11-08. Confirmed against Dune docs source on GitHub (dune-workspace/profile.rst, dune/executable.rst) and the OCaml 5.5 manual pages for ocamlopt (native.html: `-ccopt`, `-nodynlink`) and Flambda (flambda.html: `-O2`, `-O3`, `-Oclassic`, `-inline`, configure `-flambda`). Removed: musl and Alpine setup, `ocaml-option-musl` / `ocaml-option-static` package names, glibc static-link advice, `strip` and `-ccopt -s`, macOS and Windows static claims, opam sandbox flags and `dune build --release`.
Method: documentation only; no commands were run.
