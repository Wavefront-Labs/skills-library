---
id: computing-software.software-engineering.perl.exception-objects-carp
name: exception-objects-carp
category: computing-software
field: software-engineering
product: perl
tags: [perl, exception-class, carp-croak, confess, throwable, die-with-object, exception-objects-carp]
level: advanced
status: docs-checked
description: "Report errors from the caller's viewpoint with Carp, and throw exception objects with Exception::Class or the Throwable role."
sources: ["https://perldoc.perl.org/Carp", "https://metacpan.org/pod/Exception::Class", "https://metacpan.org/pod/Throwable"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception classes and Carp

**Goal:** structured errors callers can inspect, and messages that blame the right line.

## Carp
```perl
use Carp;                         # exports carp croak confess
croak "We're outta here!";        # die, from the perspective of the caller
carp  "string trimmed to 80 chars"; # warn, from the caller's perspective
confess "not implemented";        # die with stack backtrace
use Carp qw(cluck longmess shortmess);  # not exported by default
cluck "how we got here";          # warn with stack backtrace
```
- `carp`/`croak` search the call stack for the first call not marked safe and report the error from there. The result is "an educated guess", not guaranteed to be where the error was.
- Safe calls: a package calling itself; packages listed in `@CARP_NOT` (or `@ISA` when `@CARP_NOT` is empty), with transitive trust; calls from perl-internal modules; calls into the warning system. If every call is safe you get a full backtrace.
- `@CARP_NOT` must be in the package symbol table (`our @CARP_NOT;` at file scope works, a `my` variable does not).
- `$Carp::CarpLevel` skips extra frames, but the docs say to avoid it (hard to get right, usually skips too many) and use `@CARP_NOT`, `%Carp::Internal` and `%Carp::CarpInternal` instead.
- Force backtraces everywhere while debugging: `perl -MCarp=verbose script.pl`, or `PERL5OPT=-MCarp=verbose`, or `$Carp::Verbose = 1`.
- Backtrace formatting: `$Carp::MaxArgLen` (default 64), `$Carp::MaxArgNums` (default 8), `$Carp::MaxEvalLen`; objects may define `CARP_TRACE`; references can use `$Carp::RefArgFormatter`.
- Carp does not clobber `$!` and `$^E` when building messages.
- **Known limit:** Carp routines do not handle exception objects; if the first argument is a reference they just call `die`/`warn`.

## Exception::Class
```perl
use Exception::Class (
    'MyException',
    'ExceptionWithFields' => {
        isa => 'MyException', fields => ['grandiosity'],
        description => 'IPC related', alias => 'throw_fields',
    },
);
use Scalar::Util qw(blessed);
use Try::Tiny;
try   { MyException->throw(error => 'I feel funny.') }
catch { die $_ unless blessed $_ && $_->can('rethrow');
        warn $_->error, "\n", $_->trace->as_string; };

eval { ... };
if (my $e = Exception::Class->caught('MyException')) { ... }   # copy it; do not use $@ directly
throw_fields error => "No strawberry", grandiosity => "quite a bit";
```
- Options: `isa` (parent; default is `$Exception::Class::BASE_EXC_CLASS`), `fields` (scalar or arrayref; become constructor args and accessors, inherited), `alias` (a sub in the caller's namespace that calls `->throw`; called without parentheses it is checked at compile time), `description` (fixed string per class).
- `caught($class)` returns the object if the last exception is of that class or a subclass; with no argument it returns `$@`. Copy the result because a `cleanup` that uses `eval` overwrites `$@`.
- You cannot use `Exception::Class->caught` with Try::Tiny; use `blessed $_ && $_->isa(...)` there.
- The module itself recommends: with Moose or Moo prefer Throwable, and use Try::Tiny either way.
- For larger systems, declare all exception classes in one module (for example `Foo::Exceptions`). You can subclass `Exception::Class::Base` to add methods.

## Throwable
```perl
package Redirect; use Moose; with 'Throwable'; has url => (is => 'ro');
Redirect->throw({ url => $url });
die Something::Throwable->new_with_previous({ attr => $value });
```
- The role does two things: saves any previous `$@` and calls `die $self`. It is implemented with Moo; Moose also works.
- `previous_exception` holds the earlier `$@`, best effort only. `new_with_previous` builds the object while protecting `$@` and is more reliable than `new`, but does not die. `throw` on an existing object rethrows it.

## Self-check
- [ ] A caller-side `eval`/`try` receives an object of the right class; `croak` from a module reports the caller's file and line.

## Checked
Method: 2026-11-08 read the full plain-text POD of Carp, Exception::Class and Throwable via the MetaCPAN API. Removed unsupported v1 claims ($SIG{__DIE__} advice, cause field, overload stringification, Exception::Tiny, `$e->message`, never-match-message rules). Carp's object limitation added from its BUGS section.
