---
id: computing-software.software-engineering.perl.local-lib-perlbrew-plenv
name: local-lib-perlbrew-plenv
category: computing-software
field: software-engineering
product: perl
tags: [perl, local-lib, perlbrew, plenv, perl-versions, perl-install, local-lib-perlbrew-plenv]
level: practitioner
status: docs-checked
description: "Manage Perl versions and per-user module trees with perlbrew, plenv and local::lib."
sources: ["https://metacpan.org/pod/local::lib", "https://github.com/tokuhirom/plenv", "https://raw.githubusercontent.com/gugod/App-perlbrew/master/lib/App/perlbrew.pm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local::lib, perlbrew and plenv

**Goal:** separate your Perl from the system Perl.

## perlbrew
```bash
curl -L https://install.perlbrew.pl | bash      # installs under ~/perl5/perlbrew; follow the on-screen bashrc/cshrc step
perlbrew init
perlbrew available                              # what can be installed
perlbrew install perl-<version>                 # a name from 'available'
perlbrew list                                   # what is installed
perlbrew switch perl-<version>                  # set as default
perlbrew use perl-<version>                     # current shell only
perlbrew off                                    # back to the system perl
perlbrew exec -- perl -E 'say $]'               # run a command under every perlbrew perl
```
- Everything lives in the perlbrew root, `~/perl5/perlbrew` by default; set `PERLBREW_ROOT` before running the installer to put it elsewhere (for example when HOME has a quota).
- You must source the bashrc/cshrc perlbrew provides so it can adjust `PATH`.
- Use `perlbrew --notest install ...` to skip tests; `PERLBREW_SYSTEM_PERL` selects the Perl used to run the installer when it is not `/usr/bin/perl` or `/usr/local/bin/perl`.
- If you install perlbrew from CPAN (`cpan App::perlbrew`), use the system `cpan` with `perlbrew off` first.

## plenv (rbenv-style)
```bash
git clone https://github.com/tokuhirom/plenv.git ~/.plenv
echo 'export PATH="$HOME/.plenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(plenv init -)"' >> ~/.bash_profile         # shims and completion; restart the shell
git clone https://github.com/tokuhirom/Perl-Build.git ~/.plenv/plugins/perl-build/   # provides 'plenv install'
plenv install --list ; plenv install <version> [-Dusethreads]
plenv global <version> ; plenv local <version>          # local writes .perl-version in the directory
plenv rehash ; plenv install-cpanm
```
- Precedence: `plenv shell` (PLENV_VERSION) over the `.perl-version` file over `plenv global`; the global version `system` means the system perl.
- plenv is incompatible with perlbrew: remove perlbrew and its shell-init lines first. plenv has no built-in local::lib integration.
- Run `plenv rehash` after installing a Perl or a CPAN module that ships an executable.

## local::lib
```bash
perl -Mlocal::lib                                       # prints the exports, does not set them
eval "$(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)"     # sets PERL5LIB, PERL_LOCAL_LIB_ROOT, PERL_MB_OPT, PERL_MM_OPT and PATH
perl Makefile.PL --bootstrap                            # from the local::lib source: install it into ~/perl5
```
- Put the eval line in your shell profile (the page appends it to `~/.bashrc`) so installs and runs agree.
- A `.bashrc` activation is re-applied in sub-shells; guard it with `[ $SHLVL -eq 1 ] && eval ...` or use `.bash_profile`.
- `perl -Mlocal::lib=--deactivate,<path>` undoes an activation; `perl -Mlocal::lib=./` targets a directory other than `~/perl5`.

## Self-check
- [ ] `which perl` and `perl -v` show the selected version in a new shell.

## Checked

Confirmed on the local::lib page, the plenv README and the App::perlbrew source and POD on GitHub (perlbrew.pm). Removed because the pages do not state them or the perlbrew manual on MetaCPAN was blocked: `perlbrew lib create`, `install-cpanm` and `--as` / Configure flag examples for perlbrew, the `cpanm --local-lib` bootstrap, the `#!/usr/bin/env perl` shebang note, Strawberry Perl, Carton, cron and systemd advice, and fixed Perl version numbers.

Method: docs-only read of cited pages, 2026-11-08
