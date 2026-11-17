---
id: computing-software.software-engineering.perl.dist-zilla-dist-ini
name: dist-zilla-dist-ini
category: computing-software
field: software-engineering
product: perl
tags: [perl, dist-zilla, dist-ini, dzil, release-automation, podweaver, dist-zilla-dist-ini]
level: advanced
status: draft
description: "Automate releases with Dist::Zilla: dist.ini plugins, version bumps, dzil test/build/release and plugin bundles."
sources: ["https://dzil.org", "https://metacpan.org/pod/Dist::Zilla"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dist::Zilla and dist.ini

**Goal:** generate every release artefact from a small config.

```ini
; dist.ini
name    = My-Module
author  = A Person <a@example.org>
license = Perl_5
copyright_holder = A Person
copyright_year   = 2026

[@Starter]                  ; bundle: gather files, MakeMaker, MetaJSON, manifest, tests...
revision = 5
[Prereqs::FromCPANfile]     ; deps from cpanfile
[GitHub::Meta]
[NextRelease]
[Git::NextVersion]          ; version from git tags
[Git::Check]
[Git::Tag]
[Git::Push]
[UploadToCPAN]
```
```bash
cpanm Dist::Zilla && dzil authordeps --missing | cpanm   # install plugins named in dist.ini
dzil listdeps --missing | cpanm                          # install runtime/test deps
dzil new My::Module           # skeleton (uses ~/.dzil/config.ini for author data)
dzil test                     # build in a temp dir and run tests (--release runs author tests)
dzil build                    # My-Module-X.Y.Z directory and tarball
dzil release                  # runs release hooks incl. UploadToCPAN (asks for PAUSE credentials in ~/.pause)
dzil clean ; dzil smoke ; dzil authordeps
```

## Rules
- Dist::Zilla builds into a separate directory; the repository does not contain the built `Makefile.PL`, so contributors need `dzil` or you should also commit a generated `Makefile.PL` (plugin `[CopyFilesFromBuild]`).
- Pod and version insertion plugins (`[PkgVersion]`/`[OurPkgVersion]`, `[PodWeaver]`) rewrite files at build time; the checked-in source may lack `$VERSION` unless you use `[RewriteVersion]`.
- Bundles (`@Starter`, `@Basic`, `@Filter`, authors' bundles such as `@DAGOLDEN`) hide many plugins; check what a bundle includes with `dzil build -v` or its docs.
- Plugin versions matter; pin with `revision` or in `dist.ini`.
- Lighter alternatives: Minilla (`minil`), Dist::Milla, or manual `make dist` with scripts.
- Never commit PAUSE passwords; use `~/.pause` with restricted permissions or an upload token if supported.

## Self-check
- [ ] `dzil test` passes and `dzil build` creates a tarball whose files match what you expect.
