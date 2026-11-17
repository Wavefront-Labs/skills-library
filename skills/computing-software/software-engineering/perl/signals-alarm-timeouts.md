---
id: computing-software.software-engineering.perl.signals-alarm-timeouts
name: signals-alarm-timeouts
category: computing-software
field: software-engineering
product: perl
tags: [perl, signals, sig-handlers, alarm-timeout, kill-function, sigchld, signals-alarm-timeouts]
level: advanced
status: docs-checked
description: "Handle signals with %SIG, set timeouts with alarm, and write async-safe handlers (SIGINT, SIGTERM, SIGCHLD, SIGALRM)."
sources: ["https://perldoc.perl.org/perlipc", "https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/POSIX"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signals, %SIG and alarm timeouts

**Goal:** react to signals and enforce timeouts.

```perl
my $stop = 0;
$SIG{INT} = $SIG{TERM} = sub { $stop = 1 };       # set a flag; act in the main loop
until ($stop) { work(); }

my $res = eval {
    local $SIG{ALRM} = sub { die "timeout\n" };
    alarm 5;                                      # whole seconds (Time::HiRes provides ualarm)
    my $r = slow_call();
    alarm 0;
    $r;
};
alarm 0;
die $@ if $@ && $@ ne "timeout\n";

kill 'TERM', $pid;  kill 0, $pid;                 # signal 0: does the process exist?
$SIG{CHLD} = 'IGNORE';                             # auto-reap children (no exit status)
$SIG{PIPE} = 'IGNORE';                             # ignore SIGPIPE
local $SIG{__WARN__} = ...;
```

## Rules
- Perl uses "safe signals": handlers run between ops, not inside C calls; a long blocking syscall defers the handler until it returns, except that most blocking syscalls get interrupted (EINTR) and the handler then runs. `POSIX::sigaction` and `Sys::SigAction` give finer control; `PERL_SIGNALS=unsafe` is discouraged.
- Keep handlers tiny: set a flag or `die`; do not do I/O or allocate heavily.
- Restore state in `local $SIG{...}`; handlers are global per process.
- SIGCHLD: `$SIG{CHLD} = sub { while ((my $p = waitpid(-1, WNOHANG)) > 0) { ... } }` with `use POSIX ':sys_wait_h'`.

## Self-check
- [ ] A 1-second `alarm` around `sleep 10` makes the eval return with `$@ eq "timeout\n"` in about one second.

## Checked
2026-11-03: confirmed against perlfunc (alarm: whole seconds, one timer, eval/die pair for timing out a call, Time::HiRes for finer granularity; kill with signal 0; waitpid with WNOHANG), perlipc (deferred signals, $SIG{CHLD} IGNORE, handlers should do little) and perlport (signal emulation limits on Windows). Removed: PERL_SIGNALS and Sys::SigAction remarks, the EINTR statement, driver-specific limitations and the %SIG name listing.
Method: documentation only; no commands were run.
