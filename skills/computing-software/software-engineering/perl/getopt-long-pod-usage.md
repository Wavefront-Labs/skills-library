---
id: computing-software.software-engineering.perl.getopt-long-pod-usage
name: getopt-long-pod-usage
category: computing-software
field: software-engineering
product: perl
tags: [perl, getopt-long, pod-usage, command-line-options, bundling, usage-message, getopt-long-pod-usage, perl-cli-apps]
level: intro
status: docs-checked
description: "Parse command-line options with Getopt::Long, validate arguments and print help from POD with Pod::Usage."
sources: ["https://perldoc.perl.org/Getopt::Long", "https://perldoc.perl.org/Pod::Usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getopt::Long and Pod::Usage

**Goal:** a standard CLI interface.

```perl
use Getopt::Long qw(GetOptions :config bundling no_ignore_case);
use Pod::Usage;
my %opt = (verbose => 0, jobs => 4);
GetOptions(\%opt,
    'verbose|v+',           # counted: -vv
    'jobs|j=i',             # integer value
    'name|n=s',             # string
    'tag=s@',               # repeatable list
    'define|D=s%',          # key=value hash
    'dry-run!',             # --dry-run / --no-dry-run
    'help|h|?', 'man',
) or pod2usage(2);          # bad options: usage to STDERR, exit 2
pod2usage(1) if $opt{help};
pod2usage(-verbose => 2) if $opt{man};
pod2usage("$0: FILE required") unless @ARGV;
my @files = @ARGV;           # non-options remain
__END__

=head1 NAME

mytool - do something

=head1 SYNOPSIS

mytool [options] FILE...

=head1 OPTIONS

=over 4

=item B<--jobs|-j> N

Number of workers.

=back

=cut
```

## Rules
- Config `bundling` lets single-character options be combined (`-vvj4`); single-character options then match case-sensitively and long options case-insensitively (`ignorecase_always` changes that). `auto_abbrev` (on by default) lets option names be abbreviated to uniqueness.
- `GetOptions` returns false and warns on unknown options or bad values; always `or pod2usage(2)`.
- Option values like `--num=abc` for `=i` fail; defaults come from your hash before parsing.
- `--` ends options; `@ARGV` keeps the rest. `GetOptionsFromArray(\@args, ...)` makes testing easy.
- `pod2usage` defaults: exit status 2 with verbose level 0 if neither is given; `pod2usage(1)` exits 1 and prints more (verbose 1); `-verbose => 2` prints the whole manpage and `99` with `-sections` prints chosen sections.
- `pod2usage(-exitval => 'NOEXIT', -verbose => 1)` prints without exiting.

## Self-check
- [ ] `perl tool.pl --help` prints SYNOPSIS and OPTIONS; `perl tool.pl --bogus` exits with status 2 (pod2usage(2)).

## Checked

2026-11-02. Checked against perldoc Getopt::Long (spec suffixes ! + =s@ =s%, GetOptionsFromArray, bundling and ignorecase_always, auto_abbrev, :config import) and Pod::Usage (-exitval, -verbose levels 0/1/2/99, -sections, NOEXIT, default exit status 2 and verbose-level defaults). Removed: the -CA decoding advice, the list of subcommand frameworks, and the claim that single-dash long options need -- under bundling (not stated).

Method: documentation only; no commands were run.
