---
id: computing-software.software-engineering.perl.warn-die-handlers-sig
name: warn-die-handlers-sig
category: computing-software
field: software-engineering
product: perl
tags: [perl, sig-die, sig-warn, autodie-exceptions, warn-handler, perlvar, warn-die-handlers-sig]
level: advanced
status: docs-checked
description: "Install $SIG{__WARN__} and $SIG{__DIE__} handlers safely, check $^S, and use autodie exceptions."
sources: ["https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/autodie", "https://perldoc.perl.org/perlipc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signal handlers for die and warn, autodie

**Goal:** central logging of warnings and fatals without breaking control flow.

```perl
local $SIG{__WARN__} = sub { push @warnings, @_ };       # capture warnings in a scope
local $SIG{__WARN__} = sub { log_it('warn', @_) };       # or log them
$SIG{__DIE__} = sub {
    return if $^S;                      # inside eval: let the exception propagate untouched
    log_it('fatal', @_);
};
END { ... }                              # runs on normal exit and after an uncaught die
```
- `$^S` is true inside an `eval`, undef while compiling, false at top level.
- A `__DIE__` handler may rethrow a modified message or object with `die`; if it returns, exception processing continues as normal (perlvar).
- Avoid heavy logic in `__DIE__`: it fires for every `die`, including those inside `eval`.


## autodie
`use autodie;` makes built-ins throw `autodie::exception` objects: test with `$@->matches('open')`. The pragma has lexical scope, and `no autodie qw(unlink)` turns it off for a function.

## Failure modes
- A `__DIE__` handler that does not check `$^S` converts every caught exception into a logged fatal.
- Setting `$SIG{__WARN__}` globally without `local` hides warnings from the rest of the program.

## Self-check
- [ ] `perl -e '$SIG{__WARN__}=sub{print "W:@_"}; warn "x\n"'` prints `W:x`.

## Checked
2026-11-03: confirmed against perlvar ($SIG{__WARN__}, $SIG{__DIE__} called even inside eval, $^S values, END blocks) and autodie (autodie::exception, matches, lexical scope, no autodie). Removed: the claim that the handler is disabled during its own run, Carp::Always, Devel::Confess, Test::Warnings, Test::Warn, Test::Fatal, autodie method names other than matches, and the core-since claim.
Method: documentation only; no commands were run.
