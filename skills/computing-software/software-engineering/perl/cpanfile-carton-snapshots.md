---
id: computing-software.software-engineering.perl.cpanfile-carton-snapshots
name: cpanfile-carton-snapshots
category: computing-software
field: software-engineering
product: perl
tags: [perl, cpanfile, carton, snapshot, dependency-pinning, carton-exec, cpanfile-carton-snapshots]
level: practitioner
status: docs-checked
description: "Declare Perl dependencies in a cpanfile, lock them with Carton's cpanfile.snapshot, deploy with --deployment and run apps with carton exec."
sources: ["https://metacpan.org/pod/Carton", "https://metacpan.org/pod/cpanfile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cpanfile, Carton and reproducible dependencies

**Goal:** the same module versions in dev, CI and production.

## cpanfile syntax
```perl
requires 'perl', '5.16.3';            # minimum perl; carton/cpanm error on older hosts
requires 'Plack', '1.0';              # plain number means 1.0 OR NEWER
requires 'JSON', '>= 2.00, < 2.80';   # version range
requires 'Plack', '== 0.9980';        # exact version needs the range syntax
recommends 'JSON::XS', '2.0';
conflicts 'JSON', '< 1.0';
on 'test'    => sub { requires 'Test::More', '>= 0.96, < 2.0' };
on 'develop' => sub { recommends 'Devel::NYTProf' };
feature 'sqlite', 'SQLite support' => sub { recommends 'DBD::SQLite' };
```
- Verbs: `requires`, `recommends`, `suggests`, `conflicts`. An omitted version means 0 (any version).
- Phases for `on`: configure, build, test, runtime, develop. Shortcuts `configure_requires`, `build_requires`, `test_requires`, `author_requires` exist mainly for Module::Install compatibility.
- `feature` groups requirements; the description may be omitted.
- Pin a distribution with `dist`, `mirror` or `url` options, for example `requires 'Plack', '== 0.9980', dist => 'MIYAGAWA/Plack-0.9980.tar.gz';` (a `mirror` option points at a local DarkPAN).

## Carton workflow
```bash
echo local/ >> .gitignore
carton install                    # installs into ./local, writes cpanfile.snapshot
git add cpanfile cpanfile.snapshot && git commit
carton install --deployment       # on deploy box: only versions in the snapshot, no CPAN Meta DB fallback
carton exec starman -p 8080 myapp.psgi
carton bundle                     # tarballs into vendor/cache
carton install --cached           # install from that cache
```
- `carton exec` is optional; you can instead put `local/lib/perl5` on the path with `PERL5LIB`, `-I` or `use lib`.
- Commit `cpanfile` and `cpanfile.snapshot`; keep `local` out of version control. When deploying by copying the app directory, exclude `local` and `.carton`.
- With `--deployment --cached` after `carton bundle`, deployment avoids querying CPAN Meta DB or CPAN mirrors. The bundle can include non-CPAN (DarkPAN) distributions.
- From Carton v1.0.32 the bundle also holds a package index, so a plain `cpanm -L local --from "$PWD/vendor/cache" --installdeps --notest --quiet .` works without installing Carton on the remote machine.

## Gotchas
- Carton needs a perl with the complete set of core modules; vendor perls with stripped core modules are not expected to work.
- A snapshot taken on one perl version may cause trouble with core modules on another. Simplest fix is the same perl in development and deployment (the page suggests plenv and `.perl-version`) plus `requires 'perl', ...` in the cpanfile.
- For CPAN distributions, tools exist to turn a cpanfile into toolchain formats: Module::CPANfile, Dist::Zilla::Plugin::Prereqs::FromCPANfile, Module::Install::CPANfile. `cpanfile-dump` dumps dependencies.

## Checked
Method: 2026-11-08 read the full plain-text POD of Carton and cpanfile via the MetaCPAN API. Removed unsupported claims from v1 (carton update/list/tree, --without, PERL_CARTON_PATH/--path, Pinto, cpm, snapshot-diff advice, Docker build advice, rm -rf self-check). Examples are taken from the pages.
