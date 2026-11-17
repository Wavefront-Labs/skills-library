---
id: computing-software.software-engineering.perl.fork-wait-sockets
name: fork-wait-sockets
category: computing-software
field: software-engineering
product: perl
tags: [perl, fork, waitpid, zombie-processes, io-socket, tcp-server, fork-wait-sockets]
level: advanced
status: docs-checked
description: "Create child processes with fork, reap them with waitpid, avoid zombies, and write TCP clients and servers with IO::Socket::IP."
sources: ["https://perldoc.perl.org/perlipc", "https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/IO::Socket::IP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fork, wait and IO::Socket

**Goal:** basic multi-process and socket programs.

```perl
use POSIX ':sys_wait_h';
my %kids;
for my $job (@jobs) {
    my $pid = fork() // die "fork: $!";
    if ($pid == 0) { run($job); exit 0 }      # child: always exit, never fall through
    $kids{$pid} = $job;
}
while (%kids) { my $pid = waitpid(-1, 0); last if $pid < 0; delete $kids{$pid}; warn "failed" if $? }

use IO::Socket::IP;                            # IPv4 and IPv6
my $srv = IO::Socket::IP->new(Listen => 5, LocalPort => 8080, ReuseAddr => 1) or die $!;
while (my $c = $srv->accept) { $c->autoflush(1); my $line = <$c>; print $c "echo: $line"; close $c }
my $cl = IO::Socket::IP->new(PeerHost => 'example.org', PeerPort => 80, Timeout => 5) or die "$@";
```

## Rules
- `fork` returns the child's PID in the parent, 0 in the child, undef on failure. File descriptors are shared with the child. Perl tries to flush output handles before forking but may not on some platforms, so set `$|` or call `autoflush` on open handles to avoid duplicate output (perlfunc fork).
- Reap every child (`wait`, `waitpid`, or on some systems `$SIG{CHLD}='IGNORE'`) to prevent zombies (perlfunc fork, perlipc).
- Sockets: `IO::Socket::IP` uses getaddrinfo, so it works for IPv4 and IPv6; pass `Timeout` to bound a connect.
- On platforms without fork(2), such as Windows, Perl can be built to emulate it with limitations (perlfunc fork, perlfork).

## Failure modes
- Forgetting `exit` in the child runs the parent's remaining code twice.

## Self-check
- [ ] After the run, no zombie child processes remain (check with `ps`).

## Checked
2026-11-03: confirmed against perlfunc (fork return values and undef on failure, pre-fork flushing, zombies, waitpid with -1 and WNOHANG, Windows emulation), perlipc ($SIG{CHLD} IGNORE) and IO::Socket::IP (Listen, ReuseAddr, PeerHost, PeerPort, Timeout, getaddrinfo). Removed: DBI InactiveDestroy, Parallel::ForkManager, IO::Socket::SSL, IO::Select, double fork, $/ for protocols, Test::TCP and Net::EmptyPort, the EINTR failure mode.
Method: documentation only; no commands were run.
