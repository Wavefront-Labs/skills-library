---
id: computing-software.software-engineering.perl.perl-debugger-commands
name: perl-debugger-commands
category: computing-software
field: software-engineering
product: perl
tags: [perl, perl-debugger, perl-d, breakpoints, debugger-commands, perldebug, perl-debugger-commands, perl-debugging]
level: practitioner
status: docs-checked
description: "Step through code with perl -d using n, s, r, c, b, B, L, l, p, x, T, w, a, o and R, with conditions, actions, rc files and PERLDB_OPTS non-interactive runs."
sources: ["https://perldoc.perl.org/perldebug", "https://perldoc.perl.org/perldebtut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The perl debugger (perl -d)

**Goal:** inspect a running program interactively.

```bash
perl -d script.pl args              # start under the debugger
perl -d -e 0                        # empty program: experiment with expressions
perl -d:ptkdb script.pl             # Devel::ptkdb GUI debugger
perl -dt threaded_script.pl         # threads (experimental)
PERLDB_OPTS="NonStop LineInfo=listing frame=2" perl -d script.pl    # non-interactive, trace to file "listing"
```
| Command | Action (per perldebug) |
|---|---|
| `s [expr]` / `n [expr]` | single step, descending into subs / next statement, executing over sub calls |
| `<CR>` | repeat the last `n` or `s` |
| `r` | continue until the current sub returns; dumps the return value if `PrintRet` is set (default) |
| `c [line\|sub]` | continue, optionally with a one-time breakpoint at a line or sub |
| `b [line] [condition]` | breakpoint before a line (current line if omitted, `.` also means current); conditions do not use `if`: `b 237 $x > 30`; also `b file:line cond`, `b subname`, `b postpone subname`, `b load file`, `b compile subname` |
| `B line` / `B *` | delete a breakpoint / all breakpoints; `disable` and `enable [file]:[line]` toggle one |
| `L [abw]` | list actions, breakpoints and watch expressions (all by default) |
| `l`, `l min-max`, `l subname`, `-`, `v [line]`, `.` | list next window, a range, a sub, the previous window, a few lines around the current line, the last executed line |
| `p expr` | `print` in the current package; it does not dump nested data or objects |
| `x [maxdepth] expr` | list-context evaluation, pretty-printed recursively; use `x \%h` rather than `x %h` |
| `V [pkg [vars]]` / `X [vars]` | dump package variables (default `main` / current package), without the `$` sigil |
| `y [level [vars]]` | lexical variables in scope; needs PadWalker 0.08 or higher |
| `T` | stack backtrace |
| `w expr` / `W expr` / `W *` | add a global watch expression (stops and shows old and new values) / delete one / delete all |
| `a [line] command` / `A line` / `A *` | set an action run before a line / delete one / delete all |
| `t [n]` | toggle trace mode |
| `m expr` | list methods callable on the object or package the expression gives |
| `o`, `o opt=value`, `o opt?` | display all options, set an option, print an option |
| `!n`, `!-n`, `!pattern`, `H -n` | redo a command, redo the nth previous, redo by pattern, show history |
| `h`, `h cmd`, `h h` | help; prefix with a pipe (`\|h h`) to send long output through the pager |
| `R` | restart (history, breakpoints, actions, debugger options and perl switches -w, -I, -e are preserved) |
| `q` or `^D` | quit; the only supported way to exit |

Example session: `b 42 $x > 10`, `c`, `x \%h`, `p scalar(@list)`, `n`, `T`.

## Rules
- Breakpoints can only be set on lines that begin an executable statement.
- To step off the end of the script set `inhibit_exit` to 0 (`o inhibit_exit=0`).
- Startup file: `./.perldb` or `~/.perldb` on Unix with `/dev/tty`, `perldb.ini` otherwise. After it is read, the debugger parses `$ENV{PERLDB_OPTS}` as the rest of an `o ...` line; `TTY`, `noTTY`, `ReadLine` and `NonStop` can be set there.
- `NonStop` runs without human intervention; if you set `LineInfo` to a file and interrupt the run, reset `LineInfo` to something interactive.
- `$^P` is true when the program runs under `-d`.
- By default the debugger leaves your exceptions and warnings alone. `signalLevel`, `warnLevel` and `dieLevel` above 0 add backtraces and, at `dieLevel` 2, take over your exception handler; the docs warn this can wreck a program that relies on its own exception handling.
- If a debugger command matches a function in your program, precede the function with something like `;` or `+`.
- The `frame` option controls entry and exit messages: `frame & 4` prints arguments, `frame & 16` prints return values.

## Self-check
- [ ] In `perl -d -e 0`, `p 1+2` prints `3` and `x [1,2]` dumps the array.

## Checked

Date: 2026-11-08. Confirmed against perldebug on perldoc.perl.org: every command and option row above, the rc-file names and PERLDB_OPTS handling, the NonStop and LineInfo examples, and the dieLevel warning. perldebtut was fetched but no claim here depends on it beyond perldebug. Removed: the Devel::Trace example, the claims that `x` is like Data::Dumper, that `my` variables are evaluated in the stopped frame, the specific "blank lines, comments and else lines" claim, the IDE and Devel::Camelcadet notes, RemotePort remote debugging advice and the note about Devel::Confess and `use diagnostics`, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
