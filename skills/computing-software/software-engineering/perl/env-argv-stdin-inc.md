---
id: computing-software.software-engineering.perl.env-argv-stdin-inc
name: env-argv-stdin-inc
category: computing-software
field: software-engineering
product: perl
tags: [perl, env-hash, argv-array, stdin-stdout, inc-hash, perlrun, env-argv-stdin-inc]
level: practitioner
status: docs-checked
description: "Read environment variables and arguments, set child environments, detect interactive terminals and find loaded modules."
sources: ["https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/perlrun"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# %ENV, @ARGV, STDIN, %INC and invocation data

**Goal:** the program's inputs from the outside world.

```perl
my $home = $ENV{HOME} // $ENV{USERPROFILE} // die "no home";
local $ENV{LC_ALL} = 'C';                                  # visible to child processes during this scope
my $name = shift @ARGV // die "usage: $0 NAME\n";          # outside subs shift reads @ARGV
my @files = @ARGV;                                          # remaining arguments
delete $ENV{PERL5LIB};
my $interactive = -t STDIN && -t STDOUT;                    # terminal checks
chomp(my $answer = <STDIN> // '');                          # undef at EOF
print STDERR "diagnostic\n";   warn "also stderr\n";
printf "%s\n", join ",", sort keys %ENV;
$| = 1;                                                      # flush STDOUT per print
exit(2) if $bad;                                             # exit code; die exits 255 (or errno-based)
```

## Rules
- Setting a value in `%ENV` changes the environment of child processes started afterwards (perlvar); `local` restores it on scope exit.
- Exit status: `die` exits with `$!` if non-zero, else `$? >> 8` if non-zero, else 255. `exit N` explicitly for CLI contracts.
- `@ARGV` elements are bytes unless perl runs with `-CA`, which expects them to be UTF-8 (perlrun).
- `%INC` maps `Foo/Bar.pm` to the loaded path; `@INC` is the search list.
- STDIN, STDOUT, STDERR, DATA, ARGV, ARGVOUT and `_` stay usable as bareword handles even when the `bareword_filehandles` feature is off (feature docs).
- `$ENV{PATH}` in taint mode must be set to a safe value before `system` (see perlsec).

## Self-check
- [ ] `perl -e 'print $0'` prints `-e` (perlvar).

## Checked
2026-11-03: confirmed against perlvar (%ENV, $0 is -e under -e, %INC, @INC, $?, END), perlfunc (die exit status rule: errno, then $? >> 8, then 255; shift on @ARGV; file test -t), perlrun (-CA means @ARGV is UTF-8) and perlsec (safe PATH under taint). Removed: Windows %ENV key case claim, XS getenv claim, Encode::decode_utf8, __FILE__/__DATA__ constants bullet, Getopt::Long pointer, shell self-check.
Method: documentation only; no commands were run.
