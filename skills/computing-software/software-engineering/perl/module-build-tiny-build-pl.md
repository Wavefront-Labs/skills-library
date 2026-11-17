---
id: computing-software.software-engineering.perl.module-build-tiny-build-pl
name: module-build-tiny-build-pl
category: computing-software
field: software-engineering
product: perl
tags: [perl, module-build, build-pl, module-build-tiny, dist-build, directory-layout, module-build-tiny-build-pl]
level: practitioner
status: docs-checked
description: "Drive a Perl distribution with a Build.PL using Module::Build::Tiny: supported features, required directory layout, build options and incompatibilities."
sources: ["https://metacpan.org/pod/Module::Build::Tiny"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module::Build::Tiny

**Goal:** a lightweight Build.PL driver (documented version 0.053), a drop-in replacement for Module::Build.

```perl
# Build.PL
use Module::Build::Tiny;
Build_PL();
```
```bash
perl Build.PL
./Build            # or: Build build
./Build test
./Build install
```
(`Build` options listed on the page: `verbose`, `install_base`, `installdirs`, `prefix`, `install_path`, `destdir`, `uninst`, `config`, `pure-perl`, `create_packlist`.)

## Supported
Pure Perl distributions, building XS or C, recursive test files, MYMETA, man page generation, generated code from PL files, module sharedirs, dynamic prerequisites. Under 200 lines versus Module::Build's 6,700+.

## Not supported
HTML documentation generation, and extending Module::Build::Tiny. It does not support authoring: the page recommends Dist::Zilla::Plugin::ModuleBuildTiny or App::ModuleBuildTiny for developing a distribution.

## Layout it expects
- `.pm`, `.xs` and `.pod` files in `lib/`; executables in `script/`; tests in `t/`.
- Distribution sharedirs in `share/`; module sharedirs under `module-share/` (for example `module-share/Foo-Bar` for `Foo::Bar`).
- `.c` files in `src/` are compiled together with the `.xs` file matching the distribution name.

## Options and incompatibilities
- Options can also come from the `PERL_MB_OPT` environment variable, set at configuration stage as with Module::Build.
- Only a subset of Module::Build's permissive argument parsing works: `./Build destdir=/foo` fails; use `./Build --destdir=/foo`.
- `.modulebuildrc` is not supported. local::lib older than 1.006008 may then fail with "ERROR: Can't create /usr/local/somepath"; if `perl -Mlocal::lib` output contains `MODULEBUILDRC` but not `PERL_MB_OPT `, upgrade local::lib.

## Self-check
- [ ] `perl Build.PL && ./Build test` passes with sources under `lib/` and tests under `t/`.

## Checked
Method: 2026-11-08 read the full plain-text POD of Module::Build::Tiny 0.053 via the MetaCPAN API. The Module::Build page was not read, so its source URL and the v1 claims about it (core removal in 5.22, status, `Build.PL` constructor arguments, Minilla commands, cpanm ordering, `Build dist`) were dropped; the claim that it reads `META.json`/`cpanfile` was also unsupported by this page and removed.
