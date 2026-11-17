---
id: computing-software.software-engineering.python.faulthandler-and-crash-tracebacks
name: faulthandler-and-crash-tracebacks
category: computing-software
field: software-engineering
product: python
tags: [python, py-debugging, faulthandler-traceback, faulthandler, segfault, deadlock-diagnosis, dump-traceback-later, sigusr1]
level: practitioner
status: docs-checked
description: "Get Python tracebacks from segfaults, hangs and deadlocks using faulthandler: enable, dump_traceback_later watchdog, and register on a signal."
sources: ["https://docs.python.org/3/library/faulthandler.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# faulthandler and crash tracebacks

When the interpreter dies from SIGSEGV/SIGFPE/SIGABRT/SIGBUS/SIGILL (C extension bug) or hangs, a normal traceback never appears. `faulthandler` dumps every thread's Python stack.

```
python -X faulthandler app.py            # or PYTHONFAULTHANDLER=1
```
```python
import faulthandler, signal, sys

faulthandler.enable(file=open("crash.log", "w"), all_threads=True)   # keep the file object alive!

# Hang watchdog: dump stacks if still running after 60 s, repeat every 60 s
faulthandler.dump_traceback_later(60, repeat=True, exit=False)
faulthandler.cancel_dump_traceback_later()

# On-demand dump from the shell: kill -USR1 <pid>   (POSIX)
faulthandler.register(signal.SIGUSR1, all_threads=True, chain=False)

faulthandler.dump_traceback()            # now, to stderr
```
`register` is not available on Windows; use `dump_traceback_later` there. `faulthandler.dump_c_stack()` (3.14) dumps the C stack of the current thread where the build and OS support it.

## Diagnosing a deadlock
1. Start with `PYTHONFAULTHANDLER=1`.
2. When it hangs: `kill -USR1 <pid>` (after `register`) or rely on the watchdog.
3. Read the dump: each thread shows the line where it is blocked (`threading.py: acquire`, `queue.get`, socket `recv`). Two threads each waiting on locks held by the other prove the cycle.

## Rules
- The handler can only use signal-safe functions, so dumps are minimal: ASCII only, filename, function name and line number (no source), at most 100 frames per thread and 100 threads (`max_threads`), most recent call first.
- Output goes to stderr by default; in containers make sure stderr is collected.

## Gotchas
- `enable`, `dump_traceback_later` and `register` keep the file descriptor of `file`; if the file is closed the dump goes nowhere or to a different file, so keep it open.
- Python frames only (plus the C stack on `enable` where supported); use a debugger or core files for more.
- `exit=True` in `dump_traceback_later` calls `_exit` with status 1 after dumping, without flushing buffers: good for CI hang guards.

## Verify
- [ ] `python -X faulthandler -c "import ctypes; ctypes.string_at(0)"` prints "Fatal Python error: Segmentation fault" with the stack.
- [ ] CI jobs use `dump_traceback_later(..., exit=True)` so a hang yields stacks rather than a silent timeout.

## Checked

- 2026-11-03: checked against the CPython docs `library/faulthandler.rst`: signals handled, `-X faulthandler` and `PYTHONFAULTHANDLER`, `enable`, `dump_traceback_later` (`repeat`, `exit`), `register` (not on Windows, `chain`), `dump_c_stack` (3.14), signal-safe limits, file descriptor caveat.
- Removed: py-spy, gdb and pytest `faulthandler_timeout` advice (not in the docs read), the GIL remark.

Method: documentation only; no commands were run.
