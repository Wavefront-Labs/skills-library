---
id: computing-software.software-engineering.perl.system-exec-backticks
name: system-exec-backticks
category: computing-software
field: software-engineering
product: perl
tags: [perl, system-call, backticks, exec, capture-tiny, ipc-cmd, system-exec-backticks, perl-processes-ipc]
level: practitioner
status: docs-checked
description: "Run external commands safely: list-form system, exit status decoding, and capturing output with backticks and qx."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlipc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system, exec and capturing command output

**Goal:** run commands without shell injection and with correct status handling.

```perl
system('git', 'status', '--short') == 0 or die "git failed: " . ($? >> 8);   # list form: no shell
my $out = `ls -l`;            # qx// (shell, if the string has metacharacters)
chomp(my @lines = `df -h`);
exec('perl', $script, @args) or die "exec: $!";    # replaces this process
```

## Rules
- The one-string form `system("cmd $arg")` is passed to the system's command shell when it contains shell metacharacters. Interpolating untrusted data is shell injection; use the list form.
- `$?` encodes status: exit code is `$? >> 8`, signal `$? & 127`, core flag `$? & 128`; `-1` means the command could not start (see `$!`).
- Backticks capture STDOUT only; add `2>&1` (shell syntax) to include stderr.
- `qx` in list context returns lines; with a list-style safe version use `open(my $p, '-|', @cmd)`.
- `system` returns the wait status, not "success"; a true return means failure.
- `exec` never returns on success; any code after it only runs on failure.
- Set a timeout with `alarm` and an eval/die pair (perlfunc alarm).
- In taint mode, sanitise `$ENV{PATH}` and arguments first.

## Failure modes
- Ignoring non-zero statuses; assuming output encoding is UTF-8 (decode).
- Zombie children if you use `fork` without `wait`.

## Self-check
- [ ] `perl -e 'system("false") == 0 or print "fail ", $?>>8'` prints `fail 1`.

## Checked
2026-11-03: confirmed against perlfunc (system list form and shell metacharacter rule, exec returning only on failure, qx and backticks, $?) and perlvar ($? decoding: >> 8, & 127, & 128; -1 for failure to start), perlsec (taint and PATH) and autodie (qw(:all) covering system with IPC::System::Simple). Removed: Capture::Tiny, IPC::Run3, IPC::Run, capturex, Win32::Process, and the /bin/sh -c and cmd.exe detail.
Method: documentation only; no commands were run.
