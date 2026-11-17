---
id: computing-software.software-engineering.perl.try-catch-feature-try-tiny
name: try-catch-feature-try-tiny
category: computing-software
field: software-engineering
product: perl
tags: [perl, try-catch, feature-try, try-tiny, finally-block, perlsyn, try-catch-feature-try-tiny]
level: practitioner
status: docs-checked
description: "Use core try/catch (feature 'try', Perl 5.34+; warning-free without finally from 5.40) or Try::Tiny, and know how they differ on return, $_ and $@."
sources: ["https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/feature", "https://metacpan.org/pod/Try::Tiny"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try/catch feature and Try::Tiny

**Goal:** structured exception handling syntax.

## Core feature
```perl
use feature 'try';                  # 5.34+; in the :5.40 feature bundle, so "use v5.40;" also enables it
try {
    my $x = call_a_function();
    $x < 100 or die "Too big";
}
catch ($e) {                        # "my" is implied; $e holds the exception
    warn "Unable to output a value; $e";
}
```
- Availability (feature page): from 5.34; before 5.40 it was experimental and warned unless `no warnings "experimental::try";`. From 5.40, using it without `finally` no longer warns. The page still warns the feature is "partly experimental" and may change.
- `return`, `goto`, `next`/`last`/`redo` inside `try` or `catch` behave as expected; a `return` in the `try` block makes the whole containing function return (unlike `eval`).
- `try`/`catch` yield the last evaluated value as the final statement of a function or `do` block (then do not use `return`): `my $v = do { try { get() } catch ($e) { $DEFAULT } };`
- `try` blocks are invisible to `caller()`.
- Optional `finally { ... }` runs after the construct, like a `defer` block, including just before `return`, loop controls or `goto` leave the try/catch blocks. A `finally` block cannot `return`, `goto` or use loop controls, and its value is ignored. `finally` is still experimental and warns in the `experimental::try` category.

## Try::Tiny (CPAN, version 0.32 documented)
```perl
use Try::Tiny;                       # exports try, catch, finally by default
my $r = try { risky() } catch { warn "caught: $_"; undef } finally { cleanup(@_) };   # semicolon needed
```
- Blocks are subs: `return` leaves only the block (like `eval`), and `@_` of the enclosing sub is not available in `try` (copy arguments or pass `\@_`). The `catch` block gets the error in `$_` (and as `$_[0]`); `$@` keeps its previous value, so it is not the error.
- If `try` dies it returns the last value of `catch`, else undef/empty list. Because the `catch` return value is not ignored, return a false value from `catch` when you test the result for truth.
- `finally` always runs; it receives the error as `@_` if one was caught, nothing otherwise. Exceptions in `finally` cannot be trapped. A `finally` without a `catch` suppresses errors, unlike Java/Python/JS.
- It exists to avoid `eval` pitfalls: success clears `$@` (clobbering errors being handled), localizing `$@` can silently mask `die`, and before 5.14 destructors using `eval` could clear `$@`.
- `$SIG{__DIE__}` stays in effect. Lexical `$_` (for example inside `given`) can override the one `catch` sets; use `$_[0]` there.
- `try` adds a caller stack frame; Carp hides it in full traces via `%Carp::Internal`.
- Page-listed alternatives: Syntax::Keyword::Try (perl 5.14+, a real keyword so `return` and `next` work; Feature::Compat::Try switches to native syntax on newer perls), TryCatch (more features, heavier), autodie, Throwable, Error, Exception::Class::TryCatch.

## Choosing
Use core `try/catch` when the minimum Perl is 5.34 or newer, preferably 5.40+ and without `finally`. Try::Tiny for older Perls.

## Self-check
- [ ] `perl -E 'use feature "try"; no warnings; try { die "x\n" } catch ($e) { print "c:$e" }'` prints `c:x`.

## Checked
Method: 2026-11-08 read the full plain-text POD of Try::Tiny; for perlsyn and feature read only the try/catch sections (feature's "The 'try' feature" and bundle table lines, perlsyn "Try Catch Exception Handling"), not the whole pages. Resolved the v1 "unconfirmed finally" note: it is still experimental per the pages. Dropped the `eval { ...; 1 } or do` fallback and TryCatch "obsolete" labelling as unsupported.
