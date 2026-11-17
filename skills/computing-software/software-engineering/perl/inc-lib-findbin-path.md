---
id: computing-software.software-engineering.perl.inc-lib-findbin-path
name: inc-lib-findbin-path
category: computing-software
field: software-engineering
product: perl
tags: [perl, inc-path, use-lib, findbin, perl5lib, perl-lib, inc-lib-findbin-path]
level: practitioner
status: docs-checked
description: "Control where Perl finds modules: @INC, use lib, FindBin relative paths, PERL5LIB, -I and how taint mode changes the search."
sources: ["https://perldoc.perl.org/perlrun", "https://perldoc.perl.org/lib", "https://perldoc.perl.org/FindBin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @INC, use lib, FindBin and PERL5LIB

**Goal:** make scripts find their own libraries reliably.

```perl
use FindBin qw($Bin);
use lib "$Bin/../lib";                 # relative to the script, not the cwd
BEGIN { unshift @INC, '/opt/app/lib' }
```
```bash
perl -Ilib script.pl          # add to @INC from the command line
PERL5LIB=/opt/app/lib:/opt/other/lib perl script.pl
perl -e 'print "$_\n" for @INC'
perl -MSome::Module -e 'print $INC{"Some/Module.pm"}'
```

## Search order (perlrun, lib)
`-I` directories are prepended to `@INC`; `PERL5LIB` directories are searched before the standard library; `use lib` adds its directories to the start of `@INC` at compile time. `@INC` initially holds the `-I` arguments followed by the default Perl library (perlvar). Under taint checks (`-T`, `-t`, setuid or setgid) neither `PERL5LIB` nor `PERLLIB` is consulted. Prior to Perl 5.26 `.` was in `@INC`; it has been removed, and `PERL_USE_UNSAFE_INC=1` reinstates it as a legacy workaround.

## Rules
- Under `-e` or a script read from STDIN, `FindBin` sets `$Bin` and `$RealBin` to the current directory; `$RealBin` is `$Bin` with links resolved. Two modules using FindBin from different directories under one interpreter (mod_perl) get wrong answers; `FindBin::again()` re-runs it.
- `use lib` is processed at compile time, so it must come before the `use Module` that needs it.
- Child processes inherit `PERL5LIB` because changes to `%ENV` reach children (perlvar).
- Set `$ENV{PERL_USE_UNSAFE_INC}=1` only as a deliberate legacy workaround for old test suites.

## Self-check
- [ ] Running the script from another directory (`cd / && perl /path/script.pl`) still loads `lib/` modules.

## Checked
2026-11-03: confirmed against perlrun (-I prepends to @INC, PERL5LIB, taint mode ignores PERL5LIB and PERLLIB, PERL_USE_UNSAFE_INC), lib (use lib is almost BEGIN { unshift(@INC, LIST) }), FindBin ($Bin, $RealBin, -e behaviour, again) and perlvar (@INC initial contents, . removed in 5.26, %INC). Removed: prove -l, perldoc -l, File::Basename dirname, local::lib, Cwd::abs_path, FindBin::libs, the earlier search-order claim (use lib actually goes in front of -I), do FILE bare-name claim.
Method: documentation only; no commands were run.
