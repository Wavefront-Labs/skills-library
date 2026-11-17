---
id: computing-software.software-engineering.perl.event-loops-anyevent-ioasync
name: event-loops-anyevent-ioasync
category: computing-software
field: software-engineering
product: perl
tags: [perl, event-loop, anyevent, io-async, mojo-ioloop, non-blocking-io, event-loops-anyevent-ioasync]
level: advanced
status: draft
description: "Choose and use an event loop for non-blocking I/O: AnyEvent, IO::Async or Mojo::IOLoop, with timers and watchers."
sources: ["https://metacpan.org/pod/AnyEvent", "https://metacpan.org/pod/IO::Async", "https://metacpan.org/pod/Mojo::IOLoop"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event loops: AnyEvent, IO::Async, Mojo::IOLoop

**Goal:** one process, many concurrent I/O operations.

## Mojo::IOLoop (comes with Mojolicious)
```perl
use Mojo::IOLoop; use Mojo::UserAgent;
my $ua = Mojo::UserAgent->new;
my @urls = qw(https://a.example https://b.example);
Mojo::Promise->all(map { $ua->get_p($_) } @urls)->then(sub { say $_->[0]->result->code for @_ })->catch(sub { warn "@_" })->wait;
Mojo::IOLoop->timer(2 => sub { say "tick" });
Mojo::IOLoop->recurring(1 => sub { ... });
Mojo::IOLoop->start unless Mojo::IOLoop->is_running;
```

## AnyEvent
```perl
use AnyEvent; my $cv = AnyEvent->condvar;
my $w = AnyEvent->timer(after => 1, interval => 0, cb => sub { $cv->send('done') });
print $cv->recv;                                # blocks until send (only at top level)
```
Watchers (`AnyEvent->io`, `->timer`, `->signal`, `->child`) live as long as the variable holding them; dropping the variable cancels the watcher.

## IO::Async
```perl
use IO::Async::Loop; use IO::Async::Timer::Periodic;
my $loop = IO::Async::Loop->new;
$loop->add(IO::Async::Timer::Periodic->new(interval => 1, on_tick => sub { say "tick" })->start);
$loop->run;
```

## Rules
- Never block inside callbacks (no `sleep`, no blocking DBI/LWP calls); use async drivers (Mojo::UserAgent non-blocking, AnyEvent::HTTP, Net::Async::HTTP) or run blocking work in a child process (IO::Async::Function, Mojo::IOLoop->subprocess).
- Keep watcher objects referenced; a watcher stored in a lexical that goes out of scope silently stops.
- Do not mix two event loops in one process unless an adapter exists (AnyEvent has Mojo and IO::Async backends, e.g. `AnyEvent::Impl::Mojo`).
- Handle errors in every callback; exceptions inside callbacks can end the loop or be swallowed.
- Choose by ecosystem: Mojolicious apps use Mojo::IOLoop; libraries meant for any loop use AnyEvent or Future-based APIs.

## Self-check
- [ ] A 2-second timer fires while a concurrent request completes, in a single process.
