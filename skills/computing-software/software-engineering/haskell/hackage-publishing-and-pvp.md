---
id: computing-software.software-engineering.haskell.hackage-publishing-and-pvp
name: hackage-publishing-and-pvp
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, hackage, pvp, package-versioning-policy, cabal-upload, cabal-sdist, haddock, hackage-revisions, candidates, hackage-publishing-and-pvp]
level: advanced
status: docs-checked
description: "Release a package: Package Versioning Policy version bumps, cabal check, cabal sdist, upload candidates and publishing, tokens and documentation upload."
sources: ["https://pvp.haskell.org/", "https://cabal.readthedocs.io/en/stable/cabal-commands.html", "https://cabal.readthedocs.io/en/stable/cabal-package-description-file.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing to Hackage and the PVP

**Goal:** release a library others can depend on safely.

## Package Versioning Policy (PVP)
A version should have the form `A.B.C`, optionally with more components (for example `2.1.0.4`). `A.B` is the major version number and `C` the minor.
- Breaking change (an entity removed, a type or datatype or class definition changed, orphan instances added or any instance removed): the new `A.B` must be greater.
- Non-breaking change (only new bindings, types, classes, non-orphan instances or modules added): `A.B` may stay and `C` must increase.
- Other changes (documentation, dependency-range changes): `A.B.C` may stay the same; further components may change.
`A.B.C` identifies the API, so dependents can state bounds on it; cabal also accepts the caret form `pkgname ^>= n` (see the Cabal guide).

## Release checklist
```bash
cabal check                       # fix all errors; warnings read carefully
cabal sdist                       # dist-newstyle/sdist/<pkg>-<ver>.tar.gz
cabal build --enable-tests && cabal test
cabal upload dist-newstyle/sdist/<pkg>-<ver>.tar.gz              # a package CANDIDATE
cabal upload --publish dist-newstyle/sdist/<pkg>-<ver>.tar.gz    # publish immediately
cabal upload -d <docs-tarball>                                   # upload documentation (add --publish for a published package)
```
`cabal sdist` writes to `dist-newstyle/sdist/` by default. `cabal check` exits 1 when it finds errors, which Hackage would refuse. `cabal upload` takes `--token` (`-t`) or `--password-command` (`-P`) for credentials.

## Rules
- Published packages cannot be deleted on Hackage; upload a candidate first and check it.
- Package fields to fill in include `extra-doc-files`, `tested-with`, `source-repository`, `bug-reports` and `synopsis`.
- Hackage keeps `.cabal` file revisions; `cabal get` unpacks the latest revision unless `--pristine` is given.

## Gotchas
- `cabal sdist` reports source files it cannot find and fails; still unpack the tarball and build it before publishing.
- Over-tight upper bounds on `base` lock users out of new GHCs; bump bounds promptly. `cabal check` warns on missing upper bounds.
- Test the sdist in a clean directory.

## Self-check
- [ ] The tarball builds from an empty directory.
- [ ] Version bump matches the PVP for the API diff.

## Checked
2026-11-03. Confirmed against the PVP page, the Cabal commands page (check, sdist, upload flags `--publish`, `-d`, `--token`, `--password-command`, `--pristine`) and the package description page (`tested-with`, `extra-doc-files`, `source-repository`, `bug-reports`, `synopsis`). Removed: the `A.B.C.D` and patch-level reading, `cabal haddock --haddock-for-hackage` and the docs tarball name, the Hackage UI revision claim, and Haddock-markup description.
Method: documentation only; no commands were run.
