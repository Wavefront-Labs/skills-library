---
id: computing-software.software-engineering.perl.par-packer-fatpack-bundling
name: par-packer-fatpack-bundling
category: computing-software
field: software-engineering
product: perl
tags: [perl, par-packer, pp-executable, fatpacker, single-file-script, standalone-binary, par-packer-fatpack-bundling, perl-deployment]
level: advanced
status: docs-checked
description: "Distribute a Perl program as one file or executable using App::FatPacker (pure Perl only) or PAR::Packer's pp, with the real fatpack and pp options."
sources: ["https://metacpan.org/pod/App::FatPacker", "https://metacpan.org/pod/PAR::Packer", "https://metacpan.org/pod/pp", "https://metacpan.org/pod/fatpack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundling scripts with PAR::Packer and App::FatPacker

**Goal:** ship a tool without asking users to install dependencies.

## App::FatPacker (single script with embedded modules)
```bash
fatpack pack myscript.pl > myscript.packed.pl        # one-shot: trace, packlists, fatlib, concatenate
# or step by step
fatpack trace myscript.pl                            # writes fatpacker.trace (like perl -c; every require()d module)
fatpack packlists-for `cat fatpacker.trace` > packlists
fatpack tree `cat packlists`                         # copies the dists into a tree (fatlib)
fatpack file myscript.pl > myscript.packed.pl        # bundles lib/ and fatlib/ .pm files into a BEGIN block
```
- `trace` options: `--to=FILE`, `--to-stderr` (not both), `--use=MODULE` (extra modules in the trace, repeatable).
- Dependency code is copied in as text, so only pure-Perl dependencies can be packed, not compiled XS.
- Modules are found via `.packlist` files, usually present only for non-core distributions installed by a CPAN installer. Vendors often strip them (for example apt-get installs), so the docs recommend installing dependencies into a local::lib first. `packlists-for` normally yields all non-core distributions needed.
- The App::FatPacker API is not final (0.x release).

## PAR::Packer (pp: executable with perl embedded)
```bash
pp -o hello hello.pl            # executable (hello.exe on Windows); default name a.out
pp -M Foo::Bar -M 'Foo::**' hello.pl   # force-include modules / namespaces
pp -x hello.pl                  # also run the script ("perl inputfile") to detect run-time deps; --xargs='...' supplies @ARGV
pp -c hello.pl                  # run "perl -c" to detect deps; -n skips static scanning
pp -I /foo -a data.txt -o hello hello.pl   # extra lib path, extra file (-a "old;new" renames inside the package)
pp -X Foo::Bar hello.pl         # exclude a module
pp -p -o out.par file ; pp -P -o out.pl file   # PAR archive only / stand-alone perl script
pp -o foo foo.pl bar.pl         # several scripts: the one matching the invoked basename ($0) runs
```
- `-M` variants: `Foo::**` (all below Foo, not Foo), `Foo::*` (level 1), `Foo::` (Foo and all below).
- `-N NAMESPACE` adds all modules in a namespace, mimicking plugin loaders (unlike `-M Foo::Bar::` it does not insist on Foo/Bar.pm existing).
- Core modules are bundled by default (`-B`), except with `-p` or `-P`. `-d` omits the perl interpreter (needs a shared perl library on the target).
- `-g` builds a console-less executable on Win32. `-u` packs Unicode support (ignored for Perl 5.32+): try it if the packed program dies with "Can't locate utf8_heavy.pl".
- `-f FILTER` source filters such as Bleach hide source casually; most filters are incompatible with `__DATA__` sections. Module filtering (`-F`) applies PodStrip by default; set `PAR_VERBATIM=1` to turn that off.
- `-z N` zip compression 0-9 (default 6), `-s` signs with Module::Signature, `-L FILE` logs, `-v` verbosity, `-r` runs the result, `@file` reads extra options, `PP_OPTS` env var supplies options for every run.
- At run time contents are extracted to a cache directory (Unix example `/tmp/par-USER/cache-XXXXXXX`, hash or `-T` value); `-C` cleans the extracted files afterwards, otherwise they are cached for faster later startup.
- Recipes in the docs: stand-alone `pp -o packed.exe source.pl`; `pp -B -P -o packed.pl source.pl` (perl present, pinned core modules); `pp -P -o packed.pl source.pl` (smaller, relies on the target's core modules).
- Even the stand-alone executable needs underlying system libraries such as libc to be compatible between build and target hosts.
- Licence: pp and parl impose no licensing restrictions on generated files, provided packed third-party libraries are also available under the Artistic License.
- PAR::Packer was split out of the PAR distribution at PAR 0.97 so PAR users do not need a C compiler. Troubleshooting is in PAR::Packer::Troubleshooting (not read).

## Self-check
- [ ] The produced file runs on a clean machine and handles a plugin loaded dynamically (use `-x` or `-N`/`-M` if it is missed).

## Checked
Method: 2026-11-08 read the full plain-text POD of App::FatPacker, fatpack, PAR::Packer and pp via the MetaCPAN API; added pp and fatpack as sources. Removed unsupported v1 claims (Strawberry Perl, PAR_GLOBAL_TEMP/PAR_TEMP, `parl`, dh-make-perl/cpan2rpm alternatives, "same architecture" advice beyond the libc note).
