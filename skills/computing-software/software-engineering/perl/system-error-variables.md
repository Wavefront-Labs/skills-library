---
id: computing-software.software-engineering.perl.system-error-variables
name: system-error-variables
category: computing-software
field: software-engineering
product: perl
tags: [perl, errno-variable, child-status, process-id-variable, dollar-zero, perlvar, system-error-variables]
level: practitioner
status: docs-checked
description: "Interpret $!, %!, $?, $@, $0, $$, $^O, $^T and $^X correctly, copying them before they change."
sources: ["https://perldoc.perl.org/perlvar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $!, $@, $?, $0 and process variables

**Goal:** read the status variables at the right time.

| Variable | Meaning |
|---|---|
| `$!` | last system error: number in numeric context ($!+0), message in string context; `%!` keys like `$!{ENOENT}` |
| `$@` | last `eval` exception |
| `$?` | wait status of last `system`, backticks, `wait`, `close` of a pipe |
| `$0` | program name; assignable (changes `ps` title on many systems) |
| `$$` | current process id |
| `$^O` | operating system name (for example `MSWin32` on Windows) |
| `$^T` | script start time (epoch seconds) |
| `$^X` | path to the running perl binary |
| `$]` / `$^V` | Perl version (number / version object) |
| `$;` `$,` `$\` `$"` `$/` | separators: multidim key, print field, print record, list interpolation, input record |
| `$.` | current line number of the last read handle |
| `$0`, `@ARGV`, `%ENV`, `@INC`, `%INC` | invocation, args, environment, search path |

```perl
open(my $fh, '<', $f) or die "open $f: $!";
my $errno = $! + 0; my $msg = "$!";             # copy immediately
if ($!{ENOENT}) { ... }                          # use POSIX/Errno names portably
system('prog') == 0 or die sprintf("exit %d signal %d core %d", $? >> 8, $? & 127, $? & 128);
printf "perl %vd on %s\n", $^V, $^O;
```

## Rules
- `$!` is only meaningful right after a call reported failure; successful calls may leave stale values. Perl itself may set it to non-zero on failure even if no system call is performed.
- Check `$? == -1` for "failed to start" (the reason is in `$!`).
- Exit code of a process is `$? >> 8`; `$? & 127` is the terminating signal.
- `local $|` and `$|++` control autoflush on the selected output handle.
- `$,`/`$\`/`$"` are global; always `local` them.
- Use `use English;` for readable aliases (`$OS_ERROR`, `$CHILD_ERROR`).

## Self-check
- [ ] `perl -e 'system("exit 3"); print $? >> 8'` prints `3` (Unix).

## Checked
2026-11-03: confirmed against perlvar ($!, %!, $?, $@, $0, $$, $^O, $^T, $^V, $^X, $], $;, $., $| , English names OS_ERROR and CHILD_ERROR; $? >> 8 and & 127; END can change $?) and perlfunc (system and die). Removed: the exact value list for $^O, the DESTROY and print overwrite claim, the $0 path remark and the English performance note.
Method: documentation only; no commands were run.
