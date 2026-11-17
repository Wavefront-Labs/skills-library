---
id: computing-software.software-engineering.perl.die-eval-block
name: die-eval-block
category: computing-software
field: software-engineering
product: perl
tags: [perl, die, eval-block, error-variable, local-eval-error, perlfunc, die-eval-block, perl-errors]
level: practitioner
status: docs-checked
description: "Trap exceptions with eval BLOCK, test failure by the eval's return value, protect $@ with local, and rethrow."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlvar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# die, eval BLOCK and $@

**Goal:** reliable exception handling in core Perl.

```perl
my $ok = eval {
    risky();
    1;                                   # true value only reached on success
};
unless ($ok) {
    my $err = $@ || 'unknown error';     # copy at once
    warn "failed: $err";
    die $err;                            # rethrow
}
die "message\n";                         # trailing newline: no line-number suffix is appended
die { code => 404, msg => 'not found' }; # exceptions can be refs/objects
eval { ... }; if (my $e = $@) { ... }
```

## Rules
- `eval BLOCK` is the exception catcher; `eval STRING` compiles code (avoid it for error handling).
- `$@` is empty on success. Testing the eval's return value is more robust than testing `$@` alone: `eval { ...; 1 } or do { ... }`. A control-flow operator such as `last` or `goto` can bypass the setting of `$@` (perlfunc).
- `local $@;` protects an existing `$@` from being overwritten by a nested `eval` (the pattern in perlfunc eval).
- `return` inside `eval {}` returns from the eval, not the enclosing sub.
- `$SIG{__DIE__}` is called for every `die`, even inside eval; use `$^S` to test whether inside an eval, or avoid the hook for control flow.
- `die` with a string that does not end in a newline appends the script line number and the input line number (if any) of the last-read handle.
- `warn` prints to STDERR, `$SIG{__WARN__}` can capture it.
- `$!` is for system errors (numeric and string), `$?` for child process status, `$@` for exceptions.

## Failure modes
- Catching everything and ignoring: always log or rethrow what you cannot handle.

## Self-check
- [ ] `perl -e 'eval { die "x\n" }; print "got: $@"'` prints `got: x`.

## Checked
2026-11-03: confirmed against perlfunc (die: newline rule, reference exceptions, local copy of $@; eval BLOCK: return value, $@ empty on success, return, local $@ pattern; warn) and perlvar ($@, $^S, $SIG{__DIE__} called inside eval, $!, $?). Removed: the claim that destructors clear $@ (perlfunc only documents the pre-5.14 local-restore ordering), the nested-eval bullet and the precedence bullet, and exact message-format wording.
Method: documentation only; no commands were run.
