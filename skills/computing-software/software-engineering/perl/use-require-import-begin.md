---
id: computing-software.software-engineering.perl.use-require-import-begin
name: use-require-import-begin
category: computing-software
field: software-engineering
product: perl
tags: [perl, use-versus-require, import-method, begin-block, do-file, perlfunc, use-require-import-begin]
level: practitioner
status: docs-checked
description: "Distinguish use (compile time with import) from require (run time), BEGIN/END blocks, and conditional loading."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlmod"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# use, require, import and BEGIN

**Goal:** load code at the right time.

```perl
use Foo::Bar qw(f g);        # compile time: require + Foo::Bar->import(qw(f g))
use Foo::Bar ();             # require only, call no import
use Foo::Bar 1.20;           # die unless $Foo::Bar::VERSION >= 1.20
require Foo::Bar;            # run time; bareword is converted to Foo/Bar.pm
Foo::Bar->import('f');       # import manually after a run-time require
my $ok = eval { require JSON::XS; JSON::XS->import; 1 };   # optional dependency
require "path/file.pl";      # a string path, no pm conversion
my $mod = "Plugin::$name";  (my $file = "$mod.pm") =~ s{::}{/}g;  require $file;   # dynamic load
```

## Phases
- `BEGIN { ... }` runs as soon as it is parsed; `use` is a `BEGIN` block. `INIT`, `CHECK` run after compile; `END { ... }` runs at exit (even after `die`, not after `exec`).
- `if (...) { require X }` allows conditional loading; a `use` is a `BEGIN` block, so it always runs at compile time.
- A required file must return true on the last statement (or `1;`); `use v5.38` enables the `module_true` feature so the file need not.

## Failure modes
- `use` of a module with side effects in `import` runs even in `perl -c` checks.
- Circular `use` gives half-initialised packages: move shared code to a third module or use `require` at run time.
- `require` returns true only once per module; `%INC` records loaded files: `delete $INC{'Foo/Bar.pm'}` forces reload (hot-reload hacks).
- `do "file"` ignores `%INC`, returns the last value and sets `$@`/`$!` on errors.

## Self-check
- [ ] `perl -e 'BEGIN{print "b"} print "r"'` prints `br`.

## Checked
2026-11-03: confirmed against perlfunc (use, require forms, do FILE, package), perlmod (BEGIN, UNITCHECK, CHECK, INIT, END blocks and when END runs), perlvar (%INC, @INC) and the feature documentation (module_true in the 5.38 bundle). Removed: use if, POSIX::_exit, the use constant remark and the exact missing-module error text.
Method: documentation only; no commands were run.
