---
id: computing-software.software-engineering.perl.safe-process-sql-injection
name: safe-process-sql-injection
category: computing-software
field: software-engineering
product: perl
tags: [perl, command-injection, sql-injection, input-validation, safe-open, safe-process-sql-injection]
level: practitioner
status: docs-checked
description: "Prevent injection in Perl: list-form system and open, taint mode (-T), SQL placeholders and untrusted input."
sources: ["https://perldoc.perl.org/perlsec", "https://perldoc.perl.org/perlopentut", "https://perldoc.perl.org/perlperf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe command execution, taint mode and SQL placeholders

**Goal:** untrusted input never becomes code.

## Commands
```perl
system('convert', $in, $out) == 0 or die "convert failed";     # list form: no shell
open(my $p, '-|', 'sort', '-u', glob('unsorted/*.txt'));       # list-form pipe open, from perlopentut
```
- perlsec: Perl does not call the shell to expand wildcards when `system` and `exec` get an explicit parameter list rather than a string. `open`, `glob` and backticks have no such calling convention in perlsec's account, so it shows a fork-and-`exec` pattern for backticks: "never call the shell at all".
- perlopentut: the list form of `open` (`'-|'` or `'|-'` as the mode, then the command and its arguments as separate elements) invokes the command directly, bypassing the shell, which is safer for variable arguments and for filenames with spaces. To pass a real metacharacter such as `*`, expand it with `glob` and pass the list. The list form works on Unix-based systems with a real `fork` and on Windows with Perl 5.22 or later.
- Use the three-argument `open` with the mode separate from the filename or command; perlopentut shows a shell command passed as the third argument being interpreted by the shell, so never build it from untrusted data.

## Taint mode (perlsec)
- Run with `-T` for programs that handle external data. Data from arguments, `<STDIN>`, files and `%ENV` is tainted; tainted values taint expressions that use them. Hash keys are never tainted, `print` and `syswrite` arguments are not checked, and tainting prevents stupid mistakes rather than removing the need for thought.
- Untaint only by extracting a validated substring with a regex capture (`$data = $1`); `use locale` stops `\w` from untainting.
- Under `-T` the environment variables `PERL5LIB`, `PERLLIB` and `PERL_USE_UNSAFE_INC` are ignored. Perl checks that `IFS`, `CDPATH`, `ENV` and `BASH_ENV` are empty or untainted when starting subprocesses, and `PATH` must be set safely.
- Since Perl 5.26 the current directory is not in `@INC` by default.
- Use file tests on user-supplied filenames, open files after dropping special privileges, and remember Perl will open tainted filenames for reading.
- `Scalar::Util::tainted()` tests for taint.

## SQL
perlperf: always use SQL placeholders (`?`), and consider pre-fetching data sets. Identifiers cannot be bound as placeholders, so whitelist them before interpolating. (The DBI manual on metacpan is blocked, so placeholder syntax details were not checked.)

## Self-check
- [ ] No `system`, backtick or pipe `open` is built from a single interpolated string containing input; untrusted values are bound as placeholders.

## Checked
2026-11-09. Read the matching sections of perlsec (taint, environment variables, shell avoidance) and perlopentut (list-form pipes, platform note), and the SQL placeholder sentence of perlperf. Removed because not on the cited pages or the page is blocked (metacpan DBI): the DBI call examples, IPC::Run3, Capture::Tiny, String::ShellQuote, path-traversal and File::Temp snippets, web output escaping, cookie flags, CSRF, ReDoS, Storable/YAML advice, upload limits, Perl::Critic policies and the filename self-check.
Method: documentation only; no commands were run.
