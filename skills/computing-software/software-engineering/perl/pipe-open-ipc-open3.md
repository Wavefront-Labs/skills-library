---
id: computing-software.software-engineering.perl.pipe-open-ipc-open3
name: pipe-open-ipc-open3
category: computing-software
field: software-engineering
product: perl
tags: [perl, pipe-open, ipc-open3, ipc-run3, bidirectional-pipe, pipe-function, pipe-open-ipc-open3]
level: advanced
status: docs-checked
description: "Stream to and from child processes with list-form pipe opens and IPC::Open3 for separate stderr, avoiding shell and deadlocks."
sources: ["https://perldoc.perl.org/perlipc", "https://perldoc.perl.org/perlopentut", "https://perldoc.perl.org/IPC::Open3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Piped opens, IPC::Open3 and IPC::Run3

**Goal:** read or write a child's streams without a shell.

```perl
open(my $p, '-|', 'grep', '-n', $pattern, $file) or die "fork: $!";    # read child's STDOUT (list form: no shell)
while (<$p>) { ... }
close($p) or warn "child exit status: $?";                           # reaps child; sets $?
open(my $w, '|-', 'sort', '-u') or die; print {$w} "b\na\nb\n"; close $w;   # write to child's STDIN

use IPC::Open3; use Symbol 'gensym';
my $err = gensym;
my $pid = open3(my $in, my $out, $err, 'prog', @args);    # three separate handles
close $in;
my @stdout = <$out>; my @stderr = <$err>;
waitpid($pid, 0);  my $status = $? >> 8;

```

## Rules
- Reading a child's stdout and stderr from separate pipes can block: IPC::Open3 says to use `select` or `IO::Select` with `sysread`, not readline.
- In `open3`, passing `undef` for the error handle merges stderr into stdout; a `gensym` glob gives a separate handle.
- Always `waitpid` the PID from `open3`; `close` a pipe handle waits for you.
- `pipe(READ, WRITE)` plus `fork` connects parent and child manually: close the unused ends in each process or EOF never arrives.
- Binary data: `binmode` the pipe.
- Where fork(2) is unavailable (Windows), Perl can emulate it with limitations (perlfunc fork).

## Self-check
- [ ] `perl -e 'open(my $p,"-|","echo","hi") or die; print <$p>'` prints `hi`.

## Checked
2026-11-03: confirmed against perlipc and perlfunc open (list-form -| and |- pipe opens without a shell, close waits and sets $?), IPC::Open3 (separate handles with gensym, a false error handle merges stderr into stdout, waitpid on the returned pid, select/IO::Select and sysread warning). Removed: IPC::Run3, IPC::Run, Capture::Tiny, the two-argument pipe remark and the Windows threads claim.
Method: documentation only; no commands were run.
