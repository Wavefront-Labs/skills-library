---
id: computing-software.software-engineering.perl.makefile-pl-makemaker
name: makefile-pl-makemaker
category: computing-software
field: software-engineering
product: perl
tags: [perl, makefile-pl, extutils-makemaker, make-test, writemakefile, manifest, makefile-pl-makemaker, perl-distribution-build]
level: practitioner
status: docs-checked
description: "Package a module with Makefile.PL using ExtUtils::MakeMaker: metadata, prerequisites, make test/dist and MANIFEST."
sources: ["https://perldoc.perl.org/ExtUtils::MakeMaker", "https://perldoc.perl.org/perlnewmod"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExtUtils::MakeMaker and Makefile.PL

**Goal:** a standard CPAN distribution built by `perl Makefile.PL`.

```perl
# Makefile.PL
use 5.010001;
use strict; use warnings;
use ExtUtils::MakeMaker;
WriteMakefile(
    NAME             => 'My::Module',
    VERSION_FROM     => 'lib/My/Module.pm',
    ABSTRACT_FROM    => 'lib/My/Module.pm',
    AUTHOR           => 'A Person <a@example.org>',
    LICENSE          => 'perl_5',
    MIN_PERL_VERSION => '5.010001',
    PREREQ_PM        => { 'Moo' => '2.0' },
    TEST_REQUIRES    => { 'Test::More' => '0.98' },
    CONFIGURE_REQUIRES => { 'ExtUtils::MakeMaker' => '6.64' },
    META_MERGE       => { 'meta-spec' => { version => 2 }, resources => { repository => { type => 'git', url => 'https://example.org/repo.git', web => 'https://example.org/repo' } } },
    test             => { TESTS => 't/*.t' },
);
```
```bash
perl Makefile.PL && make && make test && make install       # (use nmake/gmake on Windows)
make disttest ; make dist                                    # disttest builds and tests a fresh distribution copy; dist builds the tarball
make manifest                                                # regenerates MANIFEST (review it); MANIFEST.SKIP excludes files
prove -b t/                                                  # after make, tests with blib
```

## Rules
- Layout: `lib/`, `t/`, `Makefile.PL`, `MANIFEST`, `Changes`, `README`; scripts go in `EXE_FILES => ['bin/tool']`.
- `VERSION_FROM` parses the file for a single line containing `$VERSION`; keep it on one line.
- Tests required, not `PREREQ_PM`, belong in `TEST_REQUIRES` (MakeMaker 6.64+); `CONFIGURE_REQUIRES` needs 6.52+.
- `make clean` removes local temp files; `make realclean` deletes derived files including `blib/`.
- Prefer `META_MERGE` over `META_ADD` unless you want to override the default metadata.
- To run tests in subdirectories set `test => { TESTS => 't/*/*.t' }`; `TEST_VERBOSE=1` shows raw test output.
- Any XS code for module `Foo::Bar` should be in `Bar.xs`.

## Failure modes
- Files missing from MANIFEST are missing from the distribution; `make distcheck` reports differences between the tree and MANIFEST and `make disttest` tests the built copy.

## Self-check
- [ ] `make disttest` passes on a fresh checkout.

## Checked

2026-11-02. Checked against perldoc ExtUtils::MakeMaker (WriteMakefile keys NAME, VERSION_FROM, ABSTRACT_FROM, LICENSE, MIN_PERL_VERSION, PREREQ_PM, TEST_REQUIRES since 6.64, CONFIGURE_REQUIRES since 6.52, META_MERGE vs META_ADD, EXE_FILES, test => { TESTS }, TEST_VERBOSE, make clean / realclean / manifest / dist / disttest / distcheck, nmake and dmake on Windows). Removed: the h2xs and Module::Starter commands, the META.json-at-dist and automatic XS compile remarks, the LICENSE file in layout, and the hard-coded paths gotcha (not stated on the pages).

Method: documentation only; no commands were run.
