---
id: computing-software.software-engineering.perl.cpan-cpanm-install
name: cpan-cpanm-install
category: computing-software
field: software-engineering
product: perl
tags: [perl, cpan-client, cpanm, install-modules, cpanminus, cpan-mirror, cpan-cpanm-install, perl-cpan-ecosystem]
level: intro
status: docs-checked
description: "Install CPAN modules with the cpan shell or cpanminus: where modules land, local::lib, urllist mirrors, notest, MyConfig and what cpanm does not do."
sources: ["https://perldoc.perl.org/CPAN", "https://metacpan.org/pod/App::cpanminus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing modules with cpan and cpanm

**Goal:** reliable module installs.

```bash
cpanm Module::Name                        # install from CPAN
cpanm -h                                  # full option list (or: perldoc cpanm)
perl -MCPAN -e shell                      # CPAN.pm shell
```
```
cpan> install Acme::Meta                  # by module name
cpan> install NWCLARK/Acme-Meta-0.02.tar.gz   # by distribution path
cpan> notest install Tk                   # skip the test phase for this install
cpan> m /lorem/                           # search modules; also a (author), d (distribution), i (any)
cpan> o conf urllist unshift http://cpan.dev.local/CPAN   # add a mirror; 'o conf' shows config
```

## cpanm facts (App::cpanminus)
- A script that gets, unpacks, builds and installs modules and "does nothing else"; zero configuration, no dependencies. Requires perl 5.8.1+, `tar` or Archive::Tar, `make`, Module::Build (core in 5.10), and a C compiler for XS modules.
- Index: it queries the CPAN Meta DB site, falling back to the MetaCPAN search API. From 1.6004 it sends your perl version in the User-Agent unless you pass `--no-report-perl-version`.
- Fetched files are unpacked under `~/.cpanm`, cleaned up periodically; relocate with `PERL_CPANM_HOME`.
- Install location follows ExtUtils::MakeMaker and Module::Build settings (`PERL_MM_OPT`, `PERL_MB_OPT`), by default perl's `site_perl`. If local::lib is configured, cpanm respects it. If you have neither local::lib nor write permission, cpanm sets up a local::lib-compatible `perl5` directory under your home automatically; avoid that by running as root, with `--sudo`, or with `--local-lib`.
- It does not support: distributions whose tests need STDIN, Build.PL/Makefile.PL that prompt even with `PERL_MM_USE_DEFAULT`, or non-numeric `VERSION` (such as 1.1a). Report those to the module author.
- It does not do CPAN Testers reporting (App::cpanminus::reporter), RPM building, listing outdated modules (App::cpanoutdated), showing changes (cpan-listchanges) or distroprefs patching; use CPAN, CPANPLUS or those tools.

## CPAN.pm facts (perldoc CPAN)
- Defaults from `CPAN/Config.pm` are overridden by a user file `CPAN/MyConfig.pm`, best placed at `$HOME/.cpan/CPAN/MyConfig.pm`; `mkmyconfig` writes it for you.
- `o conf` inspects and changes config (`o conf KEY VALUE`, list values via `shift|unshift|push|pop|splice`); `o conf defaults` reverts to saved values.
- `notest` skips tests; `force` overrides failures; both are deliberate risks.

## Rules
- Prefer a user tree (local::lib) over `sudo` into the system perl.
- Failing tests usually mean a missing system library or a real incompatibility: read the build log, and use `notest` only knowingly.
- XS modules need a compiler and headers.

## Self-check
- [ ] After an install, `perl -MModule::Name -e 'print $Module::Name::VERSION'` prints a version.

## Checked
Confirmed on the perldoc CPAN page (shell commands, notest/force, MyConfig, o conf, urllist) and the metacpan App::cpanminus page (description, dependencies, index, install-location behaviour, unsupported cases, features it lacks).
Removed: the individual cpanm command-line flags (`--installdeps`, `--notest`, `-L`, `--mirror`, `--uninstall`, `--info`, `--look`, build log paths), version-pinning syntax, the cpan `-l`/`-a` flags, distro-package and Carton advice, none of which appear on the cited pages.
Method: docs-only read of cited pages, 2026-11-08
