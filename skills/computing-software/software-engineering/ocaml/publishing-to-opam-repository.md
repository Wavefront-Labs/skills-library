---
id: computing-software.software-engineering.ocaml.publishing-to-opam-repository
name: publishing-to-opam-repository
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, opam-publish, dune-release, opam-repository, release-package]
level: advanced
status: docs-checked
description: "Tag a release, build a tarball with dune-release, publish to GitHub and submit a PR to opam-repository."
sources: ["https://raw.githubusercontent.com/tarides/dune-release/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing to opam-repository

```bash
opam install dune-release
dune-release tag                 # tag from the change log's first version heading
dune-release check               # lint, build and test before distrib
dune-release distrib             # distribution archive in the build directory
dune-release publish             # GitHub release + tarball artifact
dune-release opam pkg            # opam file with tarball URL and hash
dune-release opam submit         # PR to ocaml/opam-repository
```

## Notes
- `dune-release` supports only Dune projects released on GitHub. Running it with no argument does distrib, publish, opam pkg and submit in one go; the basic workflow is `dune-release tag` then `dune-release`. It asks permission before significant actions.
- `dune-release tag` reads the version from the first item of the change log (Markdown or Asciidoc), e.g. `## v1.0.1 (2019-09-30)`, or take it from the command line (`dune-release tag v1.0.1`). `dune-release tag -d v1.0.1` deletes the tag. Dune and dune-release work only with annotated tags (`git tag -a`).
- `distrib` uses the source tree of the HEAD commit, so uncommitted changes are ignored. Files marked `export-ignore` in the repository-root `.gitattributes` are left out of the archive.
- With several opam packages in the repo, one tarball and one GitHub release are made, with several opam files added to the opam repository.
- If `publish` fails with `Permission denied`, it pushes over ssh (`git@github.com:`); set `git config url."https://github.com/".pushInsteadOf "git@github.com:"` to push over https instead.
- `dune-release help <command>` gives full man pages.

## Self-check
- [ ] `dune-release check` passes and the tarball builds from a clean checkout.

## Checked
Date: 2026-11-08. Confirmed against the dune-release README on GitHub (read in full). Removed: `opam lint`, opam-repository CI and lower-bound advice, `opam-publish`, `x-ci-accept-failures`, the token requirement and the opam.ocaml.org and ocaml.org/docs sources (unreadable stubs).
Method: documentation only; no commands were run.
